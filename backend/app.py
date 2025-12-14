from datetime import datetime, date
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
try:
    from astrology import fate_label
    from storage import (
        init_db,
        save_user,
        get_user_label,
        set_push_pref,
        get_push_pref,
        upsert_push,
        get_push,
        set_membership,
        get_membership,
        add_post,
        list_posts,
        like_post,
        get_user_fate,
        register_token,
        get_tokens,
        list_device_tokens,
        delete_token,
        has_stripe_event,
        record_stripe_event,
        has_paypal_event,
        record_paypal_event,
        create_account,
        get_account_by_email,
        set_account_lang,
        get_account_lang,
        set_account_consent,
        get_permissions,
        add_decoration,
        add_glow,
        inc_share_count,
        add_credit,
        get_share_code,
        find_user_by_code,
        record_referral,
        set_referral_paid,
        consume_credit,
        create_short_link,
        get_short_link,
        get_experience_claimed,
        set_experience_claimed,
    )
    from card_elements import elements_for
from .bedrock_client import generate_daily
from .bedrock_client import generate_expanded, generate_free_pack, generate_premium_pack, generate_line_detail
    from fcm import send_tokens, send_tokens_detail
    from payments_stripe import checkout_session, session_paid
    from payments_paypal import (
        create_order as paypal_create_order,
        capture_order as paypal_capture_order,
        verify_webhook as paypal_verify_webhook,
    )
except ImportError:
    from backend.astrology import fate_label
    from backend.storage import (
        init_db,
        save_user,
        get_user_label,
        set_push_pref,
        get_push_pref,
        upsert_push,
        get_push,
        set_membership,
        get_membership,
        add_post,
        list_posts,
        like_post,
        get_user_fate,
        register_token,
        get_tokens,
        list_device_tokens,
        delete_token,
        has_stripe_event,
        record_stripe_event,
        has_paypal_event,
        record_paypal_event,
        create_account,
        get_account_by_email,
        set_account_lang,
        get_account_lang,
        set_account_consent,
        get_permissions,
        add_decoration,
        add_glow,
        inc_share_count,
        add_credit,
        get_share_code,
        find_user_by_code,
        record_referral,
        set_referral_paid,
        consume_credit,
        create_short_link,
        get_short_link,
        get_experience_claimed,
        set_experience_claimed,
    )
    from backend.card_elements import elements_for
    from backend.bedrock_client import generate_daily
    from backend.fcm import send_tokens, send_tokens_detail
    from backend.payments_stripe import checkout_session, session_paid
    from backend.payments_paypal import (
        create_order as paypal_create_order,
        capture_order as paypal_capture_order,
        verify_webhook as paypal_verify_webhook,
    )
import os
import stripe
import logging
import sys
import json
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from .auth import hash_password, verify_password, create_jwt, decode_jwt
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except Exception:
    pass

app = FastAPI()
init_db()
logger = logging.getLogger("stripe")
logging.basicConfig(level=logging.INFO)
k = os.environ.get("STRIPE_SECRET_KEY")
if k:
    stripe.api_key = k

origins_str = os.environ.get("CORS_ORIGINS", "")
origins = [o.strip() for o in origins_str.split(",") if o.strip()] if origins_str else [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalcInput(BaseModel):
    name: str
    birthday: str
    calendar: str = "gregorian"

@app.post("/api/calc")
def calc(input: CalcInput):
    try:
        d = datetime.strptime(input.birthday, "%Y-%m-%d").date()
        if input.calendar and input.calendar != "gregorian":
            try:
                from zhdate import ZhDate
                y,m,day = map(int, input.birthday.split("-"))
                d = ZhDate(y,m,day).to_datetime().date()
            except Exception:
                pass
    except Exception:
        raise HTTPException(status_code=400, detail="invalid birthday")
    s, z, e, label = fate_label(d)
    if not s or not z or not e:
        raise HTTPException(status_code=422, detail="calculation unavailable")
    uid = save_user(input.name, input.birthday, input.calendar, s, z, e, label)
    return {"user_id": uid, "sign": s, "zodiac": z, "element": e, "label": label}

@app.get("/api/label/{user_id}")
def label(user_id: int):
    l = get_user_label(user_id)
    if not l:
        raise HTTPException(status_code=404, detail="not found")
    return {"label": l}

@app.get("/api/card-elements")
def card_elements(sign: str, zodiac: str, element: str):
    return elements_for(sign, zodiac, element)

class PushPref(BaseModel):
    user_id: int
    hour: int
    enabled: bool
    language: str

@app.post("/api/push/prefs")
def set_prefs(pref: PushPref):
    set_push_pref(pref.user_id, pref.hour, pref.enabled, pref.language)
    return {"ok": True}

class PaypalOrder(BaseModel):
    user_id: int
    level: str
    months: int = 1
    return_url: str | None = None
    cancel_url: str | None = None

@app.post("/api/pay/paypal/order")
def paypal_order(po: PaypalOrder):
    base = os.environ.get("PUBLIC_BASE_URL") or "http://localhost:5173/membership"
    ret = po.return_url or base
    can = po.cancel_url or base
    url = paypal_create_order(po.user_id, po.level, po.months, ret, can)
    if not url:
        raise HTTPException(status_code=500, detail="paypal not configured")
    return {"url": url}

@app.get("/api/pay/paypal/capture")
def paypal_capture(order_id: str, user_id: int, level: str, months: int = 1):
    res = paypal_capture_order(order_id)
    if not res:
        raise HTTPException(status_code=402, detail="unpaid")
    from datetime import timedelta
    expires = (datetime.utcnow() + timedelta(days=30 * months)).strftime("%Y-%m-%d")
    set_membership(user_id, level, expires)
    return {"ok": True, "expires_at": expires}

@app.post("/api/pay/paypal/webhook")
async def paypal_webhook(request: Request):
    webhook_id = os.environ.get("PAYPAL_WEBHOOK_ID")
    if not webhook_id:
        raise HTTPException(status_code=500, detail="paypal webhook not configured")
    payload = await request.body()
    tx_id = request.headers.get("paypal-transmission-id", "")
    tx_time = request.headers.get("paypal-transmission-time", "")
    cert_url = request.headers.get("paypal-cert-url", "")
    auth_algo = request.headers.get("paypal-auth-algo", "")
    tx_sig = request.headers.get("paypal-transmission-sig", "")
    ok = paypal_verify_webhook(tx_id, tx_time, cert_url, auth_algo, tx_sig, webhook_id, payload.decode("utf-8"))
    if not ok:
        raise HTTPException(status_code=400, detail="invalid signature")
    event = request.headers.get("paypal-event-id") or ""
    if event and has_paypal_event(event):
        return {"ok": True, "duplicate": True}
    body = json.loads(payload.decode("utf-8"))
    t = body.get("event_type", "")
    if t in ("CHECKOUT.ORDER.APPROVED", "PAYMENT.CAPTURE.COMPLETED"):
        res = body.get("resource", {})
        try:
            custom = res.get("purchase_units", [{}])[0].get("custom_id")
            meta = json.loads(custom) if custom else {}
            user_id = int(str(meta.get("user_id", "0")) or "0")
            level = str(meta.get("level", ""))
            months = int(str(meta.get("months", "1")) or "1")
            if user_id and level:
                from datetime import timedelta
                expires = (datetime.utcnow() + timedelta(days=30 * months)).strftime("%Y-%m-%d")
                set_membership(user_id, level, expires)
        except Exception:
            pass
    if event:
        record_paypal_event(event)
    return {"ok": True}

@app.get("/api/push/prefs/{user_id}")
def get_prefs(user_id: int):
    p = get_push_pref(user_id)
    if not p:
        raise HTTPException(status_code=404, detail="not found")
    return {"hour": p[0], "enabled": p[1], "language": p[2]}

class GeneratePush(BaseModel):
    user_id: int
    day: str
    language: str

@app.post("/api/push/generate")
def generate_push(body: GeneratePush):
    f = get_user_fate(body.user_id)
    if not f:
        raise HTTPException(status_code=404, detail="user fate not found")
    s, z, e = f
    energy, social, decision, relax = generate_daily(s, z, e, body.language)
    upsert_push(body.user_id, body.day, body.language, energy, social, decision, relax)
    return {"ok": True}

@app.get("/api/push/today/{user_id}")
def get_today_push(user_id: int, day: str, language: str):
    p = get_push(user_id, day, language)
    if not p:
        s, z, e, _ = fate_label(date.fromisoformat(day))
        energy, social, decision, relax = generate_daily(s, z, e, language)
        upsert_push(user_id, day, language, energy, social, decision, relax)
        p = (energy, social, decision, relax)
    return {"energy": p[0], "social": p[1], "decision": p[2], "relax": p[3]}

class RegisterToken(BaseModel):
    user_id: int
    token: str
    platform: str = "android"
    language: str = "en"

@app.post("/api/push/token")
def push_token(rt: RegisterToken):
    register_token(rt.user_id, rt.token, rt.platform, rt.language)
    return {"ok": True}

@app.get("/api/push/tokens/{user_id}")
def push_tokens(user_id: int, language: str | None = None):
    return list_device_tokens(user_id, language)

class DeleteToken(BaseModel):
    user_id: int
    token: str

@app.delete("/api/push/token")
def push_token_delete(dt: DeleteToken):
    delete_token(dt.user_id, dt.token)
    return {"ok": True}

class SendPush(BaseModel):
    user_id: int
    day: str
    language: str

@app.post("/api/push/send")
def push_send(sp: SendPush):
    p = get_push(sp.user_id, sp.day, sp.language)
    if not p:
        f = get_user_fate(sp.user_id)
        if not f:
            raise HTTPException(status_code=404, detail="user fate not found")
        s, z, e = f
        energy, social, decision, relax = generate_daily(s, z, e, sp.language)
        upsert_push(sp.user_id, sp.day, sp.language, energy, social, decision, relax)
        p = (energy, social, decision, relax)
    tokens = get_tokens(sp.user_id, sp.language)
    title = {"en": "Today Card", "es": "Tarjeta de Hoy", "fr": "Carte du Jour"}.get(sp.language, "Today Card")
    body = " | ".join([p[0], p[1], p[2], p[3]])
    data = {"day": sp.day}
    ids = send_tokens(tokens, title, body, data)
    return {"sent": len(ids)}

class SendPushDetail(BaseModel):
    user_id: int
    day: str
    language: str

@app.post("/api/push/send-detail")
def push_send_detail(sp: SendPushDetail):
    p = get_push(sp.user_id, sp.day, sp.language)
    if not p:
        f = get_user_fate(sp.user_id)
        if not f:
            raise HTTPException(status_code=404, detail="user fate not found")
        s, z, e = f
        energy, social, decision, relax = generate_daily(s, z, e, sp.language)
        upsert_push(sp.user_id, sp.day, sp.language, energy, social, decision, relax)
        p = (energy, social, decision, relax)
    tokens = get_tokens(sp.user_id, sp.language)
    title = {"en": "Today Card", "es": "Tarjeta de Hoy", "fr": "Carte du Jour"}.get(sp.language, "Today Card")
    body = " | ".join([p[0], p[1], p[2], p[3]])
    data = {"day": sp.day}
    res = send_tokens_detail(tokens, title, body, data)
    try:
        from storage import delete_token
    except Exception:
        from backend.storage import delete_token
    for r in res:
        if not r.get("ok"):
            t = r.get("token")
            if t:
                delete_token(sp.user_id, t)
    sent = sum(1 for r in res if r.get("ok"))
    return {"sent": sent, "results": res}

class BatchTokens(BaseModel):
    user_id: int
    tokens: list[str]
    platform: str = "android"
    language: str = "en"

@app.post("/api/push/tokens")
def push_tokens_batch(bt: BatchTokens):
    for t in bt.tokens:
        register_token(bt.user_id, t, bt.platform, bt.language)
    return {"ok": True, "count": len(bt.tokens)}

class DeleteTokens(BaseModel):
    user_id: int
    tokens: list[str]

@app.delete("/api/push/tokens")
def push_tokens_delete(dt: DeleteTokens):
    for t in dt.tokens:
        delete_token(dt.user_id, t)
    return {"ok": True, "count": len(dt.tokens)}

class SendTokensDetail(BaseModel):
    user_id: int
    day: str
    language: str
    tokens: list[str]

@app.post("/api/push/send-detail-tokens")
def push_send_detail_tokens(st: SendTokensDetail):
    p = get_push(st.user_id, st.day, st.language)
    if not p:
        f = get_user_fate(st.user_id)
        if not f:
            raise HTTPException(status_code=404, detail="user fate not found")
        s, z, e = f
        energy, social, decision, relax = generate_daily(s, z, e, st.language)
        upsert_push(st.user_id, st.day, st.language, energy, social, decision, relax)
        p = (energy, social, decision, relax)
    title = {"en": "Today Card", "es": "Carta de Hoy", "fr": "Carte d'aujourd'hui"}.get(st.language, "Today Card")
    kw = p[0].split(" ")[0]
    guide = {"en":"Tap to explore","es":"Toca para explorar","fr":"Clique pour explorer"}.get(st.language, "Tap to explore")
    body = f"{kw} | {guide}"
    data = {"day": st.day}
    res = send_tokens_detail(st.tokens, title, body, data)
    sent = sum(1 for r in res if r.get("ok"))
    return {"sent": sent, "results": res}

@app.get("/api/bedrock/test")
def bedrock_test(request: Request, sign: str = "白羊座", zodiac: str = "龙", element: str = "木", language: str | None = None):
    lang = language
    if not lang:
        auth = request.headers.get("authorization") or request.headers.get("Authorization") or ""
        if auth.lower().startswith("bearer "):
            tok = auth.split(" ",1)[1]
            p = decode_jwt(tok)
            if p:
                aid = int(p.get("sub", 0))
                try:
                    lang = get_account_lang(aid)
                except Exception:
                    from backend.storage import get_account_lang as gal
                    lang = gal(aid)
    lang = lang or "en"
    e, s, d, r = generate_daily(sign, zodiac, element, lang)
    return {"energy": e, "social": s, "decision": d, "relax": r}

@app.get("/api/card/details")
def card_details(request: Request, sign: str, zodiac: str, element: str, language: str | None = None):
    lang = language
    if not lang:
        auth = request.headers.get("authorization") or request.headers.get("Authorization") or ""
        if auth.lower().startswith("bearer "):
            tok = auth.split(" ",1)[1]
            p = decode_jwt(tok)
            if p:
                aid = int(p.get("sub", 0))
                try:
                    lang = get_account_lang(aid)
                except Exception:
                    from backend.storage import get_account_lang as gal
                    lang = gal(aid)
    lang = lang or "en"
    res = generate_expanded(sign, zodiac, element, lang)
    return res

@app.get("/api/card/free-pack")
def card_free_pack(request: Request, user_id: int, sign: str, zodiac: str, element: str, language: str | None = None):
    lang = language or "en"
    return generate_free_pack(sign, zodiac, element, lang)

@app.get("/api/card/premium-pack")
def card_premium_pack(request: Request, user_id: int, sign: str, zodiac: str, element: str, material: str = "brass", language: str | None = None):
    lang = language or "en"
    return generate_premium_pack(sign, zodiac, element, material, lang)

@app.get("/api/card/line-detail")
def card_line_detail(request: Request, sign: str, zodiac: str, element: str, line_type: str, language: str | None = None):
    lang = language
    if not lang:
        auth = request.headers.get("authorization") or request.headers.get("Authorization") or ""
        if auth.lower().startswith("bearer "):
            tok = auth.split(" ",1)[1]
            p = decode_jwt(tok)
            if p:
                aid = int(p.get("sub", 0))
                try:
                    lang = get_account_lang(aid)
                except Exception:
                    from backend.storage import get_account_lang as gal
                    lang = gal(aid)
    lang = lang or "en"
    return generate_line_detail(sign, zodiac, element, lang, line_type)

class ShareSuccess(BaseModel):
    user_id: int
    language: str = "en"

@app.post("/api/share/success")
def share_success(body: ShareSuccess):
    names = ["Starlight Texture", "Vine Dark", "Waterdrop Spark"]
    sc = inc_share_count(body.user_id)
    name = names[sc % len(names)]
    add_decoration(body.user_id, name)
    m = get_membership(body.user_id)
    if m and str(m[0]).lower() != "free":
        glow = ["Nebula Light", "Crystal Glow", "Flame Pulse"][sc % 3]
        add_glow(body.user_id, glow)
    perms = get_permissions(body.user_id)
    msg = {
        "en": f"You unlocked {name}!",
        "es": f"¡Desbloqueaste {name}!",
        "fr": f"Tu as débloqué {name} !",
        "de": f"Du hast {name} freigeschaltet!",
        "it": f"Hai sbloccato {name}!",
        "pt": f"Você desbloqueou {name}!",
        "ru": f"Ты разблокировал {name}!",
    }.get(body.language, f"You unlocked {name}!")
    return {"unlocked": {"type": "decoration", "name": name}, "share_count": perms["share_count"], "message": msg}

@app.get("/api/share/code/{user_id}")
def share_code(user_id: int):
    code = get_share_code(user_id)
    return {"code": code}

class ShareReferral(BaseModel):
    inviter_code: str
    new_user_id: int
    language: str = "en"

@app.post("/api/share/referral")
def share_referral(body: ShareReferral):
    inviter = find_user_by_code(body.inviter_code)
    if not inviter:
        raise HTTPException(status_code=404, detail="inviter not found")
    record_referral(inviter, body.new_user_id, 0)
    from datetime import timedelta
    expires = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d")
    set_membership(inviter, "Premium", expires)
    add_credit(body.new_user_id, 1)
    msg = {
        "en": "Referral success: 7-day Premium for inviter, 1 free premium card for new user",
        "es": "Referencia exitosa: 7 días Premium para quien invita y 1 carta premium gratis para el nuevo usuario",
        "fr": "Parrainage réussi : 7 jours Premium pour l'invitant et 1 carte premium gratuite pour le nouveau membre",
    }.get(body.language, "Referral success")
    return {"ok": True, "message": msg}

class ShareReferralPaid(BaseModel):
    inviter_code: str
    purchaser_user_id: int
    language: str = "en"

@app.post("/api/share/referral-paid")
def share_referral_paid(body: ShareReferralPaid):
    inviter = find_user_by_code(body.inviter_code)
    if not inviter:
        raise HTTPException(status_code=404, detail="inviter not found")
    set_referral_paid(inviter, body.purchaser_user_id)
    glow = ["Nebula Light", "Crystal Glow", "Flame Pulse"][0]
    add_glow(inviter, glow)
    msg = {
        "en": f"Premium conversion confirmed. {glow} unlocked",
        "de": f"Premium bestätigt. {glow} dauerhaft freigeschaltet",
        "ru": f"Premium подтверждён. {glow} разблокирован",
    }.get(body.language, "Premium conversion confirmed")
    return {"unlocked": {"type": "glow", "name": glow}, "ok": True, "message": msg}

class ConsumeCredit(BaseModel):
    user_id: int

@app.post("/api/share/consume-credit")
def share_consume_credit(body: ConsumeCredit):
    left = consume_credit(body.user_id)
    if left < 0:
        left = 0
    granted = left >= 0
    return {"premium_once": granted, "credits_left": left}

class ShortenInput(BaseModel):
    sign: str
    zodiac: str
    element: str
    language: str = "en"

@app.post("/api/share/shorten")
def share_shorten(body: ShortenInput):
    base = os.environ.get("PUBLIC_BASE_URL") or "http://localhost:5173"
    long_url = f"{base}/card?sign={body.sign}&zodiac={body.zodiac}&element={body.element}"
    code = create_short_link(body.sign, body.zodiac, body.element, long_url, body.language)
    short_url = f"{base}/s/{code}"
    return {"code": code, "short_url": short_url, "long_url": long_url}

@app.get("/s/{code}")
def share_og_page(code: str):
    rec = get_short_link(code)
    if not rec:
        raise HTTPException(status_code=404, detail="not found")
    long_url, sign, zodiac, element, lang = rec
    base = os.environ.get("PUBLIC_BASE_URL") or "http://localhost:5173"
    def _base_lang(l: str) -> str:
        l = (l or "en").lower()
        if l.startswith("es"): return "es"
        if l.startswith("fr"): return "fr"
        if l.startswith("de"): return "de"
        if l.startswith("it"): return "it"
        if l.startswith("pt"): return "pt"
        if l.startswith("ru"): return "ru"
        return "en"
    L = _base_lang(lang)
    SIGN = {
        '白羊座': {'en':'Aries','es':'Aries','fr':'Bélier','de':'Widder','it':'Ariete','pt':'Áries','ru':'Овен'},
        '金牛座': {'en':'Taurus','es':'Tauro','fr':'Taureau','de':'Stier','it':'Toro','pt':'Touro','ru':'Телец'},
        '双子座': {'en':'Gemini','es':'Géminis','fr':'Gémeaux','de':'Zwillinge','it':'Gemelli','pt':'Gêmeos','ru':'Близнецы'},
        '巨蟹座': {'en':'Cancer','es':'Cáncer','fr':'Cancer','de':'Krebs','it':'Cancro','pt':'Câncer','ru':'Рак'},
        '狮子座': {'en':'Leo','es':'Leo','fr':'Lion','de':'Löwe','it':'Leone','pt':'Leão','ru':'Лев'},
        '处女座': {'en':'Virgo','es':'Virgo','fr':'Vierge','de':'Jungfrau','it':'Vergine','pt':'Virgem','ru':'Дева'},
        '天秤座': {'en':'Libra','es':'Libra','fr':'Balance','de':'Waage','it':'Bilancia','pt':'Libra','ru':'Весы'},
        '天蝎座': {'en':'Scorpio','es':'Escorpio','fr':'Scorpion','de':'Skorpion','it':'Scorpione','pt':'Escorpião','ru':'Скорпион'},
        '射手座': {'en':'Sagittarius','es':'Sagitario','fr':'Sagittaire','de':'Schütze','it':'Sagittario','pt':'Sagitário','ru':'Стрелец'},
        '摩羯座': {'en':'Capricorn','es':'Capricornio','fr':'Capricorne','de':'Steinbock','it':'Capricorno','pt':'Capricórnio','ru':'Козерог'},
        '水瓶座': {'en':'Aquarius','es':'Acuario','fr':'Verseau','de':'Wassermann','it':'Acquario','pt':'Aquário','ru':'Водолей'},
        '双鱼座': {'en':'Pisces','es':'Piscis','fr':'Poissons','de':'Fische','it':'Pesci','pt':'Peixes','ru':'Рыбы'},
    }
    ZOD = {
        '鼠': {'en':'Rat','es':'Rata','fr':'Rat','de':'Ratte','it':'Topo','pt':'Rato','ru':'Крыса'},
        '牛': {'en':'Ox','es':'Buey','fr':'Bœuf','de':'Ochse','it':'Bue','pt':'Boi','ru':'Бык'},
        '虎': {'en':'Tiger','es':'Tigre','fr':'Tigre','de':'Tiger','it':'Tigre','pt':'Tigre','ru':'Тигр'},
        '兔': {'en':'Rabbit','es':'Conejo','fr':'Lapin','de':'Hase','it':'Coniglio','pt':'Coelho','ru':'Кролик'},
        '龙': {'en':'Dragon','es':'Dragón','fr':'Dragon','de':'Drache','it':'Drago','pt':'Dragão','ru':'Дракон'},
        '蛇': {'en':'Snake','es':'Serpiente','fr':'Serpent','de':'Schlange','it':'Serpente','pt':'Serpente','ru':'Змея'},
        '马': {'en':'Horse','es':'Caballo','fr':'Cheval','de':'Pferd','it':'Cavallo','pt':'Cavalo','ru':'Лошадь'},
        '羊': {'en':'Goat','es':'Cabra','fr':'Chèvre','de':'Ziege','it':'Capra','pt':'Cabra','ru':'Коза'},
        '猴': {'en':'Monkey','es':'Mono','fr':'Singe','de':'Affe','it':'Scimmia','pt':'Macaco','ru':'Обезьяна'},
        '鸡': {'en':'Rooster','es':'Gallo','fr':'Coq','de':'Hahn','it':'Gallo','pt':'Galo','ru':'Петух'},
        '狗': {'en':'Dog','es':'Perro','fr':'Chien','de':'Hund','it':'Cane','pt':'Cão','ru':'Собака'},
        '猪': {'en':'Pig','es':'Cerdo','fr':'Cochon','de':'Schwein','it':'Maiale','pt':'Porco','ru':'Свинья'},
    }
    ELEM = {
        '木': {'en':'Wood','es':'Madera','fr':'Bois','de':'Holz','it':'Legno','pt':'Madeira','ru':'Древесная'},
        '火': {'en':'Fire','es':'Fuego','fr':'Feu','de':'Feuer','it':'Fuoco','pt':'Fogo','ru':'Огненная'},
        '土': {'en':'Earth','es':'Tierra','fr':'Terre','de':'Erde','it':'Terra','pt':'Terra','ru':'Земная'},
        '金': {'en':'Metal','es':'Metal','fr':'Métal','de':'Metall','it':'Metallo','pt':'Metal','ru':'Металлическая'},
        '水': {'en':'Water','es':'Agua','fr':'Eau','de':'Wasser','it':'Acqua','pt':'Água','ru':'Водная'},
    }
    signL = SIGN.get(sign, {}).get(L, sign)
    zodiacL = ZOD.get(zodiac, {}).get(L, zodiac)
    elemL = ELEM.get(element, {}).get(L, element)
    title = {
        'en': f"Cosmic Card — {signL}/{zodiacL}",
        'es': f"Tarjeta Cósmica — {signL}/{zodiacL}",
        'fr': f"Carte Cosmique — {signL}/{zodiacL}",
        'de': f"Kosmische Karte — {signL}/{zodiacL}",
        'it': f"Carta Cosmica — {signL}/{zodiacL}",
        'pt': f"Carta Cósmica — {signL}/{zodiacL}",
        'ru': f"Космическая Карта — {signL}/{zodiacL}",
    }.get(L, f"Cosmic Card — {signL}/{zodiacL}")
    desc = {
        'en': f"Discover {elemL} energy for {signL}/{zodiacL}",
        'es': f"Descubre la energía de {elemL} para {signL}/{zodiacL}",
        'fr': f"Découvre l'énergie {elemL} pour {signL}/{zodiacL}",
        'de': f"Entdecke {elemL}-Energie für {signL}/{zodiacL}",
        'it': f"Scopri l'energia {elemL} per {signL}/{zodiacL}",
        'pt': f"Descubra a energia de {elemL} para {signL}/{zodiacL}",
        'ru': f"Открой энергию {elemL} для {signL}/{zodiacL}",
    }.get(L, f"Discover {elemL} energy for {signL}/{zodiacL}")
    img = f"{base}/api/share/og-image?sign={sign}&zodiac={zodiac}&element={element}&lang={L}"
    html = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title}</title>
  <link rel="canonical" href="{long_url}"/>
  <meta property="og:type" content="website"/>
  <meta property="og:title" content="{title}"/>
  <meta property="og:description" content="{desc}"/>
  <meta property="og:url" content="{long_url}"/>
  <meta property="og:image" content="{img}"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{title}"/>
  <meta name="twitter:description" content="{desc}"/>
  <meta name="twitter:image" content="{img}"/>
</head>
<body>
  <p>Redirecting...</p>
  <script>setTimeout(function(){ location.href = {json.dumps(long_url)} }, 500)</script>
</body>
</html>
"""
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html, status_code=200)

@app.get("/api/share/og-image")
def share_og_image(sign: str, zodiac: str, element: str, lang: str = "en"):
    palette = {
        "木": ("#0b3d2e", "#1fa36b"),
        "火": ("#3d0b0b", "#ff6b3d"),
        "土": ("#372c1a", "#c2a36b"),
        "金": ("#3a330f", "#ffd166"),
        "水": ("#0b2e3d", "#6ec1ff"),
    }.get(element, ("#0b3d2e", "#1fa36b"))
    symbol = {
        '白羊座': '♈','金牛座':'♉','双子座':'♊','巨蟹座':'♋','狮子座':'♌','处女座':'♍',
        '天秤座':'♎','天蝎座':'♏','射手座':'♐','摩羯座':'♑','水瓶座':'♒','双鱼座':'♓'
    }.get(sign, '★')
    def _base_lang(l: str) -> str:
        l = (l or "en").lower()
        if l.startswith("es"): return "es"
        if l.startswith("fr"): return "fr"
        if l.startswith("de"): return "de"
        if l.startswith("it"): return "it"
        if l.startswith("pt"): return "pt"
        if l.startswith("ru"): return "ru"
        return "en"
    L = _base_lang(lang)
    SIGN = {
        '白羊座': {'en':'Aries','es':'Aries','fr':'Bélier','de':'Widder','it':'Ariete','pt':'Áries','ru':'Овен'},
        '金牛座': {'en':'Taurus','es':'Tauro','fr':'Taureau','de':'Stier','it':'Toro','pt':'Touro','ru':'Телец'},
        '双子座': {'en':'Gemini','es':'Géminis','fr':'Gémeaux','de':'Zwillinge','it':'Gemelli','pt':'Gêmeos','ru':'Близнецы'},
        '巨蟹座': {'en':'Cancer','es':'Cáncer','fr':'Cancer','de':'Krebs','it':'Cancro','pt':'Câncer','ru':'Рак'},
        '狮子座': {'en':'Leo','es':'Leo','fr':'Lion','de':'Löwe','it':'Leone','pt':'Leão','ru':'Лев'},
        '处女座': {'en':'Virgo','es':'Virgo','fr':'Vierge','de':'Jungfrau','it':'Vergine','pt':'Virgem','ru':'Дева'},
        '天秤座': {'en':'Libra','es':'Libra','fr':'Balance','de':'Waage','it':'Bilancia','pt':'Libra','ru':'Весы'},
        '天蝎座': {'en':'Scorpio','es':'Escorpio','fr':'Scorpion','de':'Skorpion','it':'Scorpione','pt':'Escorpião','ru':'Скорпион'},
        '射手座': {'en':'Sagittarius','es':'Sagitario','fr':'Sagittaire','de':'Schütze','it':'Sagittario','pt':'Sagitário','ru':'Стрелец'},
        '摩羯座': {'en':'Capricorn','es':'Capricornio','fr':'Capricorne','de':'Steinbock','it':'Capricorno','pt':'Capricórnio','ru':'Козерог'},
        '水瓶座': {'en':'Aquarius','es':'Acuario','fr':'Verseau','de':'Wassermann','it':'Acquario','pt':'Aquário','ru':'Водолей'},
        '双鱼座': {'en':'Pisces','es':'Piscis','fr':'Poissons','de':'Fische','it':'Pesci','pt':'Peixes','ru':'Рыбы'},
    }
    ZOD = {
        '鼠': {'en':'Rat','es':'Rata','fr':'Rat','de':'Ratte','it':'Topo','pt':'Rato','ru':'Крыса'},
        '牛': {'en':'Ox','es':'Buey','fr':'Bœuf','de':'Ochse','it':'Bue','pt':'Boi','ru':'Бык'},
        '虎': {'en':'Tiger','es':'Tigre','fr':'Tigre','de':'Tiger','it':'Tigre','pt':'Tigre','ru':'Тигр'},
        '兔': {'en':'Rabbit','es':'Conejo','fr':'Lapin','de':'Hase','it':'Coniglio','pt':'Coelho','ru':'Кролик'},
        '龙': {'en':'Dragon','es':'Dragón','fr':'Dragon','de':'Drache','it':'Drago','pt':'Dragão','ru':'Дракон'},
        '蛇': {'en':'Snake','es':'Serpiente','fr':'Serpent','de':'Schlange','it':'Serpente','pt':'Serpente','ru':'Змея'},
        '马': {'en':'Horse','es':'Caballo','fr':'Cheval','de':'Pferd','it':'Cavallo','pt':'Cavalo','ru':'Лошадь'},
        '羊': {'en':'Goat','es':'Cabra','fr':'Chèvre','de':'Ziege','it':'Capra','pt':'Cabra','ru':'Коза'},
        '猴': {'en':'Monkey','es':'Mono','fr':'Singe','de':'Affe','it':'Scimmia','pt':'Macaco','ru':'Обезьяна'},
        '鸡': {'en':'Rooster','es':'Gallo','fr':'Coq','de':'Hahn','it':'Gallo','pt':'Galo','ru':'Петух'},
        '狗': {'en':'Dog','es':'Perro','fr':'Chien','de':'Hund','it':'Cane','pt':'Cão','ru':'Собака'},
        '猪': {'en':'Pig','es':'Cerdo','fr':'Cochon','de':'Schwein','it':'Maiale','pt':'Porco','ru':'Свинья'},
    }
    signL = SIGN.get(sign, {}).get(L, sign)
    zodiacL = ZOD.get(zodiac, {}).get(L, zodiac)
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{palette[0]}"/>
      <stop offset="100%" stop-color="{palette[1]}"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#g)"/>
  <text x="600" y="300" text-anchor="middle" font-family="serif" font-size="180" fill="#d4af37">{symbol}</text>
  <text x="600" y="460" text-anchor="middle" font-family="sans-serif" font-size="48" fill="#ffffff">{zodiacL} · {signL}</text>
</svg>
"""
    from fastapi.responses import Response
    return Response(content=svg, media_type="image/svg+xml")

class MembershipShare(BaseModel):
    user_id: int
    language: str = "en"

@app.post("/api/share/membership-share")
def share_membership(body: MembershipShare):
    m = get_membership(body.user_id)
    if m and str(m[0]).lower() != "free":
        return {"ok": False, "message": "already premium"}
    if get_experience_claimed(body.user_id):
        return {"ok": False, "message": "claimed"}
    from datetime import timedelta
    expires = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d")
    set_membership(body.user_id, "Premium", expires)
    set_experience_claimed(body.user_id)
    msg = {
        "en": "7-day Premium experience granted",
        "es": "Se otorgó experiencia Premium de 7 días",
        "fr": "Expérience Premium de 7 jours accordée",
    }.get(body.language, "7-day Premium experience granted")
    return {"ok": True, "expires_at": expires, "message": msg}

@app.get("/api/share/permissions/{user_id}")
def share_permissions(user_id: int):
    return get_permissions(user_id)

@app.get("/api/user/fate/{user_id}")
def user_fate(user_id: int):
    f = get_user_fate(user_id)
    if not f:
        raise HTTPException(status_code=404, detail="user fate not found")
    s, z, e = f
    return {"sign": s, "zodiac": z, "element": e}

@app.get("/api/health")
def health():
    return {
        "stripe_key": bool(os.environ.get("STRIPE_SECRET_KEY")),
        "webhook_secret": bool(os.environ.get("STRIPE_WEBHOOK_SECRET")),
        "public_base_url": os.environ.get("PUBLIC_BASE_URL") or "",
        "aws_region": os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "",
        "fcm_credentials": bool(os.environ.get("FCM_CREDENTIALS_PATH") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")),
    }

@app.get("/api/membership/status/{user_id}")
def membership_status(user_id: int):
    try:
        from storage import get_membership_status
    except Exception:
        from backend.storage import get_membership_status
    s = get_membership_status(user_id)
    return {"status": s or "active"}

@app.post("/api/pay/stripe/webhook")
async def stripe_webhook(request: Request):
    secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="stripe webhook not configured")
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig, secret)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid signature")
    eid = event.get("id")
    if eid and has_stripe_event(eid):
        logger.info(f"duplicate webhook {eid}")
        return {"ok": True, "duplicate": True}
    t = event.get("type")
    if t == "checkout.session.completed":
        obj = event.get("data", {}).get("object", {})
        md = obj.get("metadata") or {}
        user_id = int(str(md.get("user_id", "0")) or "0")
        level = str(md.get("level", ""))
        months = int(str(md.get("months", "1")) or "1")
        from datetime import timedelta
        expires = (datetime.utcnow() + timedelta(days=30 * months)).strftime("%Y-%m-%d")
        if user_id and level:
            set_membership(user_id, level, expires)
            logger.info(f"membership updated user={user_id} level={level} expires={expires}")
        cust = obj.get("customer")
        if user_id and cust:
            try:
                from storage import record_stripe_customer
            except Exception:
                from backend.storage import record_stripe_customer
            record_stripe_customer(user_id, cust)
    elif t == "invoice.payment_succeeded":
        obj = event.get("data", {}).get("object", {})
        cust = obj.get("customer")
        sub_id = obj.get("subscription")
        try:
            from storage import get_user_by_customer
        except Exception:
            from backend.storage import get_user_by_customer
        uid = get_user_by_customer(cust) if cust else None
        if sub_id:
            try:
                sub = stripe.Subscription.retrieve(sub_id)
                meta = sub.get("metadata") or {}
                user_id = uid or int(str(meta.get("user_id", "0")) or "0")
                level = str(meta.get("level", ""))
                months = int(str(meta.get("months", "1")) or "1")
                cpe = sub.get("current_period_end")
                if user_id and level and cpe:
                    exp = datetime.utcfromtimestamp(int(cpe)).strftime("%Y-%m-%d")
                    set_membership(user_id, level, exp)
                    try:
                        from storage import set_membership_status
                    except Exception:
                        from backend.storage import set_membership_status
                    set_membership_status(user_id, "active")
            except Exception:
                pass
    elif t == "invoice.payment_failed":
        obj = event.get("data", {}).get("object", {})
        cust = obj.get("customer")
        try:
            from storage import get_user_by_customer, set_membership_status
        except Exception:
            from backend.storage import get_user_by_customer, set_membership_status
        uid = get_user_by_customer(cust) if cust else None
        if uid:
            set_membership_status(uid, "past_due")
    elif t == "customer.subscription.updated":
        obj = event.get("data", {}).get("object", {})
        meta = obj.get("metadata") or {}
        status = obj.get("status")
        cust = obj.get("customer")
        try:
            from storage import get_user_by_customer
        except Exception:
            from backend.storage import get_user_by_customer
        user_id = int(str(meta.get("user_id", "0")) or "0") or (get_user_by_customer(cust) or 0)
        level = str(meta.get("level", ""))
        months = int(str(meta.get("months", "1")) or "1")
        cpe = obj.get("current_period_end")
        if status == "active" and user_id and level and cpe:
            exp = datetime.utcfromtimestamp(int(cpe)).strftime("%Y-%m-%d")
            set_membership(user_id, level, exp)
            try:
                from storage import set_membership_status
            except Exception:
                from backend.storage import set_membership_status
            set_membership_status(user_id, "active")
        if status in ("canceled", "unpaid", "past_due") and user_id:
            try:
                from storage import set_membership_status
            except Exception:
                from backend.storage import set_membership_status
            set_membership_status(user_id, status)
    if eid:
        record_stripe_event(eid)
    return {"ok": True}

class Upgrade(BaseModel):
    user_id: int
    level: str
    months: int = 1

@app.post("/api/membership/upgrade")
def upgrade(body: Upgrade):
    from datetime import timedelta
    expires = (datetime.utcnow() + timedelta(days=30 * body.months)).strftime("%Y-%m-%d")
    set_membership(body.user_id, body.level, expires)
    return {"ok": True, "expires_at": expires}

@app.get("/api/membership/{user_id}")
def membership(user_id: int):
    m = get_membership(user_id)
    if not m:
        try:
            from storage import get_membership_status
        except Exception:
            from backend.storage import get_membership_status
        s = get_membership_status(user_id) or "free"
        return {"level": "free", "status": s}
    try:
        from storage import get_membership_status
    except Exception:
        from backend.storage import get_membership_status
    from datetime import date as _d
    level, exp = m[0], m[1]
    try:
        exd = _d.fromisoformat(exp) if exp else None
    except Exception:
        exd = None
    if exd and exd < _d.today():
        return {"level": "free", "expires_at": exp, "status": "expired"}
    s = get_membership_status(user_id) or "active"
    return {"level": level, "expires_at": exp, "status": s}

class NewPost(BaseModel):
    user_id: int
    sign: str
    zodiac: str
    language: str
    content: str

class StripeCheckout(BaseModel):
    user_id: int
    level: str
    months: int = 1
    success_base: str | None = None
    cancel_url: str | None = None
    price_id: str | None = None

@app.post("/api/pay/stripe/checkout")
def stripe_checkout(sc: StripeCheckout):
    try:
        url = checkout_session(sc.user_id, sc.level, sc.months, sc.success_base, sc.cancel_url, sc.price_id)
        if not url:
            raise HTTPException(status_code=500, detail="stripe not configured")
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class ReminderRun(BaseModel):
    days: int = 3
    language: str | None = None

@app.post("/api/membership/reminders/run")
def reminders_run(rr: ReminderRun):
    try:
        from storage import list_memberships_expiring
    except Exception:
        from backend.storage import list_memberships_expiring
    items = list_memberships_expiring(rr.days)
    sent_total = 0
    for it in items:
        toks = get_tokens(it["user_id"], rr.language) if rr.language else get_tokens(it["user_id"])  # type: ignore
        title = "Membership expiring soon"
        body = f"Expires at {it['expires_at']}"
        data = {"type": "membership_reminder", "expires_at": it["expires_at"], "level": it["level"]}
        ids = send_tokens(toks, title, body, data)
        sent_total += len(ids)
    return {"items": len(items), "sent": sent_total}

class LangPref(BaseModel):
    lang: str

@app.post("/api/profile/lang")
def profile_lang_set(body: LangPref, request: Request):
    auth = request.headers.get("authorization") or request.headers.get("Authorization") or ""
    if not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="unauthorized")
    tok = auth.split(" ",1)[1]
    p = decode_jwt(tok)
    if not p:
        raise HTTPException(status_code=401, detail="unauthorized")
    aid = int(p.get("sub", 0))
    set_account_lang(aid, body.lang)
    return {"ok": True}

@app.get("/api/profile/lang")
def profile_lang_get(request: Request):
    auth = request.headers.get("authorization") or request.headers.get("Authorization") or ""
    if not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="unauthorized")
    tok = auth.split(" ",1)[1]
    p = decode_jwt(tok)
    if not p:
        raise HTTPException(status_code=401, detail="unauthorized")
    aid = int(p.get("sub", 0))
    lang = get_account_lang(aid) or "en"
    return {"lang": lang}

class ConsentPref(BaseModel):
    consent: bool

@app.post("/api/profile/consent")
def profile_consent_set(body: ConsentPref, request: Request):
    auth = request.headers.get("authorization") or request.headers.get("Authorization") or ""
    if not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="unauthorized")
    tok = auth.split(" ",1)[1]
    p = decode_jwt(tok)
    if not p:
        raise HTTPException(status_code=401, detail="unauthorized")
    aid = int(p.get("sub", 0))
    set_account_consent(aid, bool(body.consent))
    return {"ok": True}

@app.get("/api/pay/stripe/confirm")
def stripe_confirm(session_id: str, user_id: int, level: str, months: int = 1):
    if not session_paid(session_id):
        raise HTTPException(status_code=402, detail="unpaid")
    from datetime import timedelta
    expires = (datetime.utcnow() + timedelta(days=30 * months)).strftime("%Y-%m-%d")
    set_membership(user_id, level, expires)
    return {"ok": True, "expires_at": expires}

def _bad(content: str, language: str) -> bool:
    bad = {
        "en": ["badword"],
        "es": ["malapalabra"],
        "fr": ["grosmot"],
    }.get(language, [])
    lc = content.lower()
    return any(w in lc for w in bad)

@app.post("/api/community/post")
def post(np: NewPost):
    if len(np.content) > 100:
        raise HTTPException(status_code=400, detail="too long")
    if _bad(np.content, np.language):
        raise HTTPException(status_code=400, detail="banned")
    pid = add_post(np.user_id, np.sign, np.zodiac, np.language, np.content)
    return {"id": pid}

@app.get("/api/community/list")
def posts(sign: str | None = None, zodiac: str | None = None, language: str = "en", offset: int = 0, limit: int = 50):
    return list_posts(sign, zodiac, language, limit, offset)

@app.post("/api/community/like/{post_id}")
def like(post_id: int):
    like_post(post_id)
    return {"ok": True}
class RegisterInput(BaseModel):
    email: str
    password: str

class LoginInput(BaseModel):
    email: str
    password: str

@app.post("/api/auth/register")
def auth_register(body: RegisterInput):
    try:
        q = get_account_by_email(body.email)
        if q:
            raise HTTPException(status_code=409, detail="exists")
        aid = create_account(body.email, hash_password(body.password))
        tok = create_jwt(aid)
        return {"token": tok}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="error")

@app.post("/api/auth/login")
def auth_login(body: LoginInput):
    q = get_account_by_email(body.email)
    if not q:
        raise HTTPException(status_code=401, detail="invalid")
    aid, ph = q
    if not verify_password(body.password, ph):
        raise HTTPException(status_code=401, detail="invalid")
    tok = create_jwt(aid)
    return {"token": tok}

class GoogleOAuth(BaseModel):
    id_token: str

@app.post("/api/auth/oauth/google")
def auth_oauth_google(body: GoogleOAuth):
    import urllib.request, urllib.parse, json as _json
    try:
        q = urllib.parse.urlencode({"id_token": body.id_token})
        url = f"https://oauth2.googleapis.com/tokeninfo?{q}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = _json.loads(resp.read().decode("utf-8"))
        email = data.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="invalid google token")
        acc = get_account_by_email(email)
        if not acc:
            aid = create_account(email, hash_password("oauth-google"))
        else:
            aid = acc[0]
        tok = create_jwt(aid)
        return {"token": tok}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="invalid google token")

class AppleOAuth(BaseModel):
    id_token: str

@app.post("/api/auth/oauth/apple")
def auth_oauth_apple(body: AppleOAuth):
    import base64, json as _json
    try:
        parts = body.id_token.split('.')
        if len(parts) < 2:
            raise HTTPException(status_code=401, detail="invalid apple token")
        payload = parts[1] + '=='
        data = _json.loads(base64.urlsafe_b64decode(payload.encode('utf-8')).decode('utf-8'))
        email = data.get("email") or f"apple_{data.get('sub','')}@example.com"
        acc = get_account_by_email(email)
        if not acc:
            aid = create_account(email, hash_password("oauth-apple"))
        else:
            aid = acc[0]
        tok = create_jwt(aid)
        return {"token": tok}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="invalid apple token")

@app.get("/api/auth/me")
def auth_me(request: Request):
    auth = request.headers.get("authorization") or request.headers.get("Authorization") or ""
    if not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="unauthorized")
    tok = auth.split(" ",1)[1]
    p = decode_jwt(tok)
    if not p:
        raise HTTPException(status_code=401, detail="unauthorized")
    return {"account_id": int(p.get("sub", 0))}
@app.get("/api/auth/check")
def auth_check(email: str):
    q = get_account_by_email(email)
    return {"exists": bool(q)}
