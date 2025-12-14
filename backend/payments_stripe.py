import os
import stripe

def _init():
    k = os.environ.get("STRIPE_SECRET_KEY")
    if not k:
        return False
    stripe.api_key = k
    return True

def checkout_session(user_id: int, level: str, months: int, success_base: str | None, cancel_url: str | None, price_id: str | None = None) -> str:
    if not _init():
        return ""
    base = success_base or os.environ.get("PUBLIC_BASE_URL") or "http://localhost:5173/membership"
    cancel = cancel_url or os.environ.get("PUBLIC_BASE_URL") or "http://localhost:5173/membership"
    line_items = None
    mode = "payment"
    if price_id:
        line_items = [{"price": price_id, "quantity": 1}]
        try:
            pr = stripe.Price.retrieve(price_id)
            if pr.get("type") == "recurring" or pr.get("recurring"):
                mode = "subscription"
        except Exception:
            pass
    else:
        env_map = {
            "Premium": os.environ.get("STRIPE_PRICE_PREMIUM"),
            "VIP": os.environ.get("STRIPE_PRICE_VIP"),
        }
        pid = env_map.get(level)
        if pid:
            line_items = [{"price": pid, "quantity": 1}]
            try:
                pr = stripe.Price.retrieve(pid)
                if pr.get("type") == "recurring" or pr.get("recurring"):
                    mode = "subscription"
            except Exception:
                pass
        else:
            price = 499 if level == "Premium" else 999
            amount = price * months
            line_items = [{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": f"{level} Membership"},
                    "unit_amount": amount,
                },
                "quantity": 1,
            }]
    params = {
        "mode": mode,
        "payment_method_types": ["card"],
        "line_items": line_items,
        "metadata": {"user_id": str(user_id), "level": level, "months": str(months)},
        "success_url": f"{base}?session_id={{CHECKOUT_SESSION_ID}}&user_id={user_id}&level={level}&months={months}",
        "cancel_url": cancel,
    }
    if mode == "subscription":
        params["subscription_data"] = {"metadata": {"user_id": str(user_id), "level": level, "months": str(months)}}
    s = stripe.checkout.Session.create(**params)
    return s.url

def session_paid(session_id: str) -> bool:
    if not _init():
        return False
    s = stripe.checkout.Session.retrieve(session_id)
    return s.get("payment_status") == "paid"
