"""
72 风格日签系统 - 全新设计（基于 Anthropic 品牌色 + OpenClaw UI 设计规范）
- 常规主题：72种（S01-S72，按一年中第几天轮换，两个多月不重样）
- 节日主题：24种（H01-H24，节日期间优先使用，独立于常规主题之外）
- 设计原则：
  * 所有主题均为精致浅色/中色系，避免暗色背景
  * 严格遵循 WCAG AA 对比度规范
  * 配色比例：primary 主导 / secondary 辅助 / accent 点缀
  * 卡片使用半透明白色 + 柔和阴影
  * 暗纹：72 种通用主题各配不同装饰 SVG，24 种节日主题各配专属节日暗纹
"""

import os
import datetime
import random
from config import bj_date


# ============================================================
# LOGO 配置
# ============================================================
LOGO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
LOGO_XIATIANKANG = os.path.join(LOGO_DIR, "夏天抗衰诊所透明背景LOGO.png")
LOGO_SUMMERCLINIC = os.path.join(LOGO_DIR, "SUMMERCLINIC透明背景LOGO.png")


def select_logo_by_style(style):
    """统一使用夏天抗衰诊所 LOGO"""
    return LOGO_XIATIANKANG


# ============================================================
# 天气图标映射
# ============================================================
WEATHER_ICONS = {
    "晴": "☀️", "多云": "⛅", "阴": "🌥️", "小雨": "🌧️",
    "中雨": "🌧️", "大雨": "🌧️", "暴雨": "⛈️", "雷阵雨": "⛈️",
    "小雪": "🌨️", "中雪": "❄️", "大雪": "❄️", "雾": "🌫️",
    "霾": "😷", "阵雨": "🌦️", "阵雪": "🌨️",
}


def weather_icon(text: str) -> str:
    for k, v in WEATHER_ICONS.items():
        if k in text:
            return v
    return "🌤️"


# ============================================================
# 主题构建工具函数
# ============================================================

def make_bg(colors):
    """生成 5 阶渐变背景"""
    return f"linear-gradient(160deg,{colors[0]},{colors[1]},{colors[2]},{colors[3]},{colors[4]})"


def make_style(name, name_en, bg_grad, primary, secondary, accent,
               text, text_light, card_bg, card_border,
               divider, greeting_font, body_font, label_font,
               greeting_size, tag_bg, tag_color, card_radius,
               decor, greeting, footer):
    """标准主题构造器"""
    return dict(
        name=name, name_en=name_en,
        bg=bg_grad,
        primary=primary, secondary=secondary, accent=accent,
        text=text, text_light=text_light,
        card_bg=card_bg, card_border=card_border,
        divider=divider,
        greeting_font=greeting_font,
        body_font=body_font,
        label_font=label_font,
        greeting_size=greeting_size,
        tag_bg=tag_bg, tag_color=tag_color,
        card_radius=card_radius,
        decor=decor, greeting=greeting,
        footer=footer,
    )


# ============================================================
# 字体常量
# ============================================================
FONT_DISPLAY = "'Ma Shan Zheng', 'ZCOOL XiaoWei', cursive"
FONT_SERIF   = "'Noto Serif SC', 'Songti SC', 'FangSong', serif"
FONT_SANS    = "'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif"


# ============================================================
# 8 大色系配色方案（每系 9 种色阶变化）
# ============================================================

# ────────────────────────────────────────────────────────────
# A 系：珊瑚粉橙（温柔亲和，女性气质）
# ────────────────────────────────────────────────────────────
A_BG  = ["#FFF5F2", "#FFE8E0", "#FFD8C8", "#FFC8B0", "#FFB898"]
A_P   = "#C4604A"
A_S   = "#D47868"
A_A   = "#E89878"
A_T   = "#6B3820"
A_TL  = "rgba(107,56,32,0.62)"
A_CB  = "rgba(255,255,255,0.60)"
A_CBR = "rgba(255,196,160,0.65)"

# ────────────────────────────────────────────────────────────
# B 系：鼠尾草绿（自然清新，疗愈静谧）
# ────────────────────────────────────────────────────────────
B_BG  = ["#F0F8F2", "#E0F0E0", "#D0E8D0", "#C0E0C0", "#B0D8B0"]
B_P   = "#4A7040"
B_S   = "#608050"
B_A   = "#78A060"
B_T   = "#2A4820"
B_TL  = "rgba(42,72,32,0.62)"
B_CB  = "rgba(255,255,255,0.60)"
B_CBR = "rgba(176,224,176,0.65)"

# ────────────────────────────────────────────────────────────
# C 系：天青蓝（宁静开阔，清爽通透）
# ────────────────────────────────────────────────────────────
C_BG  = ["#F0F8FF", "#E0EFFF", "#D0E8FF", "#C0E0FF", "#B0D8FF"]
C_P   = "#3868A8"
C_S   = "#5080B8"
C_A   = "#6898C8"
C_T   = "#1E3A60"
C_TL  = "rgba(30,58,96,0.62)"
C_CB  = "rgba(255,255,255,0.60)"
C_CBR = "rgba(176,216,255,0.65)"

# ────────────────────────────────────────────────────────────
# D 系：薰衣草紫（优雅神秘，梦幻浪漫）
# ────────────────────────────────────────────────────────────
D_BG  = ["#F8F0FF", "#F0E0FF", "#E8D0FF", "#E0C0FF", "#D8B0FF"]
D_P   = "#6848A0"
D_S   = "#8058B0"
D_A   = "#9868C8"
D_T   = "#3A1868"
D_TL  = "rgba(58,24,104,0.62)"
D_CB  = "rgba(255,255,255,0.58)"
D_CBR = "rgba(216,176,255,0.68)"

# ────────────────────────────────────────────────────────────
# E 系：玫瑰粉（柔美优雅，女性气质）
# ────────────────────────────────────────────────────────────
E_BG  = ["#FFF5F8", "#FFE8F0", "#FFD8E8", "#FFC8E0", "#FFB8D8"]
E_P   = "#A04878"
E_S   = "#B85890"
E_A   = "#D068A8"
E_T   = "#602048"
E_TL  = "rgba(96,32,72,0.62)"
E_CB  = "rgba(255,255,255,0.58)"
E_CBR = "rgba(255,176,216,0.68)"

# ────────────────────────────────────────────────────────────
# F 系：奶油米色（温暖亲和，极简质感）
# ────────────────────────────────────────────────────────────
F_BG  = ["#FFFCF5", "#FFF5E8", "#FFECD8", "#FFE3C8", "#FFDAB8"]
F_P   = "#8B6840"
F_S   = "#A88050"
F_A   = "#C09860"
F_T   = "#5A4020"
F_TL  = "rgba(90,64,32,0.60)"
F_CB  = "rgba(255,252,245,0.68)"
F_CBR = "rgba(255,200,160,0.58)"

# ────────────────────────────────────────────────────────────
# G 系：薄荷青绿（清爽活力，清凉夏日）
# ────────────────────────────────────────────────────────────
G_BG  = ["#F0FFF8", "#E0F8F0", "#D0F0E8", "#C0E8E0", "#B0E0D8"]
G_P   = "#288870"
G_S   = "#40A080"
G_A   = "#58B890"
G_T   = "#185848"
G_TL  = "rgba(24,88,72,0.62)"
G_CB  = "rgba(255,255,255,0.60)"
G_CBR = "rgba(176,224,208,0.65)"

# ────────────────────────────────────────────────────────────
# H 系：琥珀金（温暖贵气，秋日暖阳）
# ────────────────────────────────────────────────────────────
H_BG  = ["#FFF8E8", "#FFE8C0", "#FFD8A0", "#FFC880", "#FFB860"]
H_P   = "#8B6820"
H_S   = "#A88030"
H_A   = "#C89840"
H_T   = "#5A4010"
H_TL  = "rgba(90,64,16,0.62)"
H_CB  = "rgba(255,248,232,0.68)"
H_CBR = "rgba(255,200,128,0.55)"


# ============================================================
# 通用主题构造器（带 decor 参数）
# ============================================================

def make_gen(n, bg_grad, primary, secondary, accent,
             text, text_light, card_bg, card_border,
             greeting_size, card_radius, decor, footer):
    return make_style(
        name=f"S{n:02d}", name_en=f"S{n:02d}",
        bg_grad=bg_grad,
        primary=primary, secondary=secondary, accent=accent,
        text=text, text_light=text_light,
        card_bg=card_bg, card_border=card_border,
        divider="✿ · ˚ ✿",
        greeting_font=FONT_DISPLAY,
        body_font=FONT_SERIF,
        label_font=FONT_SANS,
        greeting_size=greeting_size,
        tag_bg=secondary + "30",
        tag_color=primary,
        card_radius=card_radius,
        decor=decor,
        greeting="早安",
        footer=footer,
    )


# ============================================================
# 72 种通用主题（S01-S72）- 每种主题独立暗纹装饰
# ============================================================

class S:
    """72 种通用风格预设，每种主题独立暗纹"""

    # ── A 系：珊瑚粉橙（9 种）────────────────────────────────
    S01 = make_gen(1,  make_bg(A_BG), A_P, A_S, A_A, A_T, A_TL, A_CB, A_CBR,
                    "30px", "20px", "roses",        "温柔待己，岁月成诗")
    S02 = make_gen(2,  make_bg(["#FFF8F5","#FFE8EE","#FFD8E7","#FFC8E0","#FFB8D9"]),
                    "#B85080","#D06898","#E880B0",
                    "#682040","rgba(104,32,64,0.62)",
                    "rgba(255,255,255,0.58)","rgba(255,184,220,0.68)",
                    "30px","18px","cherry",      "心有蔷薇，一路芬芳")
    S03 = make_gen(3,  make_bg(["#FFF8F0","#FFE8D8","#FFD8C0","#FFC8A8","#FFB890"]),
                    A_P, A_S, A_A, A_T, A_TL, A_CB, A_CBR,
                    "30px","16px","cream",       "慢品人间烟火色")
    S04 = make_gen(4,  make_bg(["#FFF0E8","#FFE0CC","#FFD0B0","#FFC094","#FFB078"]),
                    "#A05030","#C06840","#D48058",
                    "#6B3A20","rgba(107,58,32,0.60)",
                    "rgba(255,240,228,0.62)","rgba(255,160,100,0.55)",
                    "30px","14px","maple",       "生活明朗，万物可爱")
    S05 = make_gen(5,  make_bg(["#FFF5E8","#FFE8C8","#FFD8A8","#FFC888","#FFB868"]),
                    "#8B6030","#A87840","#C09050",
                    "#5D4020","rgba(93,64,32,0.60)",
                    "rgba(255,248,228,0.68)","rgba(200,150,80,0.50)",
                    "30px","16px","lavender_field","热爱生活，日子闪光")
    S06 = make_gen(6,  make_bg(["#FDF5EC","#F0E0D0","#E8D0BC","#E0C0A8","#D8B094"]),
                    "#7B5038","#9B6848","#B08060",
                    "#4A3020","rgba(74,48,32,0.62)",
                    "rgba(255,248,240,0.65)","rgba(176,128,96,0.50)",
                    "30px","12px","cream",        "生活很苦，糖要自己加")
    S07 = make_gen(7,  make_bg(["#FFF0F5","#F8E0E8","#F0D0DB","#E8C0CE","#E0B0C1"]),
                    "#9B4A68","#B86880","#D08898",
                    "#6B3050","rgba(107,48,80,0.62)",
                    "rgba(255,255,255,0.55)","rgba(224,176,193,0.68)",
                    "30px","20px","petals",       "温柔半两，从容一生")
    S08 = make_gen(8,  make_bg(["#FFFDF5","#FFF8E8","#FFF0D8","#FFE8C8","#FFE0B8"]),
                    "#907040","#B08850","#C8A060",
                    "#5D4820","rgba(93,72,32,0.60)",
                    "rgba(255,252,240,0.68)","rgba(200,160,96,0.52)",
                    "30px","18px","lavender",     "今天也要元气满天")
    S09 = make_gen(9,  make_bg(["#FDF8F0","#F0E8D8","#E8D8C0","#E0C8A8","#D8B890"]),
                    "#7B5830","#9B7040","#B08850",
                    "#4A3818","rgba(74,56,24,0.60)",
                    "rgba(255,248,236,0.66)","rgba(176,136,80,0.48)",
                    "30px","14px","aurora",       "心有暖阳，无谓悲伤")

    # ── B 系：鼠尾草绿（9 种）────────────────────────────────
    S10 = make_gen(10, make_bg(B_BG), B_P, B_S, B_A, B_T, B_TL, B_CB, B_CBR,
                    "30px","18px","moss",         "心向自然，万物可亲")
    S11 = make_gen(11, make_bg(["#F0FFF8","#E0F8F0","#D0F0E8","#C0E8E0","#B0E0D8"]),
                    "#2D8870","#40A080","#58B898",
                    "#1D6050","rgba(29,96,80,0.60)",
                    "rgba(255,255,255,0.60)","rgba(176,224,208,0.65)",
                    "30px","20px","moss",         "清凉夏日，心旷神怡")
    S12 = make_gen(12, make_bg(["#F0F5F0","#D8E8D8","#C0DBCC","#A8CEB8","#90C1A4"]),
                    "#3D6848","#508060","#689478",
                    "#284838","rgba(40,72,56,0.60)",
                    "rgba(255,255,255,0.56)","rgba(144,193,164,0.62)",
                    "30px","16px","fern",         "自然无言，却最治愈")
    S13 = make_gen(13, make_bg(["#F8FFF0","#E8F8D0","#D8F0B0","#C8E890","#B8E070"]),
                    "#5A8020","#789840","#98B058",
                    "#3A5810","rgba(58,88,16,0.62)",
                    "rgba(255,255,255,0.60)","rgba(152,176,88,0.62)",
                    "30px","18px","grass",        "清茶一盏，浮生半闲")
    S14 = make_gen(14, make_bg(["#F5F8F0","#E0ECD8","#CCE0C0","#B8D4A8","#A4C890"]),
                    "#5A7030","#788848","#98A060",
                    "#384820","rgba(56,72,32,0.62)",
                    "rgba(255,255,240,0.58)","rgba(152,160,96,0.58)",
                    "30px","14px","grass",        "人间烟火，皆是诗意")
    S15 = make_gen(15, make_bg(["#F8FFF5","#E8F8E8","#D8F0D8","#C8E8C8","#B8E0B8"]),
                    "#387030","#4D8850","#60A068",
                    "#244A1E","rgba(36,74,30,0.62)",
                    "rgba(255,255,255,0.60)","rgba(176,224,176,0.62)",
                    "30px","20px","olive",        "每一天，都是新的开始")
    S16 = make_gen(16, make_bg(["#EDF5EC","#D8E8D8","#C4DBC8","#B0CEB8","#9CC1A8"]),
                    "#3A6038","#507850","#689068",
                    "#263C24","rgba(38,60,36,0.62)",
                    "rgba(255,255,250,0.58)","rgba(156,192,168,0.60)",
                    "30px","16px","olive",        "绿意盎然，生机勃发")
    S17 = make_gen(17, make_bg(["#F8FFF0","#E8F8D0","#D8F0B0","#C8E890","#B8E070"]),
                    "#6A9018","#88B030","#A8D048",
                    "#486000","rgba(72,96,0,0.62)",
                    "rgba(255,255,255,0.62)","rgba(168,208,72,0.60)",
                    "30px","20px","neon",        "生活有光，活力满格")
    S18 = make_gen(18, make_bg(["#F0F5F2","#D8E4D8","#C0D3C0","#A8C2A8","#90B190"]),
                    "#3D5840","#527054","#688868",
                    "#283828","rgba(40,56,40,0.60)",
                    "rgba(255,255,252,0.58)","rgba(144,176,144,0.60)",
                    "30px","14px","fern",         "静水深流，智者无言")

    # ── C 系：天青蓝（9 种）─────────────────────────────────
    S19 = make_gen(19, make_bg(C_BG), C_P, C_S, C_A, C_T, C_TL, C_CB, C_CBR,
                    "30px","20px","clouds_soft",  "心向远方，逐光而行")
    S20 = make_gen(20, make_bg(["#F5F8FF","#E8F0FF","#DBE8FF","#CEE0FF","#C1D8FF"]),
                    "#3868A0","#4878B8","#5888D0",
                    "#1E4060","rgba(30,64,96,0.62)",
                    "rgba(255,255,255,0.60)","rgba(193,216,255,0.68)",
                    "30px","18px","waves",        "纯净如冰，清澈如风")
    S21 = make_gen(21, make_bg(["#F0F5FF","#D8E8FF","#C0DBFF","#A8CEFF","#90C1FF"]),
                    "#2850A0","#3860B8","#4870D0",
                    "#18306A","rgba(24,48,106,0.62)",
                    "rgba(255,255,255,0.56)","rgba(144,193,255,0.65)",
                    "30px","16px","waves",        "海阔天空，皆是温柔")
    S22 = make_gen(22, make_bg(["#F0FFF8","#D8F8F0","#C0F0E8","#A8E8E0","#90E0D8"]),
                    "#2888A0","#38A0B8","#48B8D0",
                    "#185868","rgba(24,88,104,0.62)",
                    "rgba(255,255,255,0.60)","rgba(144,224,216,0.65)",
                    "30px","20px","fog",          "如蛋清透，如晨清新")
    S23 = make_gen(23, make_bg(["#F0F8FF","#D8ECFF","#C0E0FF","#A8D4FF","#90C8FF"]),
                    "#2060A8","#3070C0","#4080D8",
                    "#143068","rgba(20,48,104,0.62)",
                    "rgba(255,255,255,0.58)","rgba(144,200,255,0.65)",
                    "30px","16px","waves",        "面朝大海，春暖花开")
    S24 = make_gen(24, make_bg(["#F2F4F8","#DCE4F0","#C8D4E8","#B4C4E0","#A0B4D8"]),
                    "#4858A0","#5868B8","#6878D0",
                    "#28306A","rgba(40,48,106,0.62)",
                    "rgba(255,255,255,0.58)","rgba(160,180,216,0.65)",
                    "30px","14px","fog",          "雾尽风暖，美好将至")
    S25 = make_gen(25, make_bg(["#F0F5FF","#D8E4FF","#C0D3FF","#A8C2FF","#90B1FF"]),
                    "#3868B8","#4878D0","#5888E8",
                    "#1E3E80","rgba(30,62,128,0.62)",
                    "rgba(255,255,255,0.58)","rgba(144,178,255,0.68)",
                    "30px","20px","triangle",     "如花绽放，如光闪耀")
    S26 = make_gen(26, make_bg(["#F5F8FF","#E0E8FF","#CBD8FF","#B6C8FF","#A1B8FF"]),
                    "#3040B0","#4050C8","#5060E0",
                    "#1A205A","rgba(26,32,90,0.62)",
                    "rgba(255,255,255,0.56)","rgba(161,184,255,0.68)",
                    "30px","18px","aurora",       "珍贵如蓝，璀璨如星")
    S27 = make_gen(27, make_bg(["#F5F0FF","#E8E0FF","#DBD0FF","#CEC0FF","#C1B0FF"]),
                    "#6050B8","#7060D0","#8070E8",
                    "#382868","rgba(56,40,104,0.62)",
                    "rgba(255,255,255,0.58)","rgba(193,176,255,0.68)",
                    "30px","20px","lavender_field","浪漫如紫，温柔如诗")
    S28 = make_gen(28, make_bg(["#F8F4FF","#EEE8FF","#E4DCFF","#DAD0FF","#D0C4FF"]),
                    "#4A30B0","#5A40C8","#6A50E0",
                    "#261460","rgba(38,20,96,0.62)",
                    "rgba(255,255,255,0.58)","rgba(208,196,255,0.68)",
                    "30px","14px","sparkle",    "星光不问赶路人")

    # ── D 系：薰衣草紫（9 种）────────────────────────────────
    S29 = make_gen(29, make_bg(D_BG), D_P, D_S, D_A, D_T, D_TL, D_CB, D_CBR,
                    "30px","20px","lavender_field","紫色梦幻，浪漫相随")
    S30 = make_gen(30, make_bg(["#F5F0FF","#E8E0FF","#DBD0FF","#CEC0FF","#C1B0FF"]),
                    "#5848B0","#6858C8","#7868E0",
                    "#302068","rgba(48,32,104,0.62)",
                    "rgba(255,255,255,0.58)","rgba(193,176,255,0.68)",
                    "30px","18px","lavender",    "藤蔓缠绕，岁月静好")
    S31 = make_gen(31, make_bg(["#FAF0FF","#F4E0FF","#EED0FF","#E8C0FF","#E2B0FF"]),
                    "#7048A8","#8858C0","#A068D8",
                    "#482870","rgba(72,40,112,0.62)",
                    "rgba(255,255,255,0.58)","rgba(226,176,255,0.68)",
                    "30px","16px","lavender_field","如丁香绽放，淡雅从容")
    S32 = make_gen(32, make_bg(["#F5F0FF","#E8D8FF","#DCC0FF","#D0A8FF","#C490FF"]),
                    "#5020A0","#6030B8","#7040D0",
                    "#280C58","rgba(40,12,88,0.62)",
                    "rgba(255,255,255,0.56)","rgba(196,144,255,0.68)",
                    "30px","14px","triangle",    "神秘深邃，魅力无穷")
    S33 = make_gen(33, make_bg(["#FFFAFF","#F8F0FF","#F0E8FF","#E8E0FF","#E0D8FF"]),
                    "#6040B0","#7850C8","#9060E0",
                    "#3A2068","rgba(58,32,104,0.62)",
                    "rgba(255,255,255,0.60)","rgba(224,216,255,0.70)",
                    "30px","20px","sparkle",    "梦里花开，醒来温柔")
    S34 = make_gen(34, make_bg(["#F8F0FF","#E8DCFF","#D8C8FF","#C8B4FF","#B8A0FF"]),
                    "#4A28A0","#5C38B8","#6E48D0",
                    "#280E60","rgba(40,14,96,0.62)",
                    "rgba(255,255,255,0.56)","rgba(184,160,255,0.68)",
                    "30px","16px","lavender",     "岁月沉香，优雅如酒")
    S35 = make_gen(35, make_bg(["#F5F0FF","#E4D8FF","#D4C0FF","#C4A8FF","#B490FF"]),
                    "#5838B8","#6A48D0","#7C58E8",
                    "#30106A","rgba(48,16,106,0.62)",
                    "rgba(255,255,255,0.58)","rgba(180,144,255,0.68)",
                    "30px","18px","lavender_field","如鸢尾花，静美绽放")
    S36 = make_gen(36, make_bg(["#F8F4FF","#ECE8FF","#E0DCFF","#D4D0FF","#C8C4FF"]),
                    "#4838B0","#5C48C8","#7058E0",
                    "#261860","rgba(38,24,96,0.62)",
                    "rgba(255,255,255,0.58)","rgba(200,196,255,0.68)",
                    "30px","14px","fog",          "朦胧之美，意境悠远")

    # ── E 系：玫瑰粉（9 种）─────────────────────────────────
    S37 = make_gen(37, make_bg(E_BG), E_P, E_S, E_A, E_T, E_TL, E_CB, E_CBR,
                    "30px","20px","cherry",       "如花在野，热烈温柔")
    S38 = make_gen(38, make_bg(["#FFF5F8","#FFE8F0","#FFD8E8","#FFC8E0","#FFB8D8"]),
                    "#9838A0","#B048B8","#C858D0",
                    "#580E60","rgba(88,14,96,0.62)",
                    "rgba(255,255,255,0.58)","rgba(255,184,216,0.68)",
                    "30px","18px","petals",        "落樱缤纷，岁月静好")
    S39 = make_gen(39, make_bg(["#FFF8FC","#FFF0F4","#FFE8EC","#FFE0E4","#FFD8DC"]),
                    "#8858A0","#A068B8","#B878D0",
                    "#503068","rgba(80,48,104,0.62)",
                    "rgba(255,255,255,0.58)","rgba(255,216,220,0.68)",
                    "30px","16px","roses",         "清雅如荷，自在从容")
    S40 = make_gen(40, make_bg(["#FFF0F2","#FFE4E4","#FFD8D8","#FFCCCC","#FFC0C0"]),
                    "#9040A8","#A850C0","#C060D8",
                    "#501068","rgba(80,16,104,0.62)",
                    "rgba(255,255,255,0.56)","rgba(255,192,192,0.68)",
                    "30px","14px","leaves_minimal","复古优雅，精致生活")
    S41 = make_gen(41, make_bg(["#FFF5F0","#FFE8E0","#FFD8D0","#FFC8C0","#FFB8B0"]),
                    "#8858A0","#A068B8","#B878D0",
                    "#503068","rgba(80,48,104,0.62)",
                    "rgba(255,255,255,0.58)","rgba(255,184,176,0.65)",
                    "30px","20px","cream",         "法式浪漫，优雅到老")
    S42 = make_gen(42, make_bg(["#FFF5F0","#FFE8DC","#FFD8C8","#FFC8B4","#FFB8A0"]),
                    "#A04870","#B85C88","#D070A0",
                    "#682848","rgba(104,40,72,0.62)",
                    "rgba(255,255,255,0.58)","rgba(255,184,160,0.65)",
                    "30px","18px","petals",        "甜蜜如桃，元气满满")
    S43 = make_gen(43, make_bg(["#FAF4F0","#F4E4E0","#EED4D0","#E8C4C0","#E2B4B0"]),
                    "#8B4A68","#A85C80","#C07098",
                    "#582840","rgba(88,40,64,0.62)",
                    "rgba(255,250,248,0.60)","rgba(226,180,176,0.65)",
                    "30px","16px","cherry",        "干枯之美，别样风情")
    S44 = make_gen(44, make_bg(["#FFF8FC","#F8F0FF","#F0E8FF","#E8E0FF","#E0D8FF"]),
                    "#7040A8","#8850C0","#A060D8",
                    "#401A68","rgba(64,26,104,0.62)",
                    "rgba(255,255,255,0.60)","rgba(224,216,255,0.68)",
                    "30px","20px","sparkle",     "纯真如初，柔软可爱")
    S45 = make_gen(45, make_bg(["#FFF8F8","#FFF0F4","#FFE8F0","#FFE0EC","#FFD8E8"]),
                    "#9848A0","#B058B8","#C868D0",
                    "#581868","rgba(88,24,104,0.62)",
                    "rgba(255,255,255,0.58)","rgba(255,216,232,0.68)",
                    "30px","20px","roses",         "甜美如糖，精致如你")

    # ── F 系：奶油米色（3 种）────────────────────────────────
    S46 = make_gen(46, make_bg(F_BG), F_P, F_S, F_A, F_T, F_TL, F_CB, F_CBR,
                    "30px","18px","cream",         "生活很甜，慢慢品尝")
    S47 = make_gen(47, make_bg(["#FDF5EC","#F0E0D0","#E8D0BC","#E0C0A8","#D8B094"]),
                    "#7B5038","#9B6848","#B08060",
                    "#4A3020","rgba(74,48,32,0.60)",
                    "rgba(255,248,240,0.65)","rgba(176,128,96,0.50)",
                    "30px","12px","cream",          "咖啡很苦，你要很甜")
    S48 = make_gen(48, make_bg(["#FDF8F0","#F0E8D8","#E8D8C0","#E0C8A8","#D8B890"]),
                    "#7B5830","#9B7040","#B08850",
                    "#4A3818","rgba(74,56,24,0.60)",
                    "rgba(255,248,236,0.66)","rgba(176,136,80,0.48)",
                    "30px","14px","waves",          "心有暖阳，无谓悲伤")

    # ── G 系：薄荷青绿（9 种）────────────────────────────────
    S49 = make_gen(49, make_bg(G_BG), G_P, G_S, G_A, G_T, G_TL, G_CB, G_CBR,
                    "30px","20px","moss",          "清新如风，心旷神怡")
    S50 = make_gen(50, make_bg(["#F0FFF8","#D8F8F0","#C0F0E8","#A8E8E0","#90E0D8"]),
                    "#208880","#30A090","#48B8A0",
                    "#185050","rgba(24,80,80,0.62)",
                    "rgba(255,255,255,0.60)","rgba(144,224,208,0.65)",
                    "30px","18px","fog",            "水光潋滟，宁静致远")
    S51 = make_gen(51, make_bg(["#F0F8F8","#D8F0F0","#C0E8E8","#A8E0E0","#90D8D8"]),
                    "#2A7878","#3D8C8C","#50A0A0",
                    "#1A4848","rgba(26,72,72,0.62)",
                    "rgba(255,255,255,0.58)","rgba(144,200,200,0.65)",
                    "30px","16px","waves",          "海天一色，澄澈空灵")
    S52 = make_gen(52, make_bg(["#F5FFFC","#E0F8F4","#CCF0EC","#B8E8E4","#A4E0DC"]),
                    "#2C8870","#40A080","#54B890",
                    "#185848","rgba(24,88,72,0.62)",
                    "rgba(255,255,255,0.60)","rgba(160,220,200,0.65)",
                    "30px","20px","waves",          "碧波荡漾，心随境转")
    S53 = make_gen(53, make_bg(["#F8FFFC","#E0FFF0","#C8FEE4","#B0FDD8","#98FCCC"]),
                    "#208860","#38A070","#50B880",
                    "#185040","rgba(24,80,64,0.62)",
                    "rgba(255,255,255,0.62)","rgba(152,248,200,0.65)",
                    "30px","18px","bamboo",         "绿意盈盈，生机盎然")
    S54 = make_gen(54, make_bg(["#F0F8F5","#D8F0E8","#C0E8DC","#A8E0D0","#90D8C4"]),
                    "#307860","#448C70","#58A080",
                    "#1A4838","rgba(26,72,56,0.62)",
                    "rgba(255,255,255,0.58)","rgba(144,200,176,0.65)",
                    "30px","16px","bamboo",         "松风清韵，禅意悠然")
    S55 = make_gen(55, make_bg(["#F5FFFF","#E0FFF0","#CCFFE0","#B8FFD0","#A4FFC0"]),
                    "#20A870","#38C080","#50D890",
                    "#106040","rgba(16,96,64,0.62)",
                    "rgba(255,255,255,0.62)","rgba(176,240,192,0.68)",
                    "30px","20px","waves_minimal","翡翠流转，清凉一夏")
    S56 = make_gen(56, make_bg(["#F0F8F8","#D8F0F0","#C0E8E8","#A8E0E0","#90D8D8"]),
                    "#287878","#3D8C8C","#52A0A0",
                    "#184848","rgba(24,72,72,0.62)",
                    "rgba(255,255,255,0.58)","rgba(144,200,200,0.65)",
                    "30px","14px","fog",            "宁静如水，淡泊明志")
    S57 = make_gen(57, make_bg(["#F8FFFC","#E0FFF0","#C8FEE0","#B0FDD0","#98FCC0"]),
                    "#20A870","#38C080","#50D890",
                    "#106040","rgba(16,96,64,0.62)",
                    "rgba(255,255,255,0.62)","rgba(152,248,192,0.68)",
                    "30px","20px","dots_clean",   "晨露微凉，万物清朗")

    # ── H 系：琥珀金（15 种）─────────────────────────────────
    S58 = make_gen(58, make_bg(H_BG), H_P, H_S, H_A, H_T, H_TL, H_CB, H_CBR,
                    "30px","18px","inkwash",      "金风玉露，人间值得")
    S59 = make_gen(59, make_bg(["#FFF8E8","#FFE0B0","#FFD090","#FFC070","#FFB050"]),
                    "#8B6020","#A87830","#C89040",
                    "#5A4010","rgba(90,64,16,0.62)",
                    "rgba(255,248,228,0.68)","rgba(255,200,100,0.55)",
                    "30px","16px","aurora",         "流金岁月，熠熠生辉")
    S60 = make_gen(60, make_bg(["#FFFAF0","#FFF0D0","#FFE8B0","#FFE090","#FFD870"]),
                    "#907820","#B09030","#C8A840",
                    "#5A4810","rgba(90,72,16,0.62)",
                    "rgba(255,250,232,0.70)","rgba(255,220,112,0.55)",
                    "30px","14px","cream",          "麦浪金黄，秋意渐浓")
    S61 = make_gen(61, make_bg(["#FFFCE8","#FFF0C0","#FFE498","#FFD870","#FFCC48"]),
                    "#A08010","#B89820","#D0B030",
                    "#604C08","rgba(96,76,8,0.62)",
                    "rgba(255,252,232,0.70)","rgba(255,220,72,0.55)",
                    "30px","20px","filmstrip",    "丰收时节，金穗满仓")
    S62 = make_gen(62, make_bg(["#FFF5D8","#FFE8B0","#FFD888","#FFC860","#FFB838"]),
                    "#907020","#B08830","#C8A040",
                    "#5A4010","rgba(90,64,16,0.62)",
                    "rgba(255,248,224,0.68)","rgba(255,200,100,0.55)",
                    "30px","18px","aurora",         "阳光正好，未来可期")
    S63 = make_gen(63, make_bg(["#FFFAF0","#FFF0D0","#FFE8B0","#FFE090","#FFD870"]),
                    "#8B7020","#A88030","#C09040",
                    "#5A4410","rgba(90,68,16,0.62)",
                    "rgba(255,250,232,0.70)","rgba(255,220,112,0.55)",
                    "30px","16px","brushstroke", "秋日私语，金叶纷飞")
    S64 = make_gen(64, make_bg(["#FFFCE8","#FFF4C0","#FFEC98","#FFE470","#FFDC48"]),
                    "#9A8010","#B49820","#CEB030",
                    "#5C4A08","rgba(92,74,8,0.62)",
                    "rgba(255,252,232,0.72)","rgba(255,228,72,0.55)",
                    "30px","14px","aurora",         "璀璨如金，岁月无惊")
    S65 = make_gen(65, make_bg(["#FFF8D8","#FFEAB0","#FFDC88","#FFCE60","#FFC038"]),
                    "#906820","#A88030","#C09840",
                    "#5A4010","rgba(90,64,16,0.62)",
                    "rgba(255,248,224,0.68)","rgba(255,200,100,0.55)",
                    "30px","18px","cream",          "向阳而生，温暖如初")
    S66 = make_gen(66, make_bg(["#FFFAE8","#FFF0C8","#FFE8A8","#FFE088","#FFD868"]),
                    "#907820","#B09028","#C8A838",
                    "#5A4810","rgba(90,72,16,0.62)",
                    "rgba(255,250,232,0.70)","rgba(255,220,104,0.55)",
                    "30px","20px","aurora",         "光阴含笑，岁月凝香")
    S67 = make_gen(67, make_bg(["#FFF5D0","#FFE4A8","#FFD380","#FFC258","#FFB130"]),
                    "#906820","#A88030","#C09840",
                    "#5A4010","rgba(90,64,16,0.62)",
                    "rgba(255,248,224,0.68)","rgba(255,200,100,0.55)",
                    "30px","16px","wave_ukiyoe","金色年华，不负韶光")
    S68 = make_gen(68, make_bg(["#FFFCE8","#FFF4C0","#FFEC98","#FFE470","#FFDC48"]),
                    "#A08010","#B89820","#D0B030",
                    "#604C08","rgba(96,76,8,0.62)",
                    "rgba(255,252,232,0.70)","rgba(255,228,72,0.55)",
                    "30px","14px","aurora",         "星河入梦，金风满怀")
    S69 = make_gen(69, make_bg(["#FFF8D8","#FFEAB0","#FFDC88","#FFCE60","#FFC038"]),
                    "#906C20","#A88030","#C09440",
                    "#5A4010","rgba(90,64,16,0.62)",
                    "rgba(255,248,224,0.68)","rgba(255,200,100,0.55)",
                    "30px","18px","window",       "秋水长天，心有所念")
    S70 = make_gen(70, make_bg(["#FFFAE8","#FFF0C8","#FFE8A8","#FFE088","#FFD868"]),
                    "#907820","#B09028","#C8A838",
                    "#5A4810","rgba(90,72,16,0.62)",
                    "rgba(255,250,232,0.70)","rgba(255,220,104,0.55)",
                    "30px","20px","cream",          "日升月落，皆是风景")
    S71 = make_gen(71, make_bg(["#FFFCD8","#FFF2A8","#FFE878","#FFDE48","#FFD418"]),
                    "#987010","#B09020","#C8A830",
                    "#5C4810","rgba(92,72,16,0.62)",
                    "rgba(255,252,224,0.70)","rgba(255,220,80,0.55)",
                    "30px","16px","aurora",         "光影交错，岁月如歌")
    S72 = make_gen(72, make_bg(["#FFF5D0","#FFE4A8","#FFD380","#FFC258","#FFB130"]),
                    "#906820","#A88030","#C09840",
                    "#5A4010","rgba(90,64,16,0.62)",
                    "rgba(255,248,224,0.68)","rgba(255,200,100,0.55)",
                    "30px","14px","barcode",     "繁花似锦，一路繁花")


# ============================================================
# 24 种节日主题（H01-H32）- 专属配色 + 专属暗纹
# ============================================================

class H:
    """24 种节日风格预设，主题配色 + 暗纹与节日强关联"""

    # ── 春节（红金喜庆）────────────────────────────────────
    H01 = make_style(
        name="春节金辉", name_en="SpringFestival01",
        bg_grad=make_bg(["#FFF5E8","#FFE8C0","#FFD898","#FFC870","#FFB848"]),
        primary="#C8390A", secondary="#E05020", accent="#FFD700",
        text="#6B1A05", text_light="rgba(107,26,5,0.60)",
        card_bg="rgba(255,252,240,0.78)", card_border="rgba(255,215,0,0.42)",
        divider="🧧 · 🧧",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="34px", tag_bg="rgba(255,215,0,0.22)", tag_color="#C8390A",
        card_radius="18px", decor="coin", greeting="恭贺新禧",
        footer="新春快乐，万事如意 🧧",
    )

    H02 = make_style(
        name="春节桃粉", name_en="SpringFestival02",
        bg_grad=make_bg(["#FFF8F0","#FFE8D0","#FFD8B0","#FFC890","#FFB870"]),
        primary="#A03828", secondary="#C05038", accent="#E87850",
        text="#6B2A18", text_light="rgba(107,42,24,0.60)",
        card_bg="rgba(255,248,240,0.72)", card_border="rgba(200,80,56,0.48)",
        divider="🏮 · 🏮",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(192,80,56,0.20)", tag_color="#A03828",
        card_radius="16px", decor="lantern", greeting="福到财到",
        footer="新年吉祥，阖家幸福 🏮",
    )

    # ── 元宵节（暖黄灯笼）──────────────────────────────────
    H03 = make_style(
        name="元宵灯彩", name_en="Lantern01",
        bg_grad=make_bg(["#FFF8E0","#FFEAB8","#FFDC90","#FFCE68","#FFC040"]),
        primary="#C07010", secondary="#D88820", accent="#FFA020",
        text="#6B4208", text_light="rgba(107,66,8,0.60)",
        card_bg="rgba(255,252,228,0.78)", card_border="rgba(255,160,32,0.42)",
        divider="🏮 · 🌙 · 🏮",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(216,136,32,0.20)", tag_color="#C07010",
        card_radius="18px", decor="lantern", greeting="元宵喜乐",
        footer="灯火阑珊，花好月圆 🏮",
    )

    H04 = make_style(
        name="元宵星夜", name_en="Lantern02",
        bg_grad=make_bg(["#F8F0FF","#EDE0FF","#E2D0FF","#D7C0FF","#CCB0FF"]),
        primary="#5830A0", secondary="#7848B8", accent="#A060D8",
        text="#30186B", text_light="rgba(48,24,107,0.60)",
        card_bg="rgba(255,252,255,0.72)", card_border="rgba(160,96,216,0.50)",
        divider="✨ · 🌙 · ✨",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(120,72,184,0.20)", tag_color="#5830A0",
        card_radius="16px", decor="sparkle", greeting="花灯如昼",
        footer="元宵安康，灯火可亲 ✨",
    )

    # ── 清明节（新绿春雨）──────────────────────────────────
    H05 = make_style(
        name="清明新绿", name_en="Qingming01",
        bg_grad=make_bg(["#F0F8E8","#D8F0D0","#C0E8B8","#A8E0A0","#90D888"]),
        primary="#3A6020", secondary="#4D7830", accent="#609040",
        text="#253D12", text_light="rgba(37,61,18,0.62)",
        card_bg="rgba(255,255,248,0.72)", card_border="rgba(96,144,64,0.50)",
        divider="🌿 · 🌱 · 🌿",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="30px", tag_bg="rgba(77,120,48,0.18)", tag_color="#3A6020",
        card_radius="16px", decor="bamboo_leaf", greeting="清明安康",
        footer="春和景明，踏青思远 🌿",
    )

    H06 = make_style(
        name="清明烟雨", name_en="Qingming02",
        bg_grad=make_bg(["#EEF4F0","#D8E8E0","#C2DCD0","#ACD0C0","#96C4B0"]),
        primary="#385858", secondary="#487070", accent="#588888",
        text="#1E3438", text_light="rgba(30,52,56,0.62)",
        card_bg="rgba(255,255,252,0.68)", card_border="rgba(88,136,136,0.48)",
        divider="💧 · 🌧️ · 💧",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="30px", tag_bg="rgba(72,112,112,0.18)", tag_color="#385858",
        card_radius="16px", decor="rain", greeting="清明时节",
        footer="细雨纷纷，思绪悠悠 💧",
    )

    # ── 端午节（艾草粽香）──────────────────────────────────
    H07 = make_style(
        name="端午艾香", name_en="DragonBoat01",
        bg_grad=make_bg(["#EDF5E8","#D8E8D0","#C3DBC0","#AECEB0","#99C1A0"]),
        primary="#4A7030", secondary="#608840", accent="#78A050",
        text="#2D4520", text_light="rgba(45,69,32,0.62)",
        card_bg="rgba(255,255,248,0.70)", card_border="rgba(120,160,80,0.48)",
        divider="🫔 · 🌿 · 🫔",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(96,132,64,0.18)", tag_color="#4A7030",
        card_radius="14px", decor="zongye", greeting="端午安康",
        footer="粽叶飘香，祈福纳祥 🫔",
    )

    H08 = make_style(
        name="端午碧波", name_en="DragonBoat02",
        bg_grad=make_bg(["#E8F8F5","#C8F0E8","#A8E8DB","#88E0CE","#68D8C1"]),
        primary="#287870", secondary="#389090", accent="#48A8A8",
        text="#1A4A48", text_light="rgba(26,74,72,0.62)",
        card_bg="rgba(255,255,252,0.68)", card_border="rgba(72,168,168,0.45)",
        divider="🌊 · 🐉 · 🌊",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(56,144,144,0.18)", tag_color="#287870",
        card_radius="18px", decor="waves", greeting="端午安康",
        footer="龙舟竞渡，碧波欢畅 🌊",
    )

    # ── 七夕节（浪漫粉紫）──────────────────────────────────
    H09 = make_style(
        name="七夕粉缘", name_en="Qixi01",
        bg_grad=make_bg(["#FFF5F8","#FFE8F0","#FFD8E8","#FFC8E0","#FFB8D8"]),
        primary="#A03070", secondary="#B84888", accent="#D060A0",
        text="#601848", text_light="rgba(96,24,72,0.62)",
        card_bg="rgba(255,255,255,0.65)", card_border="rgba(208,96,160,0.55)",
        divider="💕 · 💕 · 💕",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(184,72,136,0.18)", tag_color="#A03070",
        card_radius="20px", decor="heart", greeting="七夕快乐",
        footer="星河鹊桥，相思成桥 💕",
    )

    H10 = make_style(
        name="七夕星河", name_en="Qixi02",
        bg_grad=make_bg(["#F5F0FF","#E8E0FF","#DCD0FF","#D0C0FF","#C4B0FF"]),
        primary="#5020A8", secondary="#6830C0", accent="#8040D8",
        text="#280C60", text_light="rgba(40,12,96,0.62)",
        card_bg="rgba(255,255,255,0.62)", card_border="rgba(128,64,216,0.52)",
        divider="✨ · 🌌 · ✨",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(104,48,192,0.18)", tag_color="#5020A8",
        card_radius="20px", decor="sparkle", greeting="七夕情深",
        footer="银河相望，爱意永恒 ✨",
    )

    # ── 中秋节（明月金桂）──────────────────────────────────
    H11 = make_style(
        name="中秋金辉", name_en="MidAutumn01",
        bg_grad=make_bg(["#FFF5E0","#FFE8B8","#FFD890","#FFC868","#FFB840"]),
        primary="#B06010", secondary="#C87820", accent="#E09030",
        text="#6B3A08", text_light="rgba(107,58,8,0.60)",
        card_bg="rgba(255,252,240,0.75)", card_border="rgba(200,120,48,0.42)",
        divider="🌕 · 🌙 · 🌕",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="34px", tag_bg="rgba(200,120,48,0.20)", tag_color="#B06010",
        card_radius="20px", decor="moon", greeting="中秋快乐",
        footer="月圆人圆，花好月圆 🌕",
    )

    H12 = make_style(
        name="中秋桂花", name_en="MidAutumn02",
        bg_grad=make_bg(["#FFF8F0","#FFEAD8","#FFDCC0","#FFCEA8","#FFC090"]),
        primary="#905020", secondary="#A86838", accent="#C08050",
        text="#5A3210", text_light="rgba(90,50,16,0.60)",
        card_bg="rgba(255,252,248,0.72)", card_border="rgba(168,104,56,0.45)",
        divider="🌸 · 🌙 · 🌸",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(168,104,56,0.18)", tag_color="#905020",
        card_radius="18px", decor="moon", greeting="花好月圆",
        footer="丹桂飘香，阖家团圆 🌸",
    )

    # ── 国庆节（红金璀璨）──────────────────────────────────
    H13 = make_style(
        name="国庆华彩", name_en="NationalDay01",
        bg_grad=make_bg(["#FFF8E8","#FFEAC0","#FFD898","#FFC670","#FFB448"]),
        primary="#B03010", secondary="#C84818", accent="#E06020",
        text="#6B1A08", text_light="rgba(107,26,8,0.60)",
        card_bg="rgba(255,252,240,0.75)", card_border="rgba(200,72,24,0.40)",
        divider="★ · ★ · ★",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(184,40,16,0.18)", tag_color="#B03010",
        card_radius="16px", decor="star", greeting="欢度国庆",
        footer="盛世华诞，锦绣中华 ★",
    )

    H14 = make_style(
        name="国庆金秋", name_en="NationalDay02",
        bg_grad=make_bg(["#FFF8E0","#FFE8B0","#FFD880","#FFC850","#FFB820"]),
        primary="#A07010", secondary="#B88820", accent="#D0A030",
        text="#5A4208", text_light="rgba(90,66,8,0.60)",
        card_bg="rgba(255,252,232,0.75)", card_border="rgba(192,136,32,0.42)",
        divider="🌾 · 🌾 · 🌾",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(176,136,32,0.18)", tag_color="#A07010",
        card_radius="18px", decor="grain", greeting="盛世华诞",
        footer="金秋十月，硕果累累 🌾",
    )

    # ── 重阳节（金菊敬老）──────────────────────────────────
    H15 = make_style(
        name="重阳金菊", name_en="DoubleNinth01",
        bg_grad=make_bg(["#FFF8E0","#FFE8B0","#FFD880","#FFC850","#FFB820"]),
        primary="#A07010", secondary="#B88820", accent="#D0A030",
        text="#5A4208", text_light="rgba(90,66,8,0.60)",
        card_bg="rgba(255,252,232,0.75)", card_border="rgba(208,160,48,0.42)",
        divider="🌻 · 🌻 · 🌻",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(176,136,32,0.18)", tag_color="#A07010",
        card_radius="16px", decor="chrysanthemum", greeting="重阳安康",
        footer="登高望远，福寿安康 🌻",
    )

    H16 = make_style(
        name="重阳秋韵", name_en="DoubleNinth02",
        bg_grad=make_bg(["#FFF0D8","#FFE4B8","#FFD898","#FFCC78","#FFC058"]),
        primary="#885020", secondary="#A06830", accent="#B88040",
        text="#5A3210", text_light="rgba(90,50,16,0.60)",
        card_bg="rgba(255,250,240,0.72)", card_border="rgba(176,128,64,0.42)",
        divider="🍂 · 🍁 · 🍂",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="30px", tag_bg="rgba(160,104,48,0.18)", tag_color="#885020",
        card_radius="16px", decor="maple", greeting="重阳敬老",
        footer="秋高气爽，敬老孝亲 🍂",
    )

    # ── 万圣节（南瓜紫夜）──────────────────────────────────
    H17 = make_style(
        name="万圣南瓜", name_en="Halloween01",
        bg_grad=make_bg(["#F0E8FF","#E0D0F0","#D0B8E0","#C0A0D0","#B088C0"]),
        primary="#7030A0", secondary="#8840B8", accent="#A050D0",
        text="#40186B", text_light="rgba(64,24,107,0.62)",
        card_bg="rgba(255,250,255,0.65)", card_border="rgba(160,80,208,0.48)",
        divider="🎃 · 🦇 · 🎃",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="30px", tag_bg="rgba(136,64,184,0.20)", tag_color="#7030A0",
        card_radius="16px", decor="pumpkin", greeting="Trick or Treat",
        footer="不给糖就捣蛋 🎃",
    )

    H18 = make_style(
        name="万圣夜紫", name_en="Halloween02",
        bg_grad=make_bg(["#F8F0FF","#EDD8F5","#E2C0EB","#D7A8E1","#CC90D7"]),
        primary="#6820A0", secondary="#8030B8", accent="#9840D0",
        text="#3A1060", text_light="rgba(58,16,96,0.62)",
        card_bg="rgba(255,252,255,0.65)", card_border="rgba(152,64,208,0.48)",
        divider="🦇 · ✨ · 🦇",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="30px", tag_bg="rgba(128,48,184,0.18)", tag_color="#6820A0",
        card_radius="16px", decor="halo", greeting="Happy Halloween",
        footer="神秘之夜，尽情捣蛋 🦇",
    )

    # ── 感恩节（枫叶暖橙）──────────────────────────────────
    H19 = make_style(
        name="感恩金秋", name_en="Thanksgiving01",
        bg_grad=make_bg(["#FFF5E8","#FFE8C8","#FFD8A8","#FFC888","#FFB868"]),
        primary="#9B4A10", secondary="#B06020", accent="#C87830",
        text="#6B2E08", text_light="rgba(107,46,8,0.60)",
        card_bg="rgba(255,250,240,0.72)", card_border="rgba(192,104,48,0.42)",
        divider="🍁 · 🍁 · 🍁",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(176,96,32,0.18)", tag_color="#9B4A10",
        card_radius="18px", decor="maple", greeting="感恩节快乐",
        footer="感恩有你，温暖同行 🍁",
    )

    H20 = make_style(
        name="感恩收获", name_en="Thanksgiving02",
        bg_grad=make_bg(["#F8F0E0","#F0E0C8","#E8D0B0","#E0C098","#D8B080"]),
        primary="#7B4818", secondary="#8F5A28", accent="#A36C38",
        text="#5A3010", text_light="rgba(90,48,16,0.60)",
        card_bg="rgba(255,252,240,0.70)", card_border="rgba(160,100,56,0.42)",
        divider="🌾 · 🍂 · 🌾",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="30px", tag_bg="rgba(143,90,40,0.18)", tag_color="#7B4818",
        card_radius="16px", decor="grain", greeting="感恩节快乐",
        footer="丰收喜悦，感恩有你 🌾",
    )

    # ── 圣诞节（红绿雪花）──────────────────────────────────
    H21 = make_style(
        name="圣诞红浆", name_en="Christmas01",
        bg_grad=make_bg(["#FFF0E8","#FFE0D0","#FFD0B8","#FFC0A0","#FFB088"]),
        primary="#A82020", secondary="#C03830", accent="#D85040",
        text="#6B1010", text_light="rgba(107,16,16,0.60)",
        card_bg="rgba(255,252,250,0.68)", card_border="rgba(192,48,48,0.42)",
        divider="🎄 · 🎄 · 🎄",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="34px", tag_bg="rgba(160,32,32,0.18)", tag_color="#A82020",
        card_radius="20px", decor="snow", greeting="圣诞快乐",
        footer="Merry Christmas 🎄",
    )

    H22 = make_style(
        name="圣诞雪夜", name_en="Christmas02",
        bg_grad=make_bg(["#EEF4FF","#D8E8FF","#C2DCFF","#ACD0FF","#96C4FF"]),
        primary="#1A4080", secondary="#2858A0", accent="#3870C0",
        text="#0E2448", text_light="rgba(14,36,72,0.62)",
        card_bg="rgba(255,255,255,0.68)", card_border="rgba(56,112,192,0.45)",
        divider="❄ · ❄ · ❄",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(40,88,160,0.18)", tag_color="#1A4080",
        card_radius="18px", decor="snow", greeting="圣诞快乐",
        footer="雪夜温暖，平安喜乐 ❄",
    )

    # ── 跨年夜 / 元旦（冰蓝极光）───────────────────────────
    H23 = make_style(
        name="跨年极光", name_en="NewYearEve",
        bg_grad=make_bg(["#EEF8FF","#D8EEFF","#C2E4FF","#ACDAFF","#96D0FF"]),
        primary="#1858A0", secondary="#2070B8", accent="#2888D0",
        text="#0E3468", text_light="rgba(14,52,104,0.62)",
        card_bg="rgba(255,255,255,0.70)", card_border="rgba(40,136,208,0.45)",
        divider="✨ · 🎆 · ✨",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="34px", tag_bg="rgba(32,112,184,0.18)", tag_color="#1858A0",
        card_radius="20px", decor="snow", greeting="新年快乐",
        footer="倒数跨年，未来可期 🎆",
    )

    H24 = make_style(
        name="元旦冰蓝", name_en="NewYearDay",
        bg_grad=make_bg(["#F0F8FF","#DDEEFF","#CAE4FF","#B7DAFF","#A4D0FF"]),
        primary="#1A4898", secondary="#225EAC", accent="#2874C0",
        text="#0E2A60", text_light="rgba(14,42,96,0.62)",
        card_bg="rgba(255,255,255,0.72)", card_border="rgba(40,116,192,0.45)",
        divider="🎉 · 🎉 · 🎉",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="34px", tag_bg="rgba(34,94,172,0.18)", tag_color="#1A4898",
        card_radius="20px", decor="sparkle", greeting="元旦快乐",
        footer="万象更新，幸福安康 🎉",
    )

    # ── 情人节（玫红爱心）──────────────────────────────────
    H25 = make_style(
        name="情人玫红", name_en="Valentine01",
        bg_grad=make_bg(["#FFF5F8","#FFE8EE","#FFD8E4","#FFC8DA","#FFB8D0"]),
        primary="#C02060", secondary="#D83878", accent="#F05090",
        text="#780E38", text_light="rgba(120,14,56,0.62)",
        card_bg="rgba(255,255,255,0.62)", card_border="rgba(240,80,144,0.52)",
        divider="💕 · 💕 · 💕",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="34px", tag_bg="rgba(216,56,120,0.18)", tag_color="#C02060",
        card_radius="20px", decor="heart", greeting="情人节快乐",
        footer="有你是缘，甜满心间 💕",
    )

    H26 = make_style(
        name="情人粉紫", name_en="Valentine02",
        bg_grad=make_bg(["#FFF5FF","#FFE8FF","#FFD8FF","#FFC8FF","#FFB8FF"]),
        primary="#9820B0", secondary="#B038C8", accent="#C850E0",
        text="#580C68", text_light="rgba(88,12,104,0.62)",
        card_bg="rgba(255,255,255,0.62)", card_border="rgba(200,80,224,0.52)",
        divider="🌹 · 💕 · 🌹",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(176,56,200,0.18)", tag_color="#9820B0",
        card_radius="18px", decor="heart", greeting="浪漫相随",
        footer="爱在今朝，岁月静好 🌹",
    )

    # ── 妇女节（粉色花瓣）──────────────────────────────────
    H27 = make_style(
        name="妇女节花", name_en="WomensDay01",
        bg_grad=make_bg(["#FFF8F5","#FFE8F0","#FFD8EB","#FFC8E6","#FFB8E1"]),
        primary="#9838A0", secondary="#B048B8", accent="#C858D0",
        text="#5C2068", text_light="rgba(92,32,104,0.62)",
        card_bg="rgba(255,255,255,0.62)", card_border="rgba(200,88,208,0.52)",
        divider="🌸 · 🌸 · 🌸",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(176,72,184,0.18)", tag_color="#9838A0",
        card_radius="20px", decor="cherry", greeting="妇女节快乐",
        footer="致敬她力量，岁月无恙 🌸",
    )

    H27B = make_style(
        name="妇女节紫", name_en="WomensDay02",
        bg_grad=make_bg(["#F8F0FF","#F0E8FF","#E8E0FF","#E0D8FF","#D8D0FF"]),
        primary="#6040B8", secondary="#7050C8", accent="#8060D8",
        text="#2C1860", text_light="rgba(44,24,96,0.62)",
        card_bg="rgba(255,255,255,0.62)", card_border="rgba(128,96,216,0.50)",
        divider="💐 · 💐 · 💐",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(112,80,200,0.18)", tag_color="#6040B8",
        card_radius="20px", decor="lavender", greeting="致敬女神",
        footer="优雅如你，璀璨如光 💐",
    )

    # ── 劳动节（深蓝麦穗）──────────────────────────────────
    H28 = make_style(
        name="劳动赞歌", name_en="LaborDay01",
        bg_grad=make_bg(["#EEF4FF","#D8E8FF","#C2DCFF","#ACD0FF","#96C4FF"]),
        primary="#1A4898", secondary="#2058B0", accent="#2868C8",
        text="#0E2C60", text_light="rgba(14,44,96,0.62)",
        card_bg="rgba(255,255,255,0.70)", card_border="rgba(40,104,200,0.45)",
        divider="⚙ · ⚙ · ⚙",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(32,88,168,0.18)", tag_color="#1A4898",
        card_radius="16px", decor="grain", greeting="劳动最光荣",
        footer="匠心筑梦，劳动最美 ⚙",
    )

    H28B = make_style(
        name="劳动金秋", name_en="LaborDay02",
        bg_grad=make_bg(["#FFF8F0","#FFE8D8","#FFD8C0","#FFC8A8","#FFB890"]),
        primary="#A06010", secondary="#B07020", accent="#C08030",
        text="#5A3010", text_light="rgba(90,48,16,0.60)",
        card_bg="rgba(255,255,255,0.65)", card_border="rgba(192,128,48,0.50)",
        divider="🌾 · 🌾 · 🌾",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(160,96,16,0.18)", tag_color="#A06010",
        card_radius="16px", decor="grain", greeting="致敬劳动者",
        footer="平凡伟大，劳动最美 🌾",
    )

    # ── 儿童节（彩虹气球）──────────────────────────────────
    H29 = make_style(
        name="儿童彩虹", name_en="ChildrensDay",
        bg_grad=make_bg(["#FFF8F0","#FFE8E0","#FFD8D0","#FFC8C0","#FFB8B0"]),
        primary="#E03010", secondary="#F04820", accent="#FF6030",
        text="#6B1808", text_light="rgba(107,24,8,0.60)",
        card_bg="rgba(255,255,255,0.65)", card_border="rgba(255,96,48,0.48)",
        divider="🎈 · 🎈 · 🎈",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="34px", tag_bg="rgba(240,72,32,0.18)", tag_color="#E03010",
        card_radius="20px", decor="balloon", greeting="儿童节快乐",
        footer="童心永驻，梦想飞扬 🎈",
    )

    H30 = make_style(
        name="儿童彩虹02", name_en="ChildrensDay02",
        bg_grad=make_bg(["#F8F0FF","#EDE0FF","#E2D0FF","#D7C0FF","#CCB0FF"]),
        primary="#5020B0", secondary="#6030C8", accent="#7040E0",
        text="#280C68", text_light="rgba(40,12,104,0.62)",
        card_bg="rgba(255,255,255,0.62)", card_border="rgba(112,64,224,0.50)",
        divider="🌈 · 🌈 · 🌈",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(96,48,200,0.18)", tag_color="#5020B0",
        card_radius="18px", decor="sparkle", greeting="童心未泯",
        footer="世界很酷，保持好奇 🌈",
    )

    # ── 教师节（暖棕书香）──────────────────────────────────
    H31 = make_style(
        name="教师书香", name_en="TeachersDay01",
        bg_grad=make_bg(["#FFF5EC","#FFE8D8","#FFD8C4","#FFC8B0","#FFB89C"]),
        primary="#7B3A10", secondary="#8F4C20", accent="#A35E30",
        text="#5A2410", text_light="rgba(90,36,16,0.60)",
        card_bg="rgba(255,250,244,0.72)", card_border="rgba(160,80,48,0.42)",
        divider="📚 · 📖 · 📚",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(143,76,32,0.18)", tag_color="#7B3A10",
        card_radius="16px", decor="chrysanthemum", greeting="教师节快乐",
        footer="师恩如山，桃李芬芳 📚",
    )

    H32 = make_style(
        name="教师向阳", name_en="TeachersDay02",
        bg_grad=make_bg(["#FFF8E0","#FFEAB0","#FFDC80","#FFCE50","#FFC020"]),
        primary="#A06808", secondary="#B88010", accent="#D09818",
        text="#5A4208", text_light="rgba(90,66,8,0.60)",
        card_bg="rgba(255,252,232,0.75)", card_border="rgba(192,136,24,0.42)",
        divider="🌻 · 🌻 · 🌻",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(176,128,24,0.18)", tag_color="#A06808",
        card_radius="18px", decor="sunflower", greeting="桃李天下",
        footer="感谢恩师，一路有你 🌻",
    )



    # ── 春节第三天（正月初三）────────────────────────────────
    H33 = make_style(
        name="正月初三", name_en="SpringFestival03",
        bg_grad=make_bg(["#FFF0E8","#FFD8C8","#FFC0A8","#FFA888","#FF9068"]),
        primary="#B03010", secondary="#C84020", accent="#D85830",
        text="#6B1808", text_light="rgba(107,24,8,0.62)",
        card_bg="rgba(255,248,240,0.72)", card_border="rgba(216,88,48,0.48)",
        divider="🧧 · 🏮 · 🧧",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(184,48,16,0.18)", tag_color="#B03010",
        card_radius="16px", decor="coin", greeting="初三开年",
        footer="迎春纳福，年味正浓 🧧",
    )

    # ── 春节第四天（正月初四）────────────────────────────────
    H34 = make_style(
        name="正月初四", name_en="SpringFestival04",
        bg_grad=make_bg(["#FFF8F0","#FFECD8","#FFE0C0","#FFD4A8","#FFC890"]),
        primary="#9B5010", secondary="#B06818", accent="#C88020",
        text="#6B3C08", text_light="rgba(107,60,8,0.62)",
        card_bg="rgba(255,252,244,0.72)", card_border="rgba(200,128,32,0.42)",
        divider="🏮 · ✨ · 🏮",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(160,88,16,0.18)", tag_color="#9B5010",
        card_radius="16px", decor="sparkle", greeting="灶神归位",
        footer="灶王保佑，福气临门 🏮",
    )

    # ── 春节第五天（正月初五）────────────────────────────────
    H35 = make_style(
        name="正月初五", name_en="SpringFestival05",
        bg_grad=make_bg(["#FFF5F0","#FFE8D8","#FFD8C0","#FFC8A8","#FFB890"]),
        primary="#C04010", secondary="#D05820", accent="#E07030",
        text="#782808", text_light="rgba(120,40,8,0.62)",
        card_bg="rgba(255,252,248,0.72)", card_border="rgba(224,112,48,0.44)",
        divider="🧧 · 🧧 · 🧧",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(192,64,16,0.18)", tag_color="#C04010",
        card_radius="16px", decor="coin", greeting="迎财神",
        footer="财源广进，金玉满堂 🧧",
    )

    # ── 春节第六天（正月初六）────────────────────────────────
    H36 = make_style(
        name="正月初六", name_en="SpringFestival06",
        bg_grad=make_bg(["#F8F0FF","#E8D8FF","#D8C0FF","#C8A8FF","#B890FF"]),
        primary="#7030B8", secondary="#8848C8", accent="#A060D8",
        text="#3C1068", text_light="rgba(60,16,104,0.62)",
        card_bg="rgba(255,252,255,0.72)", card_border="rgba(160,96,216,0.50)",
        divider="✨ · 🏮 · ✨",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(112,72,184,0.18)", tag_color="#7030B8",
        card_radius="16px", decor="sparkle", greeting="六六大顺",
        footer="顺风顺水，好运连连 ✨",
    )

    # ── 春节第七天（正月初七）────────────────────────────────
    H37 = make_style(
        name="正月初七", name_en="SpringFestival07",
        bg_grad=make_bg(["#F0F8F8","#D8F0F0","#C0E8E8","#A8E0E0","#90D8D8"]),
        primary="#206868", secondary="#387878", accent="#508888",
        text="#0E3838", text_light="rgba(14,56,56,0.62)",
        card_bg="rgba(255,255,255,0.68)", card_border="rgba(80,136,136,0.48)",
        divider="🌱 · 🌿 · 🌱",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(56,120,120,0.18)", tag_color="#206868",
        card_radius="16px", decor="grass", greeting="人日快乐",
        footer="人日登高，福寿安康 🌱",
    )

    # ── 元宵节（共用 H03 H04）──────────────────────────────
    # H03="元宵灯彩"，H04="元宵星夜"（已在上方定义）

    # ── 情人节（共用 H25 H26）─────────────────────────────
    # H25="情人玫红"，H26="情人粉紫"（已在上方定义）

    # ── 清明节第三天────────────────────────────────────────
    H38 = make_style(
        name="清明踏青", name_en="Qingming03",
        bg_grad=make_bg(["#F4F8F0","#E0F0D8","#CCE8C0","#B8E0A8","#A4D890"]),
        primary="#3A6830", secondary="#487840", accent="#588850",
        text="#1E3C18", text_light="rgba(30,60,24,0.62)",
        card_bg="rgba(255,255,248,0.72)", card_border="rgba(88,136,80,0.48)",
        divider="🌸 · 🌿 · 🌸",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="30px", tag_bg="rgba(72,120,64,0.18)", tag_color="#3A6830",
        card_radius="16px", decor="maple", greeting="清明踏青",
        footer="春光明媚，诗意盎然 🌸",
    )

    # ── 端午节第三天────────────────────────────────────────
    H39 = make_style(
        name="端午龙舟", name_en="DragonBoat03",
        bg_grad=make_bg(["#EEF4F8","#D8E8F0","#C2DCE8","#ACD0E0","#96C4D8"]),
        primary="#2A5070", secondary="#386080", accent="#467090",
        text="#0E2840", text_light="rgba(14,40,64,0.62)",
        card_bg="rgba(255,255,255,0.68)", card_border="rgba(70,112,144,0.48)",
        divider="🐉 · 🫔 · 🐉",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(56,96,128,0.18)", tag_color="#2A5070",
        card_radius="14px", decor="waves", greeting="龙舟竞渡",
        footer="百舸争流，端午安康 🐉",
    )

    # ── 劳动节第三天────────────────────────────────────────
    H40 = make_style(
        name="劳动欢歌", name_en="LaborDay03",
        bg_grad=make_bg(["#F0F8F0","#D8F0D8","#C0E8C0","#A8E0A8","#90D890"]),
        primary="#286030", secondary="#387840", accent="#489050",
        text="#1A3C1C", text_light="rgba(26,60,28,0.62)",
        card_bg="rgba(255,255,255,0.70)", card_border="rgba(72,144,80,0.45)",
        divider="⚙ · 🌾 · ⚙",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(56,120,64,0.18)", tag_color="#286030",
        card_radius="16px", decor="grain", greeting="劳动快乐",
        footer="辛勤耕耘，收获满满 ⚙",
    )

    # ── 劳动节第四天────────────────────────────────────────
    H41 = make_style(
        name="劳动赞歌02", name_en="LaborDay04",
        bg_grad=make_bg(["#F8F0E8","#F0E0D0","#E8D0B8","#E0C0A0","#D8B088"]),
        primary="#7B4818", secondary="#8F5C28", accent="#A37038",
        text="#5C3010", text_light="rgba(92,48,16,0.60)",
        card_bg="rgba(255,252,248,0.68)", card_border="rgba(160,112,56,0.45)",
        divider="🌾 · ⚙ · 🌾",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(143,92,32,0.18)", tag_color="#7B4818",
        card_radius="16px", decor="grain", greeting="匠心闪耀",
        footer="平凡岗位，不凡坚守 🌾",
    )

    # ── 劳动节第五天────────────────────────────────────────
    H42 = make_style(
        name="劳动收官", name_en="LaborDay05",
        bg_grad=make_bg(["#F0F8FF","#D8ECFF","#C0E0FF","#A8D4FF","#90C8FF"]),
        primary="#1A50A0", secondary="#2060B8", accent="#2870D0",
        text="#0E2C68", text_light="rgba(14,44,104,0.62)",
        card_bg="rgba(255,255,255,0.70)", card_border="rgba(40,112,208,0.45)",
        divider="⚙ · ✨ · ⚙",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(32,96,176,0.18)", tag_color="#1A50A0",
        card_radius="16px", decor="sparkle", greeting="致敬最美",
        footer="劳动有你，精彩继续 ⚙",
    )

    # ── 儿童节（共用 H29 H30）─────────────────────────────
    # H29="儿童彩虹"，H30="儿童彩虹02"（已在上方定义）

    # ── 七夕节（共用 H09 H10）──────────────────────────────
    # H09="七夕粉缘Qixi01"，H10="七夕星河Qixi02"（已在上方定义）

    # ── 教师节（共用 H31 H32）─────────────────────────────
    # H31="教师书香"，H32="教师向阳"（已在上方定义）

    # ── 中秋节（共用 H11 H12）─────────────────────────────
    # H11="中秋金辉"，H12="中秋玉兔"（已在上方定义）

    # ── 重阳节（共用 H15 H16）─────────────────────────────
    # H15="重阳金秋"，H16="重阳丹桂"（已在上方定义）

    # ── 万圣节（共用 H17 H18）─────────────────────────────
    # H17="万圣南瓜"，H18="万圣暗夜"（已在上方定义）

    # ── 感恩节（共用 H19 H20）─────────────────────────────
    # H19="感恩节火鸡"，H20="感恩节南瓜"（已在上方定义）

    # ── 圣诞节（共用 H21 H22）─────────────────────────────
    # H21="圣诞红装"，H22="圣诞雪夜"（已在上方定义）

    # ── 跨年/元旦（共用 H23 H24）─────────────────────────
    # H23="新年红韵"，H24="新年愿望"（已在上方定义）

    # ── 国庆第三天────────────────────────────────────────
    H45 = make_style(
        name="国庆吉日", name_en="NationalDay03",
        bg_grad=make_bg(["#FFF0E8","#FFDED0","#FFCCBC","#FFBAA8","#FFA894"]),
        primary="#C03818", secondary="#D45028", accent="#E86838",
        text="#781C08", text_light="rgba(120,28,8,0.62)",
        card_bg="rgba(255,252,248,0.72)", card_border="rgba(224,88,48,0.44)",
        divider="🏮 · 🇨🇳 · 🏮",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(192,56,24,0.18)", tag_color="#C03818",
        card_radius="16px", decor="lantern", greeting="锦绣中华",
        footer="山河壮丽，共庆华诞 🏮",
    )

    # ── 国庆第四天────────────────────────────────────────
    H46 = make_style(
        name="国庆金秋", name_en="NationalDay04",
        bg_grad=make_bg(["#F8F0D8","#F0E0B8","#E8D098","#E0C078","#D8B058"]),
        primary="#906010", secondary="#A87818", accent="#C09020",
        text="#5C4408", text_light="rgba(92,68,8,0.60)",
        card_bg="rgba(255,252,236,0.72)", card_border="rgba(192,144,32,0.42)",
        divider="🌾 · 🇨🇳 · 🌾",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(160,96,16,0.18)", tag_color="#906010",
        card_radius="16px", decor="grain", greeting="盛世华章",
        footer="金秋送爽，福满人间 🌾",
    )

    # ── 国庆第五天────────────────────────────────────────
    H47 = make_style(
        name="国庆团圆", name_en="NationalDay05",
        bg_grad=make_bg(["#F8F4F0","#F0E8E0","#E8DCD0","#E0D0C0","#D8C4B0"]),
        primary="#8B6848", secondary="#A07C60", accent="#B59078",
        text="#5C4838", text_light="rgba(92,72,56,0.60)",
        card_bg="rgba(255,252,248,0.68)", card_border="rgba(176,144,120,0.44)",
        divider="🏮 · 🏠 · 🏮",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(140,100,64,0.18)", tag_color="#8B6848",
        card_radius="16px", decor="lantern", greeting="家国同庆",
        footer="家和万事，国泰民安 🏮",
    )

    # ── 国庆第六天────────────────────────────────────────
    H48 = make_style(
        name="国庆静好", name_en="NationalDay06",
        bg_grad=make_bg(["#EEF4F0","#D8E8E0","#C2DCD0","#ACD0C0","#96C4B0"]),
        primary="#386858", secondary="#487868", accent="#588878",
        text="#1E3830", text_light="rgba(30,56,48,0.62)",
        card_bg="rgba(255,255,252,0.68)", card_border="rgba(88,136,120,0.48)",
        divider="🌿 · 🇨🇳 · 🌿",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(72,112,96,0.18)", tag_color="#386858",
        card_radius="16px", decor="grass", greeting="岁月静好",
        footer="安然自在，诗意生活 🌿",
    )

    # ── 国庆第七天────────────────────────────────────────
    H49 = make_style(
        name="国庆流金", name_en="NationalDay07",
        bg_grad=make_bg(["#FFF8F0","#FFECD8","#FFE0C0","#FFD4A8","#FFC890"]),
        primary="#A06810", secondary="#B88018", accent="#D09820",
        text="#6B4808", text_light="rgba(107,72,8,0.60)",
        card_bg="rgba(255,252,240,0.72)", card_border="rgba(192,136,32,0.42)",
        divider="✨ · 🏮 · ✨",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(160,96,16,0.18)", tag_color="#A06810",
        card_radius="16px", decor="sparkle", greeting="金色华章",
        footer="流金岁月，与国同庆 ✨",
    )

    # ── 国庆第八天────────────────────────────────────────
    H50 = make_style(
        name="国庆收官", name_en="NationalDay08",
        bg_grad=make_bg(["#F0F0F8","#DCDCE8","#C8C8D8","#B4B4C8","#A0A0B8"]),
        primary="#3A4868", secondary="#4A5878", accent="#5A6888",
        text="#1E2C40", text_light="rgba(30,44,64,0.62)",
        card_bg="rgba(255,255,255,0.68)", card_border="rgba(90,104,136,0.48)",
        divider="🌙 · 🇨🇳 · 🌙",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(74,88,120,0.18)", tag_color="#3A4868",
        card_radius="16px", decor="sparkle", greeting="与国同欢",
        footer="明日再出发，奋斗正当时 🌙",
    )

    # ── 妇女节第三版───────────────────────────────────────
    H51 = make_style(
        name="妇女节紫罗", name_en="WomensDay03",
        bg_grad=make_bg(["#FFF5F8","#FFE8F0","#FFD8E8","#FFC8E0","#FFB8D8"]),
        primary="#A03080", secondary="#B84098", accent="#CC50B0",
        text="#6C1858", text_light="rgba(108,24,88,0.62)",
        card_bg="rgba(255,255,255,0.62)", card_border="rgba(200,80,176,0.52)",
        divider="🌺 · 🌸 · 🌺",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(176,56,144,0.18)", tag_color="#A03080",
        card_radius="20px", decor="cherry", greeting="如花绽放",
        footer="温柔且坚，闪闪发光 🌺",
    )

    # ── 元旦第二天（1月2日）───────────────────────────────
    H52 = make_style(
        name="元旦欢庆", name_en="NewYearDay02",
        bg_grad=make_bg(["#FFF8F0","#FFECD8","#FFE0C0","#FFD4A8","#FFC890"]),
        primary="#A06010", secondary="#B87818", accent="#CC9020",
        text="#6B4808", text_light="rgba(107,72,8,0.60)",
        card_bg="rgba(255,252,240,0.72)", card_border="rgba(192,136,32,0.42)",
        divider="🎉 · 🎊 · 🎉",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(160,96,16,0.18)", tag_color="#A06010",
        card_radius="18px", decor="sparkle", greeting="新年快乐",
        footer="好事发生，幸福绵长 🎉",
    )

    # ── 除夕（12月31日跨年夜）────────────────────────────
    H53 = make_style(
        name="除夕守岁", name_en="NewYearEve02",
        bg_grad=make_bg(["#F8F0FF","#E8D8FF","#D8C0FF","#C8A8FF","#B890FF"]),
        primary="#6020A0", secondary="#7838B8", accent="#9050D0",
        text="#380C60", text_light="rgba(56,12,96,0.62)",
        card_bg="rgba(255,252,255,0.62)", card_border="rgba(144,80,208,0.52)",
        divider="🌟 · 🎆 · 🌟",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(112,56,176,0.18)", tag_color="#6020A0",
        card_radius="18px", decor="sparkle", greeting="守岁迎新",
        footer="爆竹声中，辞旧迎新 🌟",
    )


    # ── 调休上班日风格（节假日调休补班）───────────────────
    H54 = make_style(
        name="补班提醒", name_en="HolidayWorkday",
        bg_grad=make_bg(["#EEF4FF","#D8E8FF","#C2DCFF","#ACD0FF","#96C4FF"]),
        primary="#1A4898", secondary="#2058B0", accent="#2868C8",
        text="#0E2C60", text_light="rgba(14,44,96,0.62)",
        card_bg="rgba(255,255,255,0.70)", card_border="rgba(40,104,200,0.45)",
        divider="⚙ · ⚙ · ⚙",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(32,88,168,0.18)", tag_color="#1A4898",
        card_radius="16px", decor="grain", greeting="调休补班",
        footer="记得限号，安全出行 ⚙",
    )

    H55 = make_style(
        name="补班提醒02", name_en="HolidayWorkday02",
        bg_grad=make_bg(["#F0F8FF","#D8ECFF","#C0E0FF","#A8D4FF","#90C8FF"]),
        primary="#1A50A0", secondary="#2060B8", accent="#2870D0",
        text="#0E2C68", text_light="rgba(14,44,104,0.62)",
        card_bg="rgba(255,255,255,0.70)", card_border="rgba(40,112,208,0.45)",
        divider="📅 · 📅 · 📅",
        greeting_font=FONT_DISPLAY, body_font=FONT_SERIF, label_font=FONT_SANS,
        greeting_size="32px", tag_bg="rgba(32,96,176,0.18)", tag_color="#1A50A0",
        card_radius="16px", decor="sparkle", greeting="补班日",
        footer="调整作息，迎接明天 📅",
    )

# ============================================================
# 主题列表 & 节日判断
# ============================================================

REGULAR_STYLES = [
    S.S01, S.S02, S.S03, S.S04, S.S05, S.S06, S.S07, S.S08, S.S09,
    S.S10, S.S11, S.S12, S.S13, S.S14, S.S15, S.S16, S.S17, S.S18,
    S.S19, S.S20, S.S21, S.S22, S.S23, S.S24, S.S25, S.S26, S.S27, S.S28,
    S.S29, S.S30, S.S31, S.S32, S.S33, S.S34, S.S35, S.S36,
    S.S37, S.S38, S.S39, S.S40, S.S41, S.S42, S.S43, S.S44, S.S45,
    S.S46, S.S47, S.S48,
    S.S49, S.S50, S.S51, S.S52, S.S53, S.S54, S.S55, S.S56, S.S57,
    S.S58, S.S59, S.S60, S.S61, S.S62, S.S63, S.S64, S.S65, S.S66,
    S.S67, S.S68, S.S69, S.S70, S.S71, S.S72,
]

HOLIDAY_STYLES = [
    # 春节（7天）
    H.H01, H.H02, H.H33, H.H34, H.H35, H.H36, H.H37,
    # 元宵（2天）
    H.H03, H.H04,
    # 清明（3天）
    H.H05, H.H06, H.H38,
    # 端午（3天）
    H.H07, H.H08, H.H39,
    # 国庆（8天）
    H.H13, H.H14, H.H45, H.H46, H.H47, H.H48, H.H49, H.H50,
    # 重阳（2天）
    H.H15, H.H16,
    # 万圣（2天）
    H.H17, H.H18,
    # 感恩（2天）
    H.H19, H.H20,
    # 圣诞（2天）
    H.H21, H.H22,
    # 元旦（2天）
    H.H23, H.H24, H.H52,
    # 情人节（2天）
    H.H25, H.H26,
    # 妇女节（3天）
    H.H27, H.H27B, H.H51,
    # 劳动节（5天）
    H.H28, H.H28B, H.H40, H.H41, H.H42,
    # 儿童节（2天）
    H.H29, H.H30,
    # 七夕（2天，使用 H09 H10）
    H.H09, H.H10,
    # 教师节（2天）
    H.H31, H.H32,
    # 中秋（2天）
    H.H11, H.H12,
    # 除夕（1天）
    H.H53,
    # 调休补班日（2天）
    H.H54, H.H55,
]

ALL_STYLES = HOLIDAY_STYLES + REGULAR_STYLES


def get_style_for_date(date=None):
    """根据日期返回对应主题（节日期间返回节日主题）"""
    if date is None:
        date = bj_date()
    if is_holiday(date):
        styles = get_holiday_styles(date)
        if styles:
            return styles[0]
        return HOLIDAY_STYLES[0]
    day_of_year = (date - datetime.date(date.year, 1, 1)).days + 1
    idx = (day_of_year - 1) % len(REGULAR_STYLES)
    return REGULAR_STYLES[idx]


def get_holiday_styles(date=None):
    """获取某日期对应的节日主题列表（1-2个），用于节日期间同时推送多款供选择"""
    if date is None:
        date = bj_date()
    if not is_holiday(date):
        return []
    
    m, d = date.month, date.day
    
    # 定义节日主题对
    holiday_pairs = {
        # 春节
        (1, 28): [H.H01, H.H02],
        (1, 29): [H.H01, H.H02],
        # 元宵
        (2, 12): [H.H03, H.H04],
        (2, 13): [H.H03, H.H04],
        # 情人节
        (2, 14): [H.H25, H.H26],
        # 妇女节
        (3, 8): [H.H27, H.H27B],
        # 清明
        (4, 5): [H.H05, H.H06],
        (4, 6): [H.H05, H.H06],
        # 劳动节
        (5, 1): [H.H28, H.H28B],
        # 端午
        (5, 31): [H.H07, H.H08],
        # 儿童节
        (6, 1): [H.H29, H.H30],
        # 七夕
        (8, 25): [H.H09, H.H10],
        # 教师节
        (9, 10): [H.H31, H.H32],
        # 中秋
        (9, 28): [H.H11, H.H12],
        # 国庆
        (10, 1): [H.H13, H.H14],
        # 重阳
        (10, 11): [H.H15, H.H16],
        # 万圣
        (10, 31): [H.H17, H.H18],
        # 感恩节
        (11, 24): [H.H19, H.H20],
        # 圣诞节
        (12, 25): [H.H21, H.H22],
        # 元旦
        (12, 31): [H.H23, H.H24],
    }
    
    return holiday_pairs.get((m, d), [HOLIDAY_STYLES[0]])


# ──────────────────────────────────────────────────────────────────
# 全局节假日映射：每个日期 → (style_name, 节假日名)
# 2026年节假日方案：
#   春节 1/28-2/3（7天），清明 4/4-4/6（3天），劳动节 5/1-5/5（5天）
#   端午 6/27-6/29（3天），中秋+国庆 10/1-10/8（8天）
# ──────────────────────────────────────────────────────────────────
_HOLIDAY_MAP = {
    # 元旦
    (1, 1): ('NewYearDay', '元旦'),    (1, 2): ('NewYearDay02', '元旦'),
    # 春节（7天）
    (1, 28): ('SpringFestival01', '春节'), (1, 29): ('SpringFestival02', '春节'),
    (1, 30): ('SpringFestival03', '春节'), (1, 31): ('SpringFestival04', '春节'),
    (2, 1):  ('SpringFestival05', '春节'), (2, 2):  ('SpringFestival06', '春节'),
    (2, 3):  ('SpringFestival07', '春节'),
    # 元宵
    (2, 12): ('Lantern01', '元宵节'),  (2, 13): ('Lantern02', '元宵节'),
    # 情人节
    (2, 14): ('Valentine01', '情人节'),
    # 妇女节
    (3, 8):  ('WomensDay01', '妇女节'),  (3, 9):  ('WomensDay03', '妇女节'),
    # 清明（3天）
    (4, 4): ('Qingming01', '清明'),    (4, 5): ('Qingming02', '清明'),
    (4, 6): ('Qingming03', '清明'),
    # 劳动节（5天）
    (5, 1):  ('LaborDay01', '劳动节'),  (5, 2):  ('LaborDay02', '劳动节'),
    (5, 3):  ('LaborDay03', '劳动节'),  (5, 4):  ('LaborDay04', '劳动节'),
    (5, 5):  ('LaborDay05', '劳动节'),
    # 儿童节
    (6, 1):  ('ChildrensDay', '儿童节'),
    # 端午（3天）
    (6, 27): ('DragonBoat01', '端午'), (6, 28): ('DragonBoat02', '端午'),
    (6, 29): ('DragonBoat03', '端午'),
    # 七夕（2天）
    (8, 25): ('Qixi01', '七夕节'),
    # 教师节
    (9, 10): ('TeachersDay01', '教师节'),
    # 中秋+国庆（9/28补班，10/1-10/8放假，10/10补班）
    (9, 28): ('HolidayWorkday', '中秋'),
    (10, 1): ('NationalDay01', '国庆'), (10, 2): ('NationalDay02', '国庆'),
    (10, 3): ('NationalDay03', '国庆'), (10, 4): ('NationalDay04', '国庆'),
    (10, 5): ('NationalDay05', '国庆'), (10, 6): ('NationalDay06', '国庆'),
    (10, 7): ('NationalDay07', '国庆'), (10, 8): ('NationalDay08', '国庆'),
    (10, 10): ('HolidayWorkday02', '国庆'),
    # 重阳
    (10, 11): ('DoubleNinth01', '重阳节'),
    # 万圣
    (10, 31): ('Halloween01', '万圣节'),
    # 感恩
    (11, 24): ('Thanksgiving01', '感恩节'),
    # 圣诞
    (12, 25): ('Christmas01', '圣诞节'),
    # 除夕
    (12, 31): ('NewYearEve', '除夕'),
}


def get_style_by_name(name):
    """根据 style name_en 查找 H 风格对象"""
    try:
        from styles_72 import H
        return getattr(H, name)
    except (ImportError, AttributeError):
        # Fallback: scan HOLIDAY_STYLES
        from styles_72 import HOLIDAY_STYLES
        for s in HOLIDAY_STYLES:
            if s.get('name_en') == name:
                return s
        return HOLIDAY_STYLES[0]


def is_holiday(date=None):
    """判断是否为节假日（含调休上班日）"""
    if date is None:
        date = bj_date()
    return (date.month, date.day) in _HOLIDAY_MAP


def get_holiday_name(date=None):
    """获取节假日名称（如'春节'、'清明'）"""
    if date is None:
        date = bj_date()
    info = _HOLIDAY_MAP.get((date.month, date.day))
    return info[1] if info else ''


def get_holiday_style_name(date=None):
    """获取节假日对应的 style name_en"""
    if date is None:
        date = bj_date()
    info = _HOLIDAY_MAP.get((date.month, date.day))
    return info[0] if info else ''


def get_style_for_date(date=None):
    """根据日期返回主题：节假日→节日风格，工作日→轮换常规风格"""
    if date is None:
        date = bj_date()
    if is_holiday(date):
        return get_style_by_name(get_holiday_style_name(date))
    day_of_year = (date - datetime.date(date.year, 1, 1)).days + 1
    idx = (day_of_year - 1) % len(REGULAR_STYLES)
    return REGULAR_STYLES[idx]


def get_holiday_styles(date=None):
    """返回该日期对应的节日风格列表（节假日=1个；非节日=空列表）"""
    if date is None:
        date = bj_date()
    if not is_holiday(date):
        return []
    return [get_style_by_name(get_holiday_style_name(date))]
