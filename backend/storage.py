import sqlite3
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

DB_PATH = Path(__file__).parent / "data.db"

def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            birthday TEXT,
            calendar TEXT,
            sign TEXT,
            zodiac TEXT,
            element TEXT,
            label TEXT,
            updated_at TEXT
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT,
            created_at TEXT
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS account_prefs (
            account_id INTEGER PRIMARY KEY,
            lang TEXT,
            consent INTEGER
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS push_prefs (
            user_id INTEGER PRIMARY KEY,
            hour INTEGER,
            enabled INTEGER,
            language TEXT
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS pushes (
            user_id INTEGER,
            day TEXT,
            language TEXT,
            energy TEXT,
            social TEXT,
            decision TEXT,
            relax TEXT,
            PRIMARY KEY(user_id, day, language)
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS memberships (
            user_id INTEGER PRIMARY KEY,
            level TEXT,
            expires_at TEXT
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            sign TEXT,
            zodiac TEXT,
            language TEXT,
            content TEXT,
            likes INTEGER DEFAULT 0,
            created_at TEXT
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS device_tokens (
            user_id INTEGER,
            token TEXT,
            platform TEXT,
            language TEXT,
            PRIMARY KEY(user_id, token)
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS stripe_events (
            event_id TEXT PRIMARY KEY,
            created_at TEXT
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS paypal_events (
            event_id TEXT PRIMARY KEY,
            created_at TEXT
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS stripe_customers (
            user_id INTEGER PRIMARY KEY,
            customer_id TEXT UNIQUE
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS share_experience (
            user_id INTEGER PRIMARY KEY,
            claimed INTEGER DEFAULT 0
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS membership_flags (
            user_id INTEGER PRIMARY KEY,
            status TEXT
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS user_card_permission (
            user_id INTEGER PRIMARY KEY,
            decorations TEXT,
            glow TEXT,
            credits INTEGER DEFAULT 0,
            share_count INTEGER DEFAULT 0,
            report_unlocked INTEGER DEFAULT 0
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS share_codes (
            user_id INTEGER PRIMARY KEY,
            code TEXT UNIQUE
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS referrals (
            inviter_user_id INTEGER,
            new_user_id INTEGER,
            paid INTEGER DEFAULT 0,
            created_at TEXT,
            PRIMARY KEY(inviter_user_id, new_user_id)
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS short_links (
            code TEXT PRIMARY KEY,
            long_url TEXT,
            sign TEXT,
            zodiac TEXT,
            element TEXT,
            lang TEXT,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def save_user(name: str, birthday: str, calendar: str, sign: str, zodiac: str, element: str, label: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO users(name,birthday,calendar,sign,zodiac,element,label,updated_at) VALUES(?,?,?,?,?,?,?,datetime('now'))",
        (name, birthday, calendar, sign, zodiac, element, label),
    )
    uid = c.lastrowid
    conn.commit()
    conn.close()
    return uid

def get_user_label(user_id: int) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT label FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return row[0]

def create_account(email: str, password_hash: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO accounts(email,password_hash,created_at) VALUES(?,?,datetime('now'))",
        (email, password_hash),
    )
    aid = c.lastrowid
    conn.commit()
    conn.close()
    return aid

def get_account_by_email(email: str) -> Optional[Tuple[int, str]]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id,password_hash FROM accounts WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return row[0], row[1]

def set_account_lang(account_id: int, lang: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("REPLACE INTO account_prefs(account_id,lang,consent) VALUES(?,?,COALESCE((SELECT consent FROM account_prefs WHERE account_id=?),0))", (account_id, lang, account_id))
    conn.commit()
    conn.close()

def get_account_lang(account_id: int) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT lang FROM account_prefs WHERE account_id=?", (account_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def set_account_consent(account_id: int, consent: bool) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("REPLACE INTO account_prefs(account_id,lang,consent) VALUES(?,COALESCE((SELECT lang FROM account_prefs WHERE account_id=?),NULL),?)", (account_id, account_id, 1 if consent else 0))
    conn.commit()
    conn.close()

def get_account_consent(account_id: int) -> Optional[bool]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT consent FROM account_prefs WHERE account_id=?", (account_id,))
    row = c.fetchone()
    conn.close()
    return bool(row[0]) if row else None

def get_user_fate(user_id: int) -> Optional[Tuple[str, str, str]]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT sign,zodiac,element FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return row[0], row[1], row[2]

def register_token(user_id: int, token: str, platform: str, language: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "REPLACE INTO device_tokens(user_id,token,platform,language) VALUES(?,?,?,?)",
        (user_id, token, platform, language),
    )
    conn.commit()
    conn.close()

def get_tokens(user_id: int, language: str | None = None) -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if language:
        c.execute("SELECT token FROM device_tokens WHERE user_id=? AND language=?", (user_id, language))
    else:
        c.execute("SELECT token FROM device_tokens WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

def list_device_tokens(user_id: int, language: str | None = None) -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if language:
        c.execute("SELECT token,platform,language FROM device_tokens WHERE user_id=? AND language=?", (user_id, language))
    else:
        c.execute("SELECT token,platform,language FROM device_tokens WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [{"token": r[0], "platform": r[1], "language": r[2]} for r in rows]

def delete_token(user_id: int, token: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM device_tokens WHERE user_id=? AND token=?", (user_id, token))
    conn.commit()
    conn.close()

def delete_tokens(user_id: int, tokens: list[str]) -> None:
    if not tokens:
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for t in tokens:
        c.execute("DELETE FROM device_tokens WHERE user_id=? AND token=?", (user_id, t))
    conn.commit()
    conn.close()

def record_stripe_customer(user_id: int, customer_id: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "REPLACE INTO stripe_customers(user_id,customer_id) VALUES(?,?)",
        (user_id, customer_id),
    )
    conn.commit()
    conn.close()

def get_user_by_customer(customer_id: str) -> Optional[int]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM stripe_customers WHERE customer_id=?", (customer_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def set_membership_status(user_id: int, status: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "REPLACE INTO membership_flags(user_id,status) VALUES(?,?)",
        (user_id, status),
    )
    conn.commit()
    conn.close()

def get_membership_status(user_id: int) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT status FROM membership_flags WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def list_memberships_expiring(days: int) -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT user_id, level, expires_at FROM memberships WHERE expires_at IS NOT NULL AND date(expires_at) <= date('now', '+' || ? || ' day')",
        (days,),
    )
    rows = c.fetchall()
    conn.close()
    return [{"user_id": r[0], "level": r[1], "expires_at": r[2]} for r in rows]

def has_stripe_event(event_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM stripe_events WHERE event_id=?", (event_id,))
    row = c.fetchone()
    conn.close()
    return bool(row)

def record_stripe_event(event_id: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO stripe_events(event_id,created_at) VALUES(?,datetime('now'))",
        (event_id,),
    )
    conn.commit()
    conn.close()

def has_paypal_event(event_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM paypal_events WHERE event_id=?", (event_id,))
    row = c.fetchone()
    conn.close()
    return bool(row)

def record_paypal_event(event_id: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO paypal_events(event_id,created_at) VALUES(?,datetime('now'))",
        (event_id,),
    )
    conn.commit()
    conn.close()

def set_push_pref(user_id: int, hour: int, enabled: bool, language: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "REPLACE INTO push_prefs(user_id,hour,enabled,language) VALUES(?,?,?,?)",
        (user_id, hour, 1 if enabled else 0, language),
    )
    conn.commit()
    conn.close()

def get_push_pref(user_id: int) -> Optional[Tuple[int, bool, str]]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT hour,enabled,language FROM push_prefs WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return row[0], bool(row[1]), row[2]

def upsert_push(user_id: int, day: str, language: str, energy: str, social: str, decision: str, relax: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "REPLACE INTO pushes(user_id,day,language,energy,social,decision,relax) VALUES(?,?,?,?,?,?,?)",
        (user_id, day, language, energy, social, decision, relax),
    )
    conn.commit()
    conn.close()

def get_push(user_id: int, day: str, language: str) -> Optional[Tuple[str, str, str, str]]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT energy,social,decision,relax FROM pushes WHERE user_id=? AND day=? AND language=?",
        (user_id, day, language),
    )
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return row[0], row[1], row[2], row[3]

def set_membership(user_id: int, level: str, expires_at: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "REPLACE INTO memberships(user_id,level,expires_at) VALUES(?,?,?)",
        (user_id, level, expires_at),
    )
    conn.commit()
    conn.close()

def get_membership(user_id: int) -> Optional[Tuple[str, str]]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT level,expires_at FROM memberships WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return row[0], row[1]

def add_post(user_id: int, sign: str, zodiac: str, language: str, content: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO posts(user_id,sign,zodiac,language,content,created_at) VALUES(?,?,?,?,?,datetime('now'))",
        (user_id, sign, zodiac, language, content),
    )
    pid = c.lastrowid
    conn.commit()
    conn.close()
    return pid

def list_posts(sign: Optional[str], zodiac: Optional[str], language: str, limit: int = 50, offset: int = 0) -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    base = "SELECT id,user_id,sign,zodiac,language,content,likes,created_at FROM posts WHERE language=?"
    params = [language]
    if sign:
        base += " AND sign=?"
        params.append(sign)
    if zodiac:
        base += " AND zodiac=?"
        params.append(zodiac)
    base += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.append(limit)
    params.append(offset)
    c.execute(base, tuple(params))
    rows = c.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "user_id": r[1],
            "sign": r[2],
            "zodiac": r[3],
            "language": r[4],
            "content": r[5],
            "likes": r[6],
            "created_at": r[7],
        }
        for r in rows
    ]

def like_post(post_id: int) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE posts SET likes = likes + 1 WHERE id=?", (post_id,))
    conn.commit()
    conn.close()

def get_experience_claimed(user_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT claimed FROM share_experience WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return bool(row and row[0])

def set_experience_claimed(user_id: int) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("REPLACE INTO share_experience(user_id,claimed) VALUES(?,1)", (user_id,))
    conn.commit()
    conn.close()

def _get_permission_row(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT decorations,glow,credits,share_count,report_unlocked FROM user_card_permission WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if not row:
        c.execute("INSERT OR IGNORE INTO user_card_permission(user_id,decorations,glow,credits,share_count,report_unlocked) VALUES(?,?,?,?,?,?)", (user_id, "[]", "[]", 0, 0, 0))
        conn.commit()
        c.execute("SELECT decorations,glow,credits,share_count,report_unlocked FROM user_card_permission WHERE user_id=?", (user_id,))
        row = c.fetchone()
    conn.close()
    return row

def get_permissions(user_id: int) -> Dict[str, Any]:
    row = _get_permission_row(user_id)
    return {"decorations": row[0], "glow": row[1], "credits": row[2], "share_count": row[3], "report_unlocked": bool(row[4])}

def add_decoration(user_id: int, name: str) -> None:
    import json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT decorations FROM user_card_permission WHERE user_id=?", (user_id,))
    row = c.fetchone()
    arr = json.loads(row[0] if row and row[0] else "[]")
    if name not in arr:
        arr.append(name)
    c.execute("UPDATE user_card_permission SET decorations=? WHERE user_id=?", (json.dumps(arr), user_id))
    conn.commit()
    conn.close()

def add_glow(user_id: int, name: str) -> None:
    import json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT glow FROM user_card_permission WHERE user_id=?", (user_id,))
    row = c.fetchone()
    arr = json.loads(row[0] if row and row[0] else "[]")
    if name not in arr:
        arr.append(name)
    c.execute("UPDATE user_card_permission SET glow=? WHERE user_id=?", (json.dumps(arr), user_id))
    conn.commit()
    conn.close()

def inc_share_count(user_id: int) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE user_card_permission SET share_count = COALESCE(share_count,0) + 1 WHERE user_id=?", (user_id,))
    c.execute("SELECT share_count FROM user_card_permission WHERE user_id=?", (user_id,))
    row = c.fetchone()
    sc = int(row[0] if row and row[0] else 0)
    if sc >= 3:
        c.execute("UPDATE user_card_permission SET report_unlocked=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
    return sc

def add_credit(user_id: int, delta: int) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE user_card_permission SET credits = COALESCE(credits,0) + ? WHERE user_id=?", (delta, user_id))
    conn.commit()
    conn.close()

def consume_credit(user_id: int) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT credits FROM user_card_permission WHERE user_id=?", (user_id,))
    row = c.fetchone()
    cur = int(row[0] if row and row[0] else 0)
    if cur <= 0:
        conn.close()
        return 0
    c.execute("UPDATE user_card_permission SET credits = credits - 1 WHERE user_id=?", (user_id,))
    conn.commit()
    c.execute("SELECT credits FROM user_card_permission WHERE user_id=?", (user_id,))
    row2 = c.fetchone()
    left = int(row2[0] if row2 and row2[0] else 0)
    conn.close()
    return left

def get_share_code(user_id: int) -> str:
    import secrets
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT code FROM share_codes WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row and row[0]:
        conn.close()
        return row[0]
    code = secrets.token_urlsafe(6)
    c.execute("INSERT OR REPLACE INTO share_codes(user_id,code) VALUES(?,?)", (user_id, code))
    conn.commit()
    conn.close()
    return code

def find_user_by_code(code: str) -> Optional[int]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM share_codes WHERE code=?", (code,))
    row = c.fetchone()
    conn.close()
    return int(row[0]) if row else None

def record_referral(inviter_user_id: int, new_user_id: int, paid: int = 0) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO referrals(inviter_user_id,new_user_id,paid,created_at) VALUES(?,?,?,datetime('now'))", (inviter_user_id, new_user_id, paid))
    conn.commit()
    conn.close()

def set_referral_paid(inviter_user_id: int, new_user_id: int) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE referrals SET paid=1 WHERE inviter_user_id=? AND new_user_id=?", (inviter_user_id, new_user_id))
    conn.commit()
    conn.close()

def create_short_link(sign: str, zodiac: str, element: str, long_url: str, lang: str | None = None) -> str:
    import secrets
    code = secrets.token_urlsafe(6)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT OR REPLACE INTO short_links(code,long_url,sign,zodiac,element,lang,created_at) VALUES(?,?,?,?,?,?,datetime('now'))",
            (code, long_url, sign, zodiac, element, lang or "en"),
        )
    except Exception:
        c.execute(
            "INSERT OR REPLACE INTO short_links(code,long_url,sign,zodiac,element,created_at) VALUES(?,?,?,?,?,datetime('now'))",
            (code, long_url, sign, zodiac, element),
        )
    conn.commit()
    conn.close()
    return code

def get_short_link(code: str) -> Optional[Tuple[str, str, str, str, str]]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("SELECT long_url,sign,zodiac,element,lang FROM short_links WHERE code=?", (code,))
    except Exception:
        c.execute("SELECT long_url,sign,zodiac,element FROM short_links WHERE code=?", (code,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    if len(row) == 5:
        return row[0], row[1], row[2], row[3], row[4]
    return row[0], row[1], row[2], row[3], "en"
