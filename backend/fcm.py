import os
import time
import logging
from typing import List, Dict, Any
try:
    import firebase_admin
    from firebase_admin import credentials, messaging
except Exception:
    firebase_admin = None
    credentials = None
    messaging = None

_inited = False
_enabled = False

def _init() -> None:
    global _inited, _enabled
    if _inited:
        return
    _inited = True
    if firebase_admin is None:
        _enabled = False
        return
    path = os.environ.get("FCM_CREDENTIALS_PATH") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not path or not os.path.exists(path):
        _enabled = False
        return
    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(cred)
    _enabled = True

def send_tokens(tokens: List[str], title: str, body: str, data: Dict[str, str]) -> List[str]:
    _init()
    if not tokens:
        return []
    ids: List[str] = []
    for t in tokens:
        if t.startswith("debug"):
            logging.info(f"FCM debug send token={t} title={title} body={body} data={data}")
            ids.append(f"debug-{int(time.time())}")
            continue
        if not _enabled:
            continue
        try:
            msg = messaging.Message(token=t, notification=messaging.Notification(title=title, body=body), data=data)
            rid = messaging.send(msg)
            ids.append(rid)
        except Exception:
            pass
    return ids

def send_tokens_detail(tokens: List[str], title: str, body: str, data: Dict[str, str]) -> List[Dict[str, Any]]:
    _init()
    res: List[Dict[str, Any]] = []
    for t in tokens:
        if t.startswith("debug"):
            logging.info(f"FCM debug send token={t} title={title} body={body} data={data}")
            res.append({"token": t, "ok": True, "id": f"debug-{int(time.time())}"})
            continue
        if not _enabled:
            res.append({"token": t, "ok": False, "error": "disabled"})
            continue
        try:
            msg = messaging.Message(token=t, notification=messaging.Notification(title=title, body=body), data=data)
            rid = messaging.send(msg)
            res.append({"token": t, "ok": True, "id": rid})
        except Exception as e:
            res.append({"token": t, "ok": False, "error": str(e)})
    return res
