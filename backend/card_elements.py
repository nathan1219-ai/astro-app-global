from typing import Dict

def elements_for(sign: str, zodiac: str, element: str) -> Dict[str, str]:
    texture = {
        "木": "wood",
        "火": "flame",
        "土": "sand",
        "金": "metal",
        "水": "water",
    }.get(element, "wood")
    glow = {
        "木": "#7bd389",
        "火": "#ff6b3d",
        "土": "#c2a36b",
        "金": "#ffd166",
        "水": "#6ec1ff",
    }.get(element, "#7bd389")
    border = "brass"
    motif = f"{zodiac}+{sign}"
    return {"texture": texture, "glow": glow, "border": border, "motif": motif}
