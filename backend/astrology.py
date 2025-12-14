from datetime import date
from typing import Optional, Tuple

try:
    from zhdate import ZhDate
except Exception:
    ZhDate = None

SIGNS = (
    (1, 20, 2, 18, "水瓶座"),
    (2, 19, 3, 20, "双鱼座"),
    (3, 21, 4, 19, "白羊座"),
    (4, 20, 5, 20, "金牛座"),
    (5, 21, 6, 21, "双子座"),
    (6, 22, 7, 22, "巨蟹座"),
    (7, 23, 8, 22, "狮子座"),
    (8, 23, 9, 22, "处女座"),
    (9, 23, 10, 23, "天秤座"),
    (10, 24, 11, 22, "天蝎座"),
    (11, 23, 12, 21, "射手座"),
    (12, 22, 1, 19, "摩羯座"),
)

ZODIAC_ORDER = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

FALLBACK_ZODIAC_RANGES = (
    (date(2020, 1, 25), date(2021, 2, 11), "鼠"),
    (date(2021, 2, 12), date(2022, 1, 31), "牛"),
    (date(2022, 2, 1), date(2023, 1, 21), "虎"),
    (date(2023, 1, 22), date(2024, 2, 9), "兔"),
    (date(2024, 2, 10), date(2025, 1, 28), "龙"),
)

GAN_ORDER = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
ZHI_ORDER = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
GAN_ELEMENT = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}

def sun_sign(d: date) -> str:
    for start_m, start_d, end_m, end_d, name in SIGNS:
        if start_m <= end_m:
            s = date(d.year, start_m, start_d)
            e = date(d.year, end_m, end_d)
            if s <= d <= e:
                return name
        else:
            s = date(d.year, start_m, start_d)
            e = date(d.year + 1, end_m, end_d)
            if d >= s or d <= date(d.year, end_m, end_d):
                return name
    return ""

def zodiac(d: date) -> str:
    for s, e, z in FALLBACK_ZODIAC_RANGES:
        if s <= d <= e:
            return z
    if ZhDate is None:
        return ""
    lunar = ZhDate.from_datetime(d)
    ly = lunar.lunar_year
    gz = lunar.ganzhi_year
    gan = gz[0]
    element = GAN_ELEMENT.get(gan, "")
    idx = (ly - 1984) % 12
    return ZODIAC_ORDER[idx]

def five_element(d: date) -> str:
    for s, e, z in FALLBACK_ZODIAC_RANGES:
        if s <= d <= e:
            if z == "龙":
                return "木"
            if z == "兔":
                return "水"
            if z == "虎":
                return "水"
            if z == "牛":
                return "金"
            if z == "鼠":
                return "金"
    if ZhDate is None:
        return ""
    lunar = ZhDate.from_datetime(d)
    gz = lunar.ganzhi_year
    gan = gz[0]
    return GAN_ELEMENT.get(gan, "")

def fate_label(d: date) -> Tuple[str, str, str, str]:
    s = sun_sign(d)
    z = zodiac(d)
    e = five_element(d)
    return s, z, e, f"{s}+{z}+{e}"
