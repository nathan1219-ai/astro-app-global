import os
import time
import hmac
import base64
import json
import hashlib

def _secret() -> str:
    return os.environ.get("AUTH_SECRET", "change-me")

def hash_password(p: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", p.encode("utf-8"), salt, 100_000)
    return base64.b64encode(salt).decode("utf-8") + ":" + base64.b64encode(dk).decode("utf-8")

def verify_password(p: str, hp: str) -> bool:
    try:
        s, d = hp.split(":")
        salt = base64.b64decode(s.encode("utf-8"))
        dk = hashlib.pbkdf2_hmac("sha256", p.encode("utf-8"), salt, 100_000)
        return hmac.compare_digest(base64.b64encode(dk).decode("utf-8"), d)
    except Exception:
        return False

def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

def create_jwt(sub: int, exp_sec: int = 7*24*3600) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": sub, "exp": int(time.time()) + exp_sec}
    h = _b64url(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    p = _b64url(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing = f"{h}.{p}".encode("utf-8")
    sig = hmac.new(_secret().encode("utf-8"), signing, hashlib.sha256).digest()
    return f"{h}.{p}.{_b64url(sig)}"

def decode_jwt(tok: str) -> dict | None:
    try:
        h, p, s = tok.split(".")
        signing = f"{h}.{p}".encode("utf-8")
        sig = base64.urlsafe_b64decode(s + "=")
        mac = hmac.new(_secret().encode("utf-8"), signing, hashlib.sha256).digest()
        if not hmac.compare_digest(sig, mac):
            return None
        data = json.loads(base64.urlsafe_b64decode(p + "=").decode("utf-8"))
        if int(time.time()) > int(data.get("exp", 0)):
            return None
        return data
    except Exception:
        return None
