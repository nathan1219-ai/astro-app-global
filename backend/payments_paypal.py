import os
import json
import requests

def _base() -> str:
    env = os.environ.get("PAYPAL_ENV", "sandbox").lower()
    return "https://api-m.paypal.com" if env == "live" else "https://api-m.sandbox.paypal.com"

def _token() -> str:
    cid = os.environ.get("PAYPAL_CLIENT_ID")
    secret = os.environ.get("PAYPAL_CLIENT_SECRET")
    if not cid or not secret:
        return ""
    r = requests.post(_base() + "/v1/oauth2/token", auth=(cid, secret), data={"grant_type": "client_credentials"})
    if r.status_code != 200:
        return ""
    return r.json().get("access_token", "")

def create_order(user_id: int, level: str, months: int, return_url: str, cancel_url: str) -> str:
    t = _token()
    if not t:
        return ""
    amount = "4.99" if level == "Premium" else "9.99"
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "reference_id": str(user_id),
                "amount": {"currency_code": "USD", "value": amount},
                "custom_id": json.dumps({"user_id": user_id, "level": level, "months": months}),
            }
        ],
        "application_context": {
            "return_url": return_url,
            "cancel_url": cancel_url,
        },
    }
    r = requests.post(_base() + "/v2/checkout/orders", headers={"Authorization": f"Bearer {t}", "Content-Type": "application/json"}, json=payload)
    if r.status_code not in (200, 201):
        return ""
    j = r.json()
    links = j.get("links", [])
    for l in links:
        if l.get("rel") == "approve":
            return l.get("href")
    return ""

def capture_order(order_id: str):
    t = _token()
    if not t:
        return None
    r = requests.post(_base() + f"/v2/checkout/orders/{order_id}/capture", headers={"Authorization": f"Bearer {t}", "Content-Type": "application/json"})
    if r.status_code not in (200, 201):
        return None
    return r.json()

def verify_webhook(transmission_id: str, transmission_time: str, cert_url: str, auth_algo: str, transmission_sig: str, webhook_id: str, webhook_event_body: str) -> bool:
    t = _token()
    if not t:
        return False
    payload = {
        "transmission_id": transmission_id,
        "transmission_time": transmission_time,
        "cert_url": cert_url,
        "auth_algo": auth_algo,
        "transmission_sig": transmission_sig,
        "webhook_id": webhook_id,
        "webhook_event": json.loads(webhook_event_body),
    }
    r = requests.post(_base() + "/v1/notifications/verify-webhook-signature", headers={"Authorization": f"Bearer {t}", "Content-Type": "application/json"}, json=payload)
    if r.status_code != 200:
        return False
    return r.json().get("verification_status") == "SUCCESS"
