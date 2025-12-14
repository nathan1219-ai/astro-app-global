import os
import json
from typing import Tuple

try:
    import boto3
except Exception:
    boto3 = None

def _region() -> str:
    r = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if r:
        return r
    k = os.environ.get("BEDROCK_API_KEY")
    if k and "ap-southeast-2" in k:
        return "ap-southeast-2"
    return "ap-southeast-2"

def _client():
    if boto3 is None:
        return None
    try:
        return boto3.client("bedrock-runtime", region_name=_region())
    except Exception:
        return None

def generate_daily(sign: str, zodiac: str, element: str, language: str) -> Tuple[str, str, str, str]:
    c = _client()
    prompt = (
        f"Language: {language}.\n"
        f"User archetype: sign={sign}, zodiac={zodiac}, element={element}.\n"
        "Write four short lines (max 12 words each) as JSON with keys energy, social, decision, relax."
    )
    if c is None:
        if language == "es":
            return (f"Energía {element}", f"Social {sign}", f"Decisión {zodiac}", f"Relajación {element}")
        if language == "fr":
            return (f"Énergie {element}", f"Social {sign}", f"Décision {zodiac}", f"Détente {element}")
        return (f"Energy {element}", f"Social {sign}", f"Decision {zodiac}", f"Relax {element}")
    anthropic_version = os.environ.get("BEDROCK_ANTHROPIC_VERSION", "bedrock-2023-05-31")
    max_tokens = int(os.environ.get("BEDROCK_MAX_TOKENS", "256"))
    temperature = float(os.environ.get("BEDROCK_TEMPERATURE", "0.7"))
    body = {
        "anthropic_version": anthropic_version,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ],
    }
    try:
        model_id = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
        r = c.invoke_model(modelId=model_id, body=json.dumps(body))
        s = r.get("body").read().decode("utf-8")
        j = json.loads(s)
        txt = ""
        if j.get("content"):
            txt = j["content"][0].get("text", "")
        res = json.loads(txt)
        return (
            str(res.get("energy", ""))[:64],
            str(res.get("social", ""))[:64],
            str(res.get("decision", ""))[:64],
            str(res.get("relax", ""))[:64],
        )
    except Exception:
        if language == "es":
            return (f"Energía {element}", f"Social {sign}", f"Decisión {zodiac}", f"Relajación {element}")
        if language == "fr":
            return (f"Énergie {element}", f"Social {sign}", f"Décision {zodiac}", f"Détente {element}")
        return (f"Energy {element}", f"Social {sign}", f"Decision {zodiac}", f"Relax {element}")

def generate_expanded(sign: str, zodiac: str, element: str, language: str) -> dict:
    c = _client()
    prompt = (
        f"Language: {language}.\n"
        f"User archetype: sign={sign}, zodiac={zodiac}, element={element}.\n"
        "Write three sections as JSON keys energy_state, action_suggestions, self_exploration; each section 80-120 words; no line breaks; Unicode-safe; GDPR-friendly tone; no absolute claims."
    )
    if c is None:
        if language == "es":
            return {
                "energy_state": "Tu energía elemental se siente equilibrada pero activa; observa cómo las decisiones rápidas pueden acelerar tus avances sin perder serenidad...",
                "action_suggestions": "Organiza tu día en bloques de enfoque de 25 minutos; respira profundamente antes de reuniones; toma notas de emociones para mantener claridad...",
                "self_exploration": "Piensa en cómo tu signo y tu animal del zodíaco dialogan; escribe tres frases sobre tu propósito y una práctica breve para nutrir tu energía..."
            }
        if language == "fr":
            return {
                "energy_state": "Ton énergie élémentaire paraît stable et confiante; remarque comment les décisions mesurées renforcent ta progression sans rigidité...",
                "action_suggestions": "Structure ta journée par cycles d’attention; respire avant les échanges; prends des notes sur tes émotions pour garder la clarté...",
                "self_exploration": "Observe le dialogue entre ton signe et ton animal; écris trois phrases sur ton intention et une pratique courte pour nourrir ton énergie..."
            }
        return {
            "energy_state": "Your elemental energy feels balanced yet active; notice how measured decisions can accelerate progress without sacrificing calm...",
            "action_suggestions": "Plan your day in focused 25-min blocks; breathe before meetings; journal brief emotion notes to stay clear and steady...",
            "self_exploration": "Reflect on how your sign and zodiac animal interact; write three lines on your intent and a short practice that nourishes your energy..."
        }
    anthropic_version = os.environ.get("BEDROCK_ANTHROPIC_VERSION", "bedrock-2023-05-31")
    max_tokens = int(os.environ.get("BEDROCK_MAX_TOKENS", "512"))
    temperature = float(os.environ.get("BEDROCK_TEMPERATURE", "0.7"))
    body = {
        "anthropic_version": anthropic_version,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ],
    }
    try:
        model_id = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
        r = c.invoke_model(modelId=model_id, body=json.dumps(body))
        s = r.get("body").read().decode("utf-8")
        j = json.loads(s)
        txt = ""
        if j.get("content"):
            txt = j["content"][0].get("text", "")
        res = json.loads(txt)
        return {
            "energy_state": str(res.get("energy_state", "")),
            "action_suggestions": str(res.get("action_suggestions", "")),
            "self_exploration": str(res.get("self_exploration", "")),
        }
    except Exception:
        return generate_expanded(sign, zodiac, element, language if language in ("en","es","fr") else "en")

def generate_line_detail(sign: str, zodiac: str, element: str, language: str, line_type: str) -> dict:
    c = _client()
    tmap = {
        "energy": "Describe today's elemental energy state and how to leverage it",
        "social": "Give social guidance for interactions and relationships",
        "decision": "Offer decision-making tips balancing intuition and logic",
        "relax": "Suggest short calming practices to restore balance"
    }
    topic = tmap.get(line_type, "General guidance")
    prompt = (
        f"Language: {language}.\n"
        f"User: sign={sign}, zodiac={zodiac}, element={element}.\n"
        f"Write 100-140 words {topic}, GDPR-friendly, Unicode-safe, non-deterministic tone, no absolute claims. Return JSON {{detail: text}}."
    )
    if c is None:
        if language == "es":
            return {"detail": "Tu detalle ampliado: guía práctica y positiva para el día, enfocada en tu energía elemental, con pasos breves y claros para actuar y mantener serenidad."}
        if language == "fr":
            return {"detail": "Ton détail étendu : conseils pratiques et positifs pour la journée, ancrés dans ton énergie élémentaire, avec des gestes courts pour rester serein."}
        return {"detail": "Your extended detail: practical, positive guidance anchored to your elemental energy, with short, clear steps to act and stay calm today."}
    body = {
        "anthropic_version": os.environ.get("BEDROCK_ANTHROPIC_VERSION", "bedrock-2023-05-31"),
        "max_tokens": int(os.environ.get("BEDROCK_MAX_TOKENS", "512")),
        "temperature": float(os.environ.get("BEDROCK_TEMPERATURE", "0.7")),
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    }
    try:
        r = c.invoke_model(modelId=os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"), body=json.dumps(body))
        s = r.get("body").read().decode("utf-8")
        j = json.loads(s)
        txt = j.get("content", [{}])[0].get("text", "")
        res = json.loads(txt)
        return {"detail": str(res.get("detail", ""))}
    except Exception:
        return generate_line_detail(sign, zodiac, element, language if language in ("en","es","fr") else "en", line_type)
def generate_free_pack(sign: str, zodiac: str, element: str, language: str) -> dict:
    c = _client()
    prompt = (
        f"Language: {language}.\n"
        f"User: sign={sign}, zodiac={zodiac}, element={element}.\n"
        "Write five sections as JSON keys love, career, wealth, health, energy_state; each 80-120 words; GDPR-friendly tone; Unicode-safe; no absolute claims."
    )
    if c is None:
        base = {
            "love": "Balanced connection and mindful communication guide your day...",
            "career": "Focus blocks and calm decision-making unlock progress...",
            "wealth": "Practical budgeting and small wins reinforce stability...",
            "health": "Gentle movement and mindful breathing support resilience...",
            "energy_state": "Your elemental energy feels steady yet responsive...",
        }
        if language == "es":
            return {k: v for k, v in base.items()}
        if language == "fr":
            return {k: v for k, v in base.items()}
        return base
    body = {
        "anthropic_version": os.environ.get("BEDROCK_ANTHROPIC_VERSION", "bedrock-2023-05-31"),
        "max_tokens": int(os.environ.get("BEDROCK_MAX_TOKENS", "1024")),
        "temperature": float(os.environ.get("BEDROCK_TEMPERATURE", "0.7")),
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    }
    try:
        r = c.invoke_model(modelId=os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"), body=json.dumps(body))
        s = r.get("body").read().decode("utf-8")
        j = json.loads(s)
        txt = j.get("content", [{}])[0].get("text", "")
        return json.loads(txt)
    except Exception:
        return generate_free_pack(sign, zodiac, element, language if language in ("en","es","fr") else "en")

def generate_premium_pack(sign: str, zodiac: str, element: str, material: str, language: str) -> dict:
    c = _client()
    prompt = (
        f"Language: {language}.\n"
        f"User: sign={sign}, zodiac={zodiac}, element={element}, material={material}.\n"
        "Write three sections as JSON keys monthly_trend, balancing_advice, social_fit; each 100-140 words; mention material subtly; GDPR-friendly; Unicode-safe; no absolute claims."
    )
    if c is None:
        base = {
            "monthly_trend": "Your month trends toward steady growth with conscious pacing...",
            "balancing_advice": "Integrate short rituals to keep energy aligned and calm...",
            "social_fit": "Prioritize circles that value warmth and clarity in dialogue...",
        }
        if language == "es":
            return {k: v for k, v in base.items()}
        if language == "fr":
            return {k: v for k, v in base.items()}
        return base
    body = {
        "anthropic_version": os.environ.get("BEDROCK_ANTHROPIC_VERSION", "bedrock-2023-05-31"),
        "max_tokens": int(os.environ.get("BEDROCK_MAX_TOKENS", "1024")),
        "temperature": float(os.environ.get("BEDROCK_TEMPERATURE", "0.7")),
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    }
    try:
        r = c.invoke_model(modelId=os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"), body=json.dumps(body))
        s = r.get("body").read().decode("utf-8")
        j = json.loads(s)
        txt = j.get("content", [{}])[0].get("text", "")
        return json.loads(txt)
    except Exception:
        return generate_premium_pack(sign, zodiac, element, material, language if language in ("en","es","fr") else "en")
