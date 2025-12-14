from typing import Tuple

def generate_daily(sign: str, zodiac: str, element: str, language: str) -> Tuple[str, str, str, str]:
    if language == 'es':
        return (
            f"Energía {element}",
            f"Social {sign}",
            f"Decisión {zodiac}",
            f"Relajación {element}",
        )
    if language == 'fr':
        return (
            f"Énergie {element}",
            f"Social {sign}",
            f"Décision {zodiac}",
            f"Détente {element}",
        )
    return (
        f"Energy {element}",
        f"Social {sign}",
        f"Decision {zodiac}",
        f"Relax {element}",
    )
