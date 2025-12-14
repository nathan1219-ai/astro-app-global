from datetime import date
from backend.astrology import sun_sign, zodiac, five_element, fate_label

def test_star_sign_boundaries():
    assert sun_sign(date(2024,3,20)) == "双鱼座"
    assert sun_sign(date(2024,3,21)) == "白羊座"

def test_zodiac_switch_2024():
    assert zodiac(date(2024,2,9)) == "兔"
    assert zodiac(date(2024,2,10)) == "龙"

def test_five_element_2024():
    assert five_element(date(2024,2,10)) == "木"

def test_fate_label():
    s,z,e,l = fate_label(date(2024,2,10))
    assert l == f"{s}+{z}+{e}"
