"""Reviewed traditional lookup constants used as deterministic facts."""

STEMS = ("甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸")
BRANCHES = ("子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥")
STEM_ELEMENTS = {
    "甲": "WOOD", "乙": "WOOD", "丙": "FIRE", "丁": "FIRE", "戊": "EARTH",
    "己": "EARTH", "庚": "METAL", "辛": "METAL", "壬": "WATER", "癸": "WATER",
}
BRANCH_ELEMENTS = {
    "子": "WATER", "丑": "EARTH", "寅": "WOOD", "卯": "WOOD",
    "辰": "EARTH", "巳": "FIRE", "午": "FIRE", "未": "EARTH",
    "申": "METAL", "酉": "METAL", "戌": "EARTH", "亥": "WATER",
}
YIN_YANG = {
    **{stem: ("YANG" if index % 2 == 0 else "YIN") for index, stem in enumerate(STEMS)},
    **{branch: ("YANG" if index % 2 == 0 else "YIN") for index, branch in enumerate(BRANCHES)},
}
HIDDEN_STEMS = {
    "子": ("癸",), "丑": ("己", "癸", "辛"), "寅": ("甲", "丙", "戊"),
    "卯": ("乙",), "辰": ("戊", "乙", "癸"), "巳": ("丙", "戊", "庚"),
    "午": ("丁", "己"), "未": ("己", "丁", "乙"), "申": ("庚", "壬", "戊"),
    "酉": ("辛",), "戌": ("戊", "辛", "丁"), "亥": ("壬", "甲"),
}
STEM_COMBINATIONS = {frozenset(pair) for pair in ("甲己", "乙庚", "丙辛", "丁壬", "戊癸")}
BRANCH_COMBINATIONS = {frozenset(pair) for pair in ("子丑", "寅亥", "卯戌", "辰酉", "巳申", "午未")}
BRANCH_CLASHES = {frozenset(pair) for pair in ("子午", "丑未", "寅申", "卯酉", "辰戌", "巳亥")}
BRANCH_HARMS = {frozenset(pair) for pair in ("子未", "丑午", "寅巳", "卯辰", "申亥", "酉戌")}
BRANCH_BREAKS = {frozenset(pair) for pair in ("子酉", "丑辰", "寅亥", "卯午", "巳申", "未戌")}
BRANCH_PUNISHMENTS = (
    frozenset(("寅", "巳", "申")),
    frozenset(("丑", "未", "戌")),
    frozenset(("子", "卯")),
    frozenset(("辰",)),
    frozenset(("午",)),
    frozenset(("酉",)),
    frozenset(("亥",)),
)
THREE_HARMONIES = (
    frozenset(("申", "子", "辰")),
    frozenset(("亥", "卯", "未")),
    frozenset(("寅", "午", "戌")),
    frozenset(("巳", "酉", "丑")),
)
THREE_MEETINGS = (
    frozenset(("寅", "卯", "辰")),
    frozenset(("巳", "午", "未")),
    frozenset(("申", "酉", "戌")),
    frozenset(("亥", "子", "丑")),
)
