"""
图片生成模块 - 72 风格日签系统
- 常规主题：72种（S01-S72，按一年中第几天轮换，两个多月不重样）
- 节日主题：24种（H01-H24，节日期间优先使用，独立于常规主题之外）
- 背景/配色/装饰全部预设，不使用网搜图片
"""

import os
import sys
import io

# 修复 Windows 控制台 GBK 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import datetime
import tempfile
import random

# 导入72风格系统
from styles_72 import (
    S, H, REGULAR_STYLES, HOLIDAY_STYLES, ALL_STYLES,
    get_style_for_date, is_holiday, get_holiday_styles,
    LOGO_XIATIANKANG, select_logo_by_style, weather_icon
)






# ============================================================
# 干净清爽的装饰 SVG（无杂乱圆点）
# ============================================================
def get_decoration(decor_type, style):
    """根据装饰类型生成对应的 SVG"""
    p = style["primary"]
    s = style["secondary"]
    a = style["accent"]
    t = style["text_light"]

    def rg(clr, op):
        return f"rgba{tuple(int(clr.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (op,)}"

    svgs = {
        # ── 玫瑰花瓣 ──
        "roses": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="50" cy="60" rx="55" ry="45" fill="{rg(p,0.08)}" transform="rotate(-20,50,60)"/>
      <ellipse cx="80" cy="40" rx="40" ry="50" fill="{rg(a,0.06)}" transform="rotate(15,80,40)"/>
      <ellipse cx="35" cy="100" rx="35" ry="45" fill="{rg(s,0.05)}" transform="rotate(-35,35,100)"/>
      <path d="M50 130 Q55 170 45 210" stroke="{rg(a,0.08)}" stroke-width="1.5" fill="none"/>
      <ellipse cx="65" cy="165" rx="18" ry="9" fill="{rg(s,0.06)}" transform="rotate(-30,65,165)"/>
      <circle cx="50" cy="60" r="7" fill="{rg(a,0.10)}"/>
      <ellipse cx="700" cy="100" rx="60" ry="48" fill="{rg(s,0.07)}" transform="rotate(20,700,100)"/>
      <ellipse cx="680" cy="70" rx="42" ry="52" fill="{rg(a,0.06)}" transform="rotate(-10,680,70)"/>
      <ellipse cx="730" cy="130" rx="38" ry="38" fill="{rg(p,0.05)}"/>
      <circle cx="700" cy="100" r="8" fill="{rg(a,0.09)}"/>
      <ellipse cx="700" cy="950" rx="80" ry="60" fill="{rg(a,0.07)}" transform="rotate(10,700,950)"/>
      <ellipse cx="50" cy="850" rx="60" ry="48" fill="{rg(s,0.06)}" transform="rotate(-15,50,850)"/>
    </svg>""",

        # ── 樱花飘落 ──
        "cherry": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="40" cy="50" rx="60" ry="48" fill="{rg(a,0.10)}" transform="rotate(-20,40,50)"/>
      <ellipse cx="70" cy="30" rx="45" ry="55" fill="{rg(s,0.08)}" transform="rotate(15,70,30)"/>
      <ellipse cx="20" cy="90" rx="38" ry="48" fill="{rg(p,0.06)}" transform="rotate(-35,20,90)"/>
      <circle cx="40" cy="50" r="8" fill="{rg(s,0.12)}"/>
      <ellipse cx="710" cy="80" rx="55" ry="44" fill="{rg(s,0.09)}" transform="rotate(20,710,80)"/>
      <ellipse cx="690" cy="50" rx="40" ry="50" fill="{rg(a,0.07)}" transform="rotate(-10,690,50)"/>
      <ellipse cx="730" cy="110" rx="35" ry="35" fill="{rg(p,0.06)}"/>
      <ellipse cx="700" cy="970" rx="70" ry="56" fill="{rg(a,0.08)}" transform="rotate(10,700,970)"/>
      <ellipse cx="40" cy="880" rx="55" ry="44" fill="{rg(s,0.07)}" transform="rotate(-15,40,880)"/>
      <ellipse cx="300" cy="400" rx="8" ry="5" fill="{rg(a,0.12)}" transform="rotate(30,300,400)"/>
      <ellipse cx="480" cy="600" rx="7" ry="4.5" fill="{rg(s,0.10)}" transform="rotate(-20,480,600)"/>
    </svg>""",

        # ── 薰衣草 ──
        "lavender": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="50" cy="60" rx="45" ry="35" fill="{rg(a,0.08)}" transform="rotate(-15,50,60)"/>
      <ellipse cx="30" cy="90" rx="35" ry="28" fill="{rg(s,0.06)}" transform="rotate(-30,30,90)"/>
      <path d="M50 115 Q55 160 48 200" stroke="{rg(a,0.10)}" stroke-width="1.5" fill="none"/>
      <circle cx="50" cy="40" r="6" fill="{rg(p,0.12)}"/>
      <circle cx="45" cy="55" r="5" fill="{rg(p,0.10)}"/>
      <circle cx="55" cy="50" r="5" fill="{rg(p,0.10)}"/>
      <ellipse cx="700" cy="90" rx="50" ry="40" fill="{rg(s,0.07)}" transform="rotate(15,700,90)"/>
      <path d="M700 120 Q705 170 695 220" stroke="{rg(a,0.09)}" stroke-width="1.5" fill="none"/>
      <ellipse cx="700" cy="970" rx="65" ry="50" fill="{rg(a,0.07)}" transform="rotate(10,700,970)"/>
      <ellipse cx="30" cy="870" rx="50" ry="38" fill="{rg(p,0.06)}"/>
    </svg>""",

        # ── 橄榄枝 ──
        "olive": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="50" cy="60" rx="50" ry="25" fill="{rg(s,0.08)}" transform="rotate(-25,50,60)"/>
      <ellipse cx="30" cy="90" rx="42" ry="20" fill="{rg(a,0.06)}" transform="rotate(-45,30,90)"/>
      <path d="M50 100 Q55 150 45 200" stroke="{rg(a,0.10)}" stroke-width="2" fill="none"/>
      <ellipse cx="700" cy="80" rx="55" ry="27" fill="{rg(a,0.07)}" transform="rotate(20,700,80)"/>
      <ellipse cx="720" cy="120" rx="45" ry="22" fill="{rg(s,0.06)}" transform="rotate(40,720,120)"/>
      <ellipse cx="700" cy="960" rx="70" ry="35" fill="{rg(a,0.08)}" transform="rotate(-10,700,960)"/>
      <ellipse cx="40" cy="860" rx="55" ry="28" fill="{rg(s,0.06)}" transform="rotate(15,40,860)"/>
    </svg>""",

        # ── 伦敦雾 ──
        "fog": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M0 50 Q100 30 200 50 Q300 70 400 50 Q500 30 600 50 Q680 70 750 50" stroke="{rg(s,0.08)}" stroke-width="20" fill="none" opacity="0.5"/>
      <path d="M0 120 Q150 100 300 120 Q450 140 600 120 Q680 100 750 120" stroke="{rg(s,0.06)}" stroke-width="15" fill="none" opacity="0.4"/>
      <path d="M0 180 Q200 160 400 180 Q550 200 750 180" stroke="{rg(p,0.05)}" stroke-width="12" fill="none" opacity="0.3"/>
      <path d="M0 900 Q150 880 300 900 Q450 920 600 900 Q680 880 750 900" stroke="{rg(s,0.07)}" stroke-width="18" fill="none" opacity="0.4"/>
      <path d="M0 960 Q200 940 400 960 Q550 980 750 960" stroke="{rg(p,0.05)}" stroke-width="14" fill="none" opacity="0.3"/>
    </svg>""",

        # ── 竹叶线条 ──
        "bamboo": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <line x1="30" y1="0" x2="30" y2="500" stroke="{rg(s,0.10)}" stroke-width="1.5"/>
      <line x1="30" y1="80" x2="110" y2="125" stroke="{rg(s,0.07)}" stroke-width="1"/>
      <line x1="30" y1="160" x2="90" y2="195" stroke="{rg(s,0.07)}" stroke-width="1"/>
      <line x1="30" y1="240" x2="100" y2="285" stroke="{rg(s,0.07)}" stroke-width="1"/>
      <line x1="30" y1="320" x2="80" y2="355" stroke="{rg(s,0.07)}" stroke-width="1"/>
      <line x1="720" y1="200" x2="720" y2="800" stroke="{rg(s,0.10)}" stroke-width="1.5"/>
      <line x1="720" y1="380" x2="640" y2="425" stroke="{rg(s,0.07)}" stroke-width="1"/>
      <line x1="720" y1="500" x2="660" y2="545" stroke="{rg(s,0.07)}" stroke-width="1"/>
      <line x1="0" y1="525" x2="750" y2="525" stroke="{rg(s,0.05)}" stroke-width="0.8"/>
      <line x1="0" y1="535" x2="750" y2="535" stroke="{rg(s,0.03)}" stroke-width="0.5"/>
    </svg>""",

        # ── 青苔森林 ──
        "moss": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="45" cy="55" rx="48" ry="24" fill="{rg(a,0.10)}" transform="rotate(-30,45,55)"/>
      <ellipse cx="25" cy="85" rx="40" ry="20" fill="{rg(s,0.08)}" transform="rotate(-50,25,85)"/>
      <ellipse cx="55" cy="110" rx="30" ry="15" fill="{rg(a,0.06)}" transform="rotate(-20,55,110)"/>
      <ellipse cx="705" cy="75" rx="52" ry="26" fill="{rg(s,0.09)}" transform="rotate(20,705,75)"/>
      <ellipse cx="720" cy="115" rx="42" ry="21" fill="{rg(a,0.07)}" transform="rotate(40,720,115)"/>
      <ellipse cx="700" cy="965" rx="75" ry="38" fill="{rg(a,0.08)}" transform="rotate(-10,700,965)"/>
      <ellipse cx="35" cy="865" rx="58" ry="29" fill="{rg(s,0.07)}" transform="rotate(15,35,865)"/>
    </svg>""",

        # ── 海浪波纹 ──
        "waves": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M0 80 Q100 60 200 80 Q300 100 400 80 Q500 60 600 80 Q680 100 750 80" stroke="{rg(a,0.12)}" stroke-width="2.5" fill="none"/>
      <path d="M0 100 Q100 80 200 100 Q300 120 400 100 Q500 80 600 100 Q680 120 750 100" stroke="{rg(s,0.08)}" stroke-width="1.5" fill="none"/>
      <path d="M0 900 Q150 880 300 900 Q450 920 600 900 Q680 880 750 900" stroke="{rg(s,0.10)}" stroke-width="2" fill="none"/>
      <path d="M0 930 Q150 910 300 930 Q450 950 600 930 Q680 910 750 930" stroke="{rg(a,0.07)}" stroke-width="1.5" fill="none"/>
      <ellipse cx="60" cy="60" rx="45" ry="45" fill="{rg(a,0.06)}"/>
      <ellipse cx="700" cy="100" rx="50" ry="50" fill="{rg(s,0.05)}"/>
    </svg>""",

        # ── 麦浪草原 ──
        "grass": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M30 400 Q40 350 35 300" stroke="{rg(s,0.12)}" stroke-width="1.5" fill="none"/>
      <path d="M50 420 Q55 370 48 310" stroke="{rg(a,0.10)}" stroke-width="1.5" fill="none"/>
      <path d="M70 400 Q78 355 72 300" stroke="{rg(s,0.08)}" stroke-width="1.5" fill="none"/>
      <path d="M680 620 Q690 570 685 520" stroke="{rg(a,0.10)}" stroke-width="1.5" fill="none"/>
      <path d="M700 640 Q708 595 700 540" stroke="{rg(s,0.12)}" stroke-width="1.5" fill="none"/>
      <path d="M0 900 Q100 880 200 900 Q300 920 400 900 Q500 880 600 900 Q680 920 750 900" stroke="{rg(a,0.08)}" stroke-width="2" fill="none"/>
      <ellipse cx="40" cy="60" rx="50" ry="35" fill="{rg(s,0.06)}"/>
      <ellipse cx="710" cy="90" rx="45" ry="32" fill="{rg(a,0.05)}"/>
    </svg>""",

        # ── 蕨类植物 ──
        "fern": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M100 300 Q120 200 100 100" stroke="{rg(a,0.12)}" stroke-width="2" fill="none"/>
      <path d="M100 250 Q130 230 150 240" stroke="{rg(a,0.08)}" stroke-width="1.5" fill="none"/>
      <path d="M100 300 Q80 270 60 280" stroke="{rg(s,0.08)}" stroke-width="1.5" fill="none"/>
      <path d="M100 200 Q120 180 140 185" stroke="{rg(s,0.06)}" stroke-width="1" fill="none"/>
      <path d="M650 700 Q670 600 650 500" stroke="{rg(s,0.12)}" stroke-width="2" fill="none"/>
      <path d="M650 650 Q630 620 610 630" stroke="{rg(a,0.08)}" stroke-width="1.5" fill="none"/>
      <path d="M650 550 Q670 530 690 535" stroke="{rg(a,0.06)}" stroke-width="1" fill="none"/>
      <ellipse cx="40" cy="80" rx="55" ry="40" fill="{rg(s,0.07)}"/>
      <ellipse cx="710" cy="100" rx="50" ry="36" fill="{rg(a,0.06)}"/>
    </svg>""",

        # ── 水墨山水 ──
        "mountains": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M0 920 Q100 870 200 900 Q300 880 400 890 Q500 870 600 900 Q680 880 750 890 L750 1050 L0 1050 Z" fill="{rg(p,0.06)}"/>
      <path d="M0 950 Q150 920 300 940 Q450 920 600 940 Q700 920 750 930 L750 1050 L0 1050 Z" fill="{rg(s,0.05)}"/>
      <path d="M200 700 L240 580 L290 680 L330 540 L380 680 L420 600 L470 700" stroke="{rg(p,0.08)}" stroke-width="2" fill="none"/>
      <path d="M600 680 L630 600 L670 670 L710 560 L750 670" stroke="{rg(s,0.06)}" stroke-width="1.5" fill="none"/>
      <ellipse cx="680" cy="100" rx="65" ry="22" fill="{rg(a,0.05)}"/>
    </svg>""",

        # ── 北欧线条 ──
        "lines": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <line x1="0" y1="100" x2="750" y2="100" stroke="{rg(s,0.08)}" stroke-width="0.8"/>
      <line x1="0" y1="200" x2="750" y2="200" stroke="{rg(s,0.05)}" stroke-width="0.5"/>
      <line x1="0" y1="300" x2="750" y2="300" stroke="{rg(s,0.05)}" stroke-width="0.5"/>
      <line x1="0" y1="400" x2="750" y2="400" stroke="{rg(s,0.05)}" stroke-width="0.5"/>
      <line x1="0" y1="850" x2="750" y2="850" stroke="{rg(s,0.08)}" stroke-width="0.8"/>
      <line x1="0" y1="950" x2="750" y2="950" stroke="{rg(s,0.05)}" stroke-width="0.5"/>
      <rect x="20" y="20" width="710" height="1010" stroke="{rg(p,0.06)}" stroke-width="1" fill="none"/>
    </svg>""",

        # ── 水墨晕染 ──
        "inkwash": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M0 900 Q150 880 300 900 Q450 920 600 900 Q680 880 750 900" stroke="{rg(p,0.10)}" stroke-width="3" fill="none"/>
      <path d="M0 930 Q200 910 400 930 Q550 950 750 930" stroke="{rg(s,0.07)}" stroke-width="2" fill="none"/>
      <path d="M100 700 L130 600 L170 700 L210 580 L260 700" stroke="{rg(p,0.06)}" stroke-width="2" fill="none"/>
      <ellipse cx="700" cy="100" rx="60" ry="25" fill="{rg(p,0.05)}"/>
    </svg>""",

        # ── 霓虹灯光 ──
        "neon": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M0 100 Q100 80 200 100 Q300 120 400 100 Q500 80 600 100 Q680 120 750 100" stroke="{rg(a,0.20)}" stroke-width="3" fill="none"/>
      <path d="M0 120 Q100 100 200 120 Q300 140 400 120 Q500 100 600 120 Q680 140 750 120" stroke="{rg(s,0.12)}" stroke-width="2" fill="none"/>
      <path d="M0 900 Q150 880 300 900 Q450 920 600 900 Q680 880 750 900" stroke="{rg(a,0.15)}" stroke-width="2.5" fill="none"/>
      <path d="M0 920 Q150 900 300 920 Q450 940 600 920 Q680 900 750 920" stroke="{rg(s,0.10)}" stroke-width="2" fill="none"/>
      <ellipse cx="50" cy="60" rx="40" ry="40" fill="{rg(a,0.06)}"/>
      <ellipse cx="700" cy="80" rx="45" ry="45" fill="{rg(s,0.05)}"/>
    </svg>""",

        # ── 胶片边框 ──
        "filmstrip": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <rect x="20" y="20" width="710" height="1010" stroke="{rg(s,0.10)}" stroke-width="1" fill="none"/>
      <rect x="30" y="30" width="690" height="990" stroke="{rg(s,0.06)}" stroke-width="0.5" fill="none" stroke-dasharray="4,4"/>
      <rect x="50" y="50" width="650" height="950" stroke="{rg(a,0.08)}" stroke-width="2" fill="none"/>
      <ellipse cx="40" cy="60" rx="40" ry="40" fill="{rg(a,0.06)}"/>
      <ellipse cx="710" cy="90" rx="38" ry="38" fill="{rg(s,0.05)}"/>
    </svg>""",

        # ── 简约圆点（干净的） ──
        "dots_clean": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <circle cx="60" cy="70" r="30" fill="{rg(s,0.08)}"/>
      <circle cx="45" cy="50" r="18" fill="{rg(a,0.06)}"/>
      <circle cx="700" cy="100" r="35" fill="{rg(a,0.07)}"/>
      <circle cx="720" cy="75" r="22" fill="{rg(s,0.05)}"/>
      <circle cx="700" cy="960" r="40" fill="{rg(s,0.07)}"/>
      <circle cx="45" cy="880" r="32" fill="{rg(a,0.06)}"/>
    </svg>""",

        # ── 柔云 ──
        "clouds_soft": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="100" cy="80" rx="70" ry="30" fill="{rg(s,0.10)}"/>
      <ellipse cx="70" cy="70" rx="45" ry="25" fill="{rg(a,0.08)}"/>
      <ellipse cx="130" cy="75" rx="40" ry="22" fill="{rg(p,0.06)}"/>
      <ellipse cx="640" cy="100" rx="65" ry="28" fill="{rg(a,0.09)}"/>
      <ellipse cx="680" cy="90" rx="40" ry="22" fill="{rg(s,0.07)}"/>
      <ellipse cx="100" cy="920" rx="75" ry="32" fill="{rg(s,0.08)}"/>
      <ellipse cx="65" cy="910" rx="48" ry="24" fill="{rg(a,0.06)}"/>
      <ellipse cx="680" cy="960" rx="70" ry="30" fill="{rg(a,0.08)}"/>
    </svg>""",

        # ── 花瓣 ──
        "petals": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="50" cy="55" rx="50" ry="40" fill="{rg(a,0.09)}" transform="rotate(-20,50,55)"/>
      <ellipse cx="30" cy="85" rx="40" ry="32" fill="{rg(s,0.07)}" transform="rotate(-40,30,85)"/>
      <circle cx="50" cy="55" r="10" fill="{rg(p,0.12)}"/>
      <ellipse cx="700" cy="90" rx="55" ry="44" fill="{rg(s,0.08)}" transform="rotate(20,700,90)"/>
      <ellipse cx="720" cy="60" rx="42" ry="34" fill="{rg(a,0.06)}" transform="rotate(-10,720,60)"/>
      <circle cx="700" cy="90" r="10" fill="{rg(p,0.10)}"/>
      <ellipse cx="700" cy="965" rx="65" ry="52" fill="{rg(a,0.08)}" transform="rotate(10,700,965)"/>
      <ellipse cx="40" cy="870" rx="50" ry="40" fill="{rg(s,0.07)}" transform="rotate(-15,40,870)"/>
    </svg>""",

        # ── 简约叶 ──
        "leaves_minimal": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="50" cy="60" rx="45" ry="20" fill="{rg(a,0.10)}" transform="rotate(-30,50,60)"/>
      <ellipse cx="28" cy="90" rx="38" ry="17" fill="{rg(s,0.08)}" transform="rotate(-50,28,90)"/>
      <ellipse cx="700" cy="80" rx="50" ry="22" fill="{rg(s,0.09)}" transform="rotate(20,700,80)"/>
      <ellipse cx="720" cy="120" rx="40" ry="18" fill="{rg(a,0.07)}" transform="rotate(40,720,120)"/>
      <ellipse cx="700" cy="970" rx="60" ry="26" fill="{rg(a,0.08)}" transform="rotate(-10,700,970)"/>
      <ellipse cx="35" cy="865" rx="48" ry="21" fill="{rg(s,0.07)}" transform="rotate(15,35,865)"/>
    </svg>""",

        # ── 简约波浪 ──
        "waves_minimal": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M0 90 Q100 70 200 90 Q300 110 400 90 Q500 70 600 90 Q680 110 750 90" stroke="{rg(s,0.12)}" stroke-width="2" fill="none"/>
      <path d="M0 905 Q150 885 300 905 Q450 925 600 905 Q680 885 750 905" stroke="{rg(s,0.10)}" stroke-width="2" fill="none"/>
      <ellipse cx="55" cy="60" rx="45" ry="45" fill="{rg(a,0.06)}"/>
      <ellipse cx="705" cy="95" rx="42" ry="42" fill="{rg(s,0.05)}"/>
    </svg>""",

        # ── 三角形几何 ──
        "triangle": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <polygon points="50,0 100,50 0,50" fill="{rg(s,0.08)}"/>
      <polygon points="700,0 750,0 750,50" fill="{rg(a,0.10)}"/>
      <polygon points="0,920 80,920 0,840" fill="{rg(a,0.09)}"/>
      <polygon points="750,920 670,920 750,840" fill="{rg(s,0.08)}"/>
      <polygon points="375,1040 425,1000 325,1000" fill="{rg(p,0.06)}"/>
      <line x1="200" y1="0" x2="185" y2="100" stroke="{rg(s,0.08)}" stroke-width="1.5"/>
      <line x1="220" y1="0" x2="210" y2="100" stroke="{rg(a,0.06)}" stroke-width="1.5"/>
      <line x1="240" y1="0" x2="235" y2="100" stroke="{rg(p,0.05)}" stroke-width="1.5"/>
    </svg>""",

        # ── 电路线条 ──
        "circuit": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <line x1="0" y1="200" x2="600" y2="200" stroke="{rg(s,0.15)}" stroke-width="1"/>
      <line x1="600" y1="200" x2="600" y2="400" stroke="{rg(s,0.15)}" stroke-width="1"/>
      <circle cx="600" cy="200" r="4" fill="{rg(a,0.30)}"/>
      <line x1="150" y1="0" x2="150" y2="500" stroke="{rg(p,0.12)}" stroke-width="0.8"/>
      <line x1="150" y1="500" x2="300" y2="500" stroke="{rg(p,0.12)}" stroke-width="0.8"/>
      <circle cx="150" cy="500" r="3" fill="{rg(p,0.25)}"/>
      <line x1="0" y1="800" x2="500" y2="800" stroke="{rg(s,0.12)}" stroke-width="1"/>
      <line x1="500" y1="800" x2="500" y2="900" stroke="{rg(s,0.12)}" stroke-width="1"/>
      <circle cx="500" cy="800" r="3" fill="{rg(p,0.25)}"/>
      <line x1="700" y1="0" x2="700" y2="600" stroke="{rg(p,0.10)}" stroke-width="0.8"/>
    </svg>""",

        # ── 窗框线条 ──
        "window": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <rect x="30" y="30" width="80" height="120" stroke="{rg(s,0.12)}" stroke-width="1.5" fill="none"/>
      <line x1="30" y1="90" x2="110" y2="90" stroke="{rg(s,0.12)}" stroke-width="1"/>
      <line x1="70" y1="30" x2="70" y2="150" stroke="{rg(s,0.12)}" stroke-width="1"/>
      <rect x="640" y="40" width="80" height="100" stroke="{rg(a,0.10)}" stroke-width="1.5" fill="none"/>
      <line x1="640" y1="90" x2="720" y2="90" stroke="{rg(a,0.10)}" stroke-width="1"/>
      <line x1="680" y1="40" x2="680" y2="140" stroke="{rg(a,0.10)}" stroke-width="1"/>
      <rect x="35" y="880" width="70" height="100" stroke="{rg(s,0.10)}" stroke-width="1.5" fill="none"/>
      <rect x="650" y="870" width="75" height="110" stroke="{rg(a,0.09)}" stroke-width="1.5" fill="none"/>
    </svg>""",

        # ── 条形码 ──
        "barcode": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <line x1="60" y1="30" x2="60" y2="200" stroke="{rg(s,0.20)}" stroke-width="2"/>
      <line x1="70" y1="30" x2="70" y2="200" stroke="{rg(s,0.20)}" stroke-width="1"/>
      <line x1="75" y1="30" x2="75" y2="200" stroke="{rg(s,0.20)}" stroke-width="3"/>
      <line x1="85" y1="30" x2="85" y2="200" stroke="{rg(s,0.20)}" stroke-width="1"/>
      <line x1="90" y1="30" x2="90" y2="200" stroke="{rg(s,0.20)}" stroke-width="2"/>
      <line x1="100" y1="30" x2="100" y2="200" stroke="{rg(s,0.20)}" stroke-width="4"/>
      <line x1="110" y1="30" x2="110" y2="200" stroke="{rg(s,0.20)}" stroke-width="1"/>
      <line x1="120" y1="30" x2="120" y2="200" stroke="{rg(s,0.20)}" stroke-width="2"/>
      <line x1="60" y1="850" x2="60" y2="1020" stroke="{rg(s,0.20)}" stroke-width="2"/>
      <line x1="70" y1="850" x2="70" y2="1020" stroke="{rg(s,0.20)}" stroke-width="1"/>
      <line x1="75" y1="850" x2="75" y2="1020" stroke="{rg(s,0.20)}" stroke-width="3"/>
      <line x1="85" y1="850" x2="85" y2="1020" stroke="{rg(s,0.20)}" stroke-width="1"/>
    </svg>""",

        # ── 印象派笔触 ──
        "brushstroke": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M0 100 Q100 70 200 100 Q300 130 400 100 Q500 70 600 100 Q680 130 750 100" stroke="{rg(a,0.15)}" stroke-width="8" fill="none" stroke-linecap="round"/>
      <path d="M0 140 Q100 110 200 140 Q300 170 400 140 Q500 110 600 140 Q680 170 750 140" stroke="{rg(s,0.08)}" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M0 920 Q150 890 300 920 Q450 950 600 920 Q680 890 750 920" stroke="{rg(a,0.12)}" stroke-width="6" fill="none" stroke-linecap="round"/>
      <path d="M0 950 Q150 920 300 950 Q450 980 600 950 Q680 920 750 950" stroke="{rg(s,0.07)}" stroke-width="3" fill="none" stroke-linecap="round"/>
      <ellipse cx="50" cy="70" rx="50" ry="50" fill="{rg(a,0.06)}"/>
      <ellipse cx="710" cy="90" rx="45" ry="45" fill="{rg(s,0.05)}"/>
    </svg>""",

        # ── 浮世绘波浪 ──
        "wave_ukiyoe": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M0 80 Q50 50 100 80 Q150 110 200 80 Q250 50 300 80 Q350 110 400 80 Q450 50 500 80 Q550 110 600 80 Q650 50 700 80 Q720 100 750 90" stroke="{rg(p,0.12)}" stroke-width="3" fill="none"/>
      <path d="M0 120 Q50 90 100 120 Q150 150 200 120 Q250 90 300 120 Q350 150 400 120 Q450 90 500 120 Q550 150 600 120 Q650 90 700 120 Q720 140 750 130" stroke="{rg(s,0.08)}" stroke-width="2" fill="none"/>
      <path d="M0 950 Q150 920 300 950 Q450 980 600 950 Q680 920 750 950" stroke="{rg(p,0.10)}" stroke-width="3" fill="none"/>
      <path d="M0 980 Q150 950 300 980 Q450 1010 600 980 Q680 950 750 980" stroke="{rg(s,0.07)}" stroke-width="2" fill="none"/>
    </svg>""",

        # ── 蒙德里安网格 ──
        "grid": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <line x1="150" y1="0" x2="150" y2="1050" stroke="{rg(p,0.15)}" stroke-width="2"/>
      <line x1="0" y1="300" x2="750" y2="300" stroke="{rg(p,0.15)}" stroke-width="2"/>
      <line x1="0" y1="600" x2="750" y2="600" stroke="{rg(p,0.15)}" stroke-width="2"/>
      <rect x="0" y="0" width="150" height="300" fill="{rg(a,0.08)}"/>
      <rect x="0" y="600" width="150" height="450" fill="{rg(s,0.08)}"/>
      <rect x="150" y="600" width="600" height="200" fill="{rg(p,0.04)}"/>
    </svg>""",

        # ── 极光光带 ──
        "aurora": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M0 150 Q200 100 400 150 Q550 200 750 150" stroke="{rg(p,0.25)}" stroke-width="8" fill="none" opacity="0.6"/>
      <path d="M0 200 Q200 150 400 200 Q550 250 750 200" stroke="{rg(s,0.18)}" stroke-width="5" fill="none" opacity="0.5"/>
      <path d="M0 250 Q200 200 400 250 Q550 300 750 250" stroke="{rg(a,0.15)}" stroke-width="3" fill="none" opacity="0.4"/>
      <path d="M0 900 Q200 870 400 900 Q550 930 750 900" stroke="{rg(s,0.20)}" stroke-width="6" fill="none" opacity="0.5"/>
      <path d="M0 940 Q200 910 400 940 Q550 970 750 940" stroke="{rg(p,0.15)}" stroke-width="4" fill="none" opacity="0.4"/>
      <circle cx="60" cy="60" r="25" fill="{rg(p,0.15)}"/>
      <circle cx="700" cy="80" r="30" fill="{rg(s,0.12)}"/>
    </svg>""",

        # ── 薰衣草田 ──
        "lavender_field": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="50" cy="55" rx="48" ry="38" fill="{rg(a,0.10)}" transform="rotate(-20,50,55)"/>
      <ellipse cx="30" cy="85" rx="38" ry="30" fill="{rg(s,0.08)}" transform="rotate(-40,30,85)"/>
      <circle cx="50" cy="35" r="6" fill="{rg(p,0.15)}"/>
      <circle cx="42" cy="48" r="5" fill="{rg(p,0.12)}"/>
      <circle cx="58" cy="45" r="5" fill="{rg(p,0.12)}"/>
      <circle cx="50" cy="60" r="5" fill="{rg(p,0.10)}"/>
      <ellipse cx="700" cy="85" rx="55" ry="44" fill="{rg(s,0.09)}" transform="rotate(20,700,85)"/>
      <circle cx="700" cy="60" r="7" fill="{rg(p,0.14)}"/>
      <circle cx="690" cy="78" r="6" fill="{rg(p,0.11)}"/>
      <circle cx="710" cy="75" r="6" fill="{rg(p,0.11)}"/>
      <ellipse cx="700" cy="965" rx="70" ry="56" fill="{rg(a,0.09)}" transform="rotate(10,700,965)"/>
      <ellipse cx="40" cy="870" rx="52" ry="42" fill="{rg(s,0.08)}" transform="rotate(-15,40,870)"/>
    </svg>""",

        # ── 枫叶 ──
        "maple": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M50 60 L60 30 L70 50 L80 20 L85 50 L100 35 L90 60 L100 55 L80 75 L85 100 L60 85 L35 100 L40 75 L20 55 L30 60 Z" fill="{rg(a,0.12)}"/>
      <path d="M700 100 L710 70 L720 90 L730 60 L735 90 L750 75 L740 100 L750 95 L730 115 L735 140 L710 125 L685 140 L690 115 L670 95 L680 100 Z" fill="{rg(s,0.10)}"/>
      <path d="M50 900 L58 875 L65 890 L73 868 L77 892 L88 880 L80 900 L88 897 L72 912 L76 932 L58 920 L40 933 L43 912 L28 897 L36 900 Z" fill="{rg(a,0.10)}"/>
      <ellipse cx="700" cy="970" rx="55" ry="55" fill="{rg(s,0.08)}"/>
    </svg>""",

        # ── 奶油漩涡 ──
        "cream": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M50 80 Q80 50 110 80 Q140 110 170 80" stroke="{rg(s,0.15)}" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M70 110 Q100 80 130 110 Q160 140 190 110" stroke="{rg(a,0.10)}" stroke-width="2" fill="none" stroke-linecap="round"/>
      <path d="M600 950 Q630 920 660 950 Q690 980 720 950" stroke="{rg(a,0.12)}" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M620 980 Q650 950 680 980 Q710 1010 740 980" stroke="{rg(s,0.08)}" stroke-width="2" fill="none" stroke-linecap="round"/>
      <ellipse cx="50" cy="60" rx="50" ry="50" fill="{rg(s,0.07)}"/>
      <ellipse cx="710" cy="90" rx="45" ry="45" fill="{rg(a,0.06)}"/>
    </svg>""",

        # ── 春节灯笼 ──
        "lantern": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 顶部流苏 -->
      <line x1="60" y1="0" x2="60" y2="25" stroke="{rg(p,0.30)}" stroke-width="1.5"/>
      <line x1="60" y1="25" x2="55" y2="60" stroke="{rg(a,0.25)}" stroke-width="1"/>
      <line x1="60" y1="25" x2="60" y2="62" stroke="{rg(a,0.25)}" stroke-width="1"/>
      <line x1="60" y1="25" x2="65" y2="60" stroke="{rg(a,0.25)}" stroke-width="1"/>
      <!-- 灯笼主体 -->
      <ellipse cx="60" cy="100" rx="35" ry="42" fill="{rg(p,0.18)}"/>
      <ellipse cx="60" cy="100" rx="28" ry="35" fill="{rg(a,0.12)}"/>
      <rect x="50" y="55" width="20" height="8" rx="3" fill="{rg(a,0.25)}"/>
      <rect x="50" y="137" width="20" height="6" rx="2" fill="{rg(a,0.25)}"/>
      <!-- 右上灯笼 -->
      <line x1="700" y1="0" x2="700" y2="22" stroke="{rg(p,0.28)}" stroke-width="1.5"/>
      <line x1="700" y1="22" x2="695" y2="55" stroke="{rg(a,0.23)}" stroke-width="1"/>
      <line x1="700" y1="22" x2="700" y2="57" stroke="{rg(a,0.23)}" stroke-width="1"/>
      <line x1="700" y1="22" x2="705" y2="55" stroke="{rg(a,0.23)}" stroke-width="1"/>
      <ellipse cx="700" cy="95" rx="30" ry="38" fill="{rg(p,0.16)}"/>
      <ellipse cx="700" cy="95" rx="24" ry="31" fill="{rg(a,0.10)}"/>
      <rect x="691" y="53" width="18" height="7" rx="3" fill="{rg(a,0.23)}"/>
      <rect x="691" y="128" width="18" height="5" rx="2" fill="{rg(a,0.23)}"/>
      <!-- 底部角落灯笼 -->
      <ellipse cx="45" cy="930" rx="28" ry="34" fill="{rg(p,0.12)}"/>
      <ellipse cx="45" cy="930" rx="22" ry="27" fill="{rg(a,0.08)}"/>
      <rect x="36" y="890" width="18" height="6" rx="2" fill="{rg(a,0.20)}"/>
      <line x1="45" y1="964" x2="45" y2="980" stroke="{rg(a,0.20)}" stroke-width="1"/>
      <ellipse cx="710" cy="970" rx="25" ry="30" fill="{rg(p,0.10)}"/>
      <ellipse cx="710" cy="970" rx="20" ry="24" fill="{rg(a,0.07)}"/>
    </svg>""",

        # ── 金色星光 ──
        "sparkle": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 四角星 -->
      <path d="M80 40 L85 55 L100 60 L85 65 L80 80 L75 65 L60 60 L75 55 Z" fill="{rg(a,0.20)}"/>
      <path d="M670 55 L674 67 L686 72 L674 77 L670 89 L666 77 L654 72 L666 67 Z" fill="{rg(a,0.18)}"/>
      <path d="M80 920 L84 932 L96 937 L84 942 L80 954 L76 942 L64 937 L76 932 Z" fill="{rg(a,0.18)}"/>
      <path d="M670 935 L674 947 L686 952 L674 957 L670 969 L666 957 L654 952 L666 947 Z" fill="{rg(a,0.16)}"/>
      <!-- 小星点 -->
      <circle cx="120" cy="90" r="4" fill="{rg(a,0.25)}"/>
      <circle cx="200" cy="60" r="3" fill="{rg(a,0.18)}"/>
      <circle cx="550" cy="75" r="4" fill="{rg(a,0.22)}"/>
      <circle cx="620" cy="110" r="3" fill="{rg(a,0.16)}"/>
      <circle cx="100" cy="900" r="3" fill="{rg(a,0.20)}"/>
      <circle cx="650" cy="920" r="4" fill="{rg(a,0.18)}"/>
      <!-- 装饰线 -->
      <path d="M0 180 Q100 160 200 180" stroke="{rg(s,0.06)}" stroke-width="1.5" fill="none"/>
      <path d="M550 880 Q650 860 750 880" stroke="{rg(s,0.06)}" stroke-width="1.5" fill="none"/>
    </svg>""",

        # ── 五角星 ──
        "star": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 大星 -->
      <path d="M100 50 L110 80 L143 80 L117 100 L127 132 L100 112 L73 132 L83 100 L57 80 L90 80 Z" fill="{rg(a,0.18)}"/>
      <path d="M100 50 L110 80 L143 80 L117 100 L127 132 L100 112 L73 132 L83 100 L57 80 L90 80 Z" fill="none" stroke="{rg(p,0.10)}" stroke-width="0.8"/>
      <!-- 小星 -->
      <path d="M650 70 L656 90 L676 90 L660 102 L666 122 L650 110 L634 122 L640 102 L624 90 L644 90 Z" fill="{rg(s,0.15)}"/>
      <path d="M60 950 L65 966 L81 966 L68 976 L73 992 L60 982 L47 992 L52 976 L39 966 L55 966 Z" fill="{rg(a,0.14)}"/>
      <path d="M680 920 L684 932 L696 932 L686 940 L690 952 L680 944 L670 952 L674 940 L664 932 L676 932 Z" fill="{rg(s,0.12)}"/>
      <!-- 散点 -->
      <circle cx="300" cy="120" r="3" fill="{rg(a,0.20)}"/>
      <circle cx="480" cy="90" r="2" fill="{rg(a,0.15)}"/>
      <circle cx="200" cy="920" r="2" fill="{rg(a,0.15)}"/>
      <circle cx="560" cy="940" r="3" fill="{rg(a,0.18)}"/>
    </svg>""",

        # ── 雪花 ──
        "snow": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 雪花1 -->
      <circle cx="80" cy="80" r="15" fill="{rg(a,0.12)}"/>
      <line x1="80" y1="62" x2="80" y2="98" stroke="{rg(a,0.18)}" stroke-width="1.5"/>
      <line x1="62" y1="80" x2="98" y2="80" stroke="{rg(a,0.18)}" stroke-width="1.5"/>
      <line x1="67" y1="67" x2="93" y2="93" stroke="{rg(a,0.14)}" stroke-width="1"/>
      <line x1="93" y1="67" x2="67" y2="93" stroke="{rg(a,0.14)}" stroke-width="1"/>
      <!-- 雪花2 -->
      <circle cx="680" cy="110" r="12" fill="{rg(s,0.10)}"/>
      <line x1="680" y1="96" x2="680" y2="124" stroke="{rg(s,0.16)}" stroke-width="1.5"/>
      <line x1="666" y1="110" x2="694" y2="110" stroke="{rg(s,0.16)}" stroke-width="1.5"/>
      <line x1="670" y1="100" x2="690" y2="120" stroke="{rg(s,0.12)}" stroke-width="1"/>
      <line x1="690" y1="100" x2="670" y2="120" stroke="{rg(s,0.12)}" stroke-width="1"/>
      <!-- 雪花3 -->
      <circle cx="60" cy="920" r="14" fill="{rg(a,0.11)}"/>
      <line x1="60" y1="904" x2="60" y2="936" stroke="{rg(a,0.17)}" stroke-width="1.5"/>
      <line x1="44" y1="920" x2="76" y2="920" stroke="{rg(a,0.17)}" stroke-width="1.5"/>
      <line x1="49" y1="911" x2="71" y2="929" stroke="{rg(a,0.13)}" stroke-width="1"/>
      <line x1="71" y1="911" x2="49" y2="929" stroke="{rg(a,0.13)}" stroke-width="1"/>
      <!-- 雪花4 -->
      <circle cx="700" cy="960" r="18" fill="{rg(s,0.09)}"/>
      <line x1="700" y1="940" x2="700" y2="980" stroke="{rg(s,0.14)}" stroke-width="1.5"/>
      <line x1="680" y1="960" x2="720" y2="960" stroke="{rg(s,0.14)}" stroke-width="1.5"/>
      <!-- 雪花5 中 -->
      <circle cx="200" cy="400" r="10" fill="{rg(a,0.08)}"/>
      <line x1="200" y1="388" x2="200" y2="412" stroke="{rg(a,0.12)}" stroke-width="1"/>
      <line x1="188" y1="400" x2="212" y2="400" stroke="{rg(a,0.12)}" stroke-width="1"/>
      <circle cx="550" cy="600" r="11" fill="{rg(s,0.07)}"/>
      <line x1="550" y1="587" x2="550" y2="613" stroke="{rg(s,0.11)}" stroke-width="1"/>
      <line x1="537" y1="600" x2="563" y2="600" stroke="{rg(s,0.11)}" stroke-width="1"/>
    </svg>""",

        # ── 南瓜 ──
        "pumpkin": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 南瓜1 -->
      <ellipse cx="65" cy="90" rx="40" ry="35" fill="{rg(p,0.18)}"/>
      <ellipse cx="65" cy="90" rx="32" ry="28" fill="{rg(s,0.12)}"/>
      <ellipse cx="65" cy="90" rx="20" ry="25" fill="{rg(p,0.10)}"/>
      <rect x="58" y="52" width="14" height="12" rx="4" fill="{rg(a,0.25)}"/>
      <path d="M65 52 Q72 42 78 48" stroke="{rg(a,0.20)}" stroke-width="2" fill="none"/>
      <!-- 南瓜2 -->
      <ellipse cx="695" cy="105" rx="35" ry="30" fill="{rg(p,0.16)}"/>
      <ellipse cx="695" cy="105" rx="28" ry="24" fill="{rg(s,0.10)}"/>
      <rect x="688" y="72" width="14" height="10" rx="3" fill="{rg(a,0.22)}"/>
      <!-- 南瓜3 -->
      <ellipse cx="50" cy="920" rx="32" ry="28" fill="{rg(p,0.14)}"/>
      <ellipse cx="50" cy="920" rx="25" ry="22" fill="{rg(s,0.09)}"/>
      <!-- 南瓜4 -->
      <ellipse cx="705" cy="960" rx="38" ry="32" fill="{rg(p,0.12)}"/>
      <ellipse cx="705" cy="960" rx="30" ry="26" fill="{rg(s,0.08)}"/>
      <!-- 蝙蝠剪影 -->
      <path d="M300 200 Q320 180 340 200 Q350 190 360 200 Q370 180 390 200 Q380 220 370 210 Q360 230 350 210 Q340 230 330 210 Q320 220 310 210 Q300 220 300 200" fill="{rg(p,0.15)}"/>
      <path d="M500 820 Q515 805 530 820 Q540 812 550 820 Q560 805 575 820 Q565 835 555 827 Q545 843 535 827 Q525 843 515 827 Q505 835 500 820" fill="{rg(s,0.12)}"/>
    </svg>""",

        # ── 气球 ──
        "balloon": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 气球1 粉 -->
      <ellipse cx="60" cy="80" rx="28" ry="36" fill="{rg(p,0.16)}"/>
      <ellipse cx="60" cy="80" rx="22" ry="29" fill="{rg(a,0.10)}"/>
      <polygon points="55,114 60,122 65,114" fill="{rg(a,0.20)}"/>
      <line x1="60" y1="122" x2="58" y2="180" stroke="{rg(a,0.15)}" stroke-width="1"/>
      <!-- 气球2 黄 -->
      <ellipse cx="700" cy="95" rx="25" ry="32" fill="{rg(a,0.14)}"/>
      <ellipse cx="700" cy="95" rx="20" ry="26" fill="{rg(s,0.09)}"/>
      <polygon points="695,125 700,132 705,125" fill="{rg(p,0.18)}"/>
      <line x1="700" y1="132" x2="702" y2="190" stroke="{rg(p,0.12)}" stroke-width="1"/>
      <!-- 气球3 蓝 -->
      <ellipse cx="45" cy="880" rx="22" ry="28" fill="{rg(s,0.12)}"/>
      <polygon points="40,906 45,913 50,906" fill="{rg(s,0.18)}"/>
      <line x1="45" y1="913" x2="43" y2="960" stroke="{rg(s,0.10)}" stroke-width="0.8"/>
      <!-- 气球4 绿 -->
      <ellipse cx="710" cy="940" rx="24" ry="30" fill="{rg(a,0.13)}"/>
      <polygon points="705,968 710,975 715,968" fill="{rg(a,0.20)}"/>
      <line x1="710" y1="975" x2="712" y2="1020" stroke="{rg(a,0.12)}" stroke-width="0.8"/>
      <!-- 气球绳波浪 -->
      <path d="M55 180 Q60 220 58 260" stroke="{rg(a,0.10)}" stroke-width="0.8" fill="none"/>
      <path d="M700 190 Q704 230 702 270" stroke="{rg(p,0.08)}" stroke-width="0.8" fill="none"/>
    </svg>""",

        # ── 向日葵 ──
        "sunflower": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 向日葵1 -->
      <ellipse cx="65" cy="70" rx="18" ry="30" fill="{rg(p,0.18)}" transform="rotate(0,65,70)"/>
      <ellipse cx="50" cy="85" rx="18" ry="30" fill="{rg(a,0.14)}" transform="rotate(60,50,85)"/>
      <ellipse cx="80" cy="85" rx="18" ry="30" fill="{rg(a,0.14)}" transform="rotate(-60,80,85)"/>
      <ellipse cx="42" cy="105" rx="16" ry="26" fill="{rg(s,0.12)}" transform="rotate(120,42,105)"/>
      <ellipse cx="88" cy="105" rx="16" ry="26" fill="{rg(s,0.12)}" transform="rotate(-120,88,105)"/>
      <circle cx="65" cy="90" r="14" fill="{rg(a,0.30)}"/>
      <circle cx="65" cy="90" r="10" fill="{rg(a,0.20)}"/>
      <!-- 向日葵2 -->
      <ellipse cx="700" cy="100" rx="15" ry="26" fill="{rg(p,0.15)}" transform="rotate(0,700,100)"/>
      <ellipse cx="688" cy="112" rx="15" ry="26" fill="{rg(a,0.12)}" transform="rotate(60,688,112)"/>
      <ellipse cx="712" cy="112" rx="15" ry="26" fill="{rg(a,0.12)}" transform="rotate(-60,712,112)"/>
      <circle cx="700" cy="112" r="12" fill="{rg(a,0.25)}"/>
      <!-- 向日葵3 -->
      <ellipse cx="50" cy="910" rx="14" ry="22" fill="{rg(p,0.13)}" transform="rotate(0,50,910)"/>
      <ellipse cx="40" cy="922" rx="14" ry="22" fill="{rg(a,0.10)}" transform="rotate(60,40,922)"/>
      <ellipse cx="60" cy="922" rx="14" ry="22" fill="{rg(a,0.10)}" transform="rotate(-60,60,922)"/>
      <circle cx="50" cy="922" r="10" fill="{rg(a,0.22)}"/>
      <ellipse cx="705" cy="960" rx="16" ry="25" fill="{rg(p,0.12)}" transform="rotate(0,705,960)"/>
      <ellipse cx="692" cy="974" rx="16" ry="25" fill="{rg(a,0.09)}" transform="rotate(60,692,974)"/>
      <ellipse cx="718" cy="974" rx="16" ry="25" fill="{rg(a,0.09)}" transform="rotate(-60,718,974)"/>
      <circle cx="705" cy="974" r="11" fill="{rg(a,0.20)}"/>
    </svg>""",

        # ── 麦穗 ──
        "grain": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 麦穗1 -->
      <path d="M50 60 Q48 90 52 130" stroke="{rg(p,0.15)}" stroke-width="1.5" fill="none"/>
      <ellipse cx="42" cy="75" rx="5" ry="10" fill="{rg(p,0.20)}" transform="rotate(-20,42,75)"/>
      <ellipse cx="52" cy="95" rx="5" ry="10" fill="{rg(a,0.18)}" transform="rotate(15,52,95)"/>
      <ellipse cx="44" cy="115" rx="5" ry="9" fill="{rg(p,0.16)}" transform="rotate(-15,44,115)"/>
      <ellipse cx="55" cy="133" rx="4" ry="8" fill="{rg(a,0.15)}" transform="rotate(10,55,133)"/>
      <!-- 麦穗2 -->
      <path d="M700 80 Q702 115 698 160" stroke="{rg(s,0.14)}" stroke-width="1.5" fill="none"/>
      <ellipse cx="706" cy="95" rx="5" ry="9" fill="{rg(s,0.18)}" transform="rotate(20,706,95)"/>
      <ellipse cx="696" cy="118" rx="5" ry="9" fill="{rg(a,0.16)}" transform="rotate(-15,696,118)"/>
      <ellipse cx="704" cy="140" rx="4" ry="8" fill="{rg(s,0.15)}" transform="rotate(12,704,140)"/>
      <!-- 麦穗3 -->
      <path d="M45 880 Q43 910 47 950" stroke="{rg(p,0.12)}" stroke-width="1.5" fill="none"/>
      <ellipse cx="39" cy="895" rx="4" ry="8" fill="{rg(p,0.16)}" transform="rotate(-18,39,895)"/>
      <ellipse cx="48" cy="915" rx="4" ry="8" fill="{rg(a,0.14)}" transform="rotate(12,48,915)"/>
      <ellipse cx="41" cy="935" rx="4" ry="7" fill="{rg(p,0.13)}" transform="rotate(-10,41,935)"/>
      <path d="M710 930 Q712 955 708 990" stroke="{rg(s,0.11)}" stroke-width="1.5" fill="none"/>
      <ellipse cx="715" cy="945" rx="4" ry="8" fill="{rg(s,0.14)}" transform="rotate(18,715,945)"/>
      <ellipse cx="705" cy="965" rx="4" ry="8" fill="{rg(a,0.12)}" transform="rotate(-12,705,965)"/>
    </svg>""",

        # ── 菊花 ──
        "chrysanthemum": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 菊花1 -->
      <ellipse cx="60" cy="75" rx="6" ry="20" fill="{rg(p,0.15)}" transform="rotate(0,60,75)"/>
      <ellipse cx="50" cy="80" rx="6" ry="20" fill="{rg(a,0.12)}" transform="rotate(45,50,80)"/>
      <ellipse cx="70" cy="80" rx="6" ry="20" fill="{rg(a,0.12)}" transform="rotate(-45,70,80)"/>
      <ellipse cx="45" cy="95" rx="5" ry="16" fill="{rg(s,0.10)}" transform="rotate(90,45,95)"/>
      <ellipse cx="75" cy="95" rx="5" ry="16" fill="{rg(s,0.10)}" transform="rotate(-90,75,95)"/>
      <ellipse cx="52" cy="108" rx="5" ry="15" fill="{rg(p,0.09)}" transform="rotate(135,52,108)"/>
      <ellipse cx="68" cy="108" rx="5" ry="15" fill="{rg(p,0.09)}" transform="rotate(-135,68,108)"/>
      <circle cx="60" cy="92" r="8" fill="{rg(a,0.22)}"/>
      <!-- 菊花2 -->
      <ellipse cx="700" cy="105" rx="5" ry="17" fill="{rg(p,0.13)}" transform="rotate(0,700,105)"/>
      <ellipse cx="692" cy="110" rx="5" ry="17" fill="{rg(a,0.10)}" transform="rotate(45,692,110)"/>
      <ellipse cx="708" cy="110" rx="5" ry="17" fill="{rg(a,0.10)}" transform="rotate(-45,708,110)"/>
      <ellipse cx="688" cy="122" rx="4" ry="13" fill="{rg(s,0.08)}" transform="rotate(90,688,122)"/>
      <ellipse cx="712" cy="122" rx="4" ry="13" fill="{rg(s,0.08)}" transform="rotate(-90,712,122)"/>
      <circle cx="700" cy="118" r="7" fill="{rg(a,0.18)}"/>
      <!-- 菊花3 -->
      <ellipse cx="45" cy="910" rx="5" ry="15" fill="{rg(p,0.12)}" transform="rotate(0,45,910)"/>
      <ellipse cx="37" cy="915" rx="5" ry="15" fill="{rg(a,0.09)}" transform="rotate(45,37,915)"/>
      <ellipse cx="53" cy="915" rx="5" ry="15" fill="{rg(a,0.09)}" transform="rotate(-45,53,915)"/>
      <circle cx="45" cy="922" r="6" fill="{rg(a,0.16)}"/>
      <ellipse cx="710" cy="950" rx="5" ry="16" fill="{rg(p,0.11)}" transform="rotate(0,710,950)"/>
      <ellipse cx="701" cy="955" rx="5" ry="16" fill="{rg(a,0.09)}" transform="rotate(45,701,955)"/>
      <ellipse cx="719" cy="955" rx="5" ry="16" fill="{rg(a,0.09)}" transform="rotate(-45,719,955)"/>
      <circle cx="710" cy="960" r="7" fill="{rg(a,0.15)}"/>
    </svg>""",

        # ── 月亮 ──
        "moon": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 月牙 -->
      <path d="M120 60 A60 60 0 1 1 120 180 A45 45 0 1 0 120 60" fill="{rg(a,0.12)}"/>
      <!-- 云遮 -->
      <ellipse cx="150" cy="100" rx="40" ry="20" fill="{rg(s,0.06)}"/>
      <ellipse cx="130" cy="115" rx="30" ry="16" fill="{rg(s,0.05)}"/>
      <!-- 星星 -->
      <circle cx="200" cy="50" r="3" fill="{rg(a,0.20)}"/>
      <circle cx="250" cy="80" r="2" fill="{rg(a,0.15)}"/>
      <circle cx="180" cy="140" r="2" fill="{rg(a,0.12)}"/>
      <!-- 底部月亮 -->
      <path d="M650 880 A50 50 0 1 1 650 980 A38 38 0 1 0 650 880" fill="{rg(p,0.10)}"/>
      <ellipse cx="680" cy="930" rx="30" ry="15" fill="{rg(s,0.05)}"/>
      <circle cx="600" cy="900" r="2" fill="{rg(a,0.15)}"/>
      <circle cx="700" cy="870" r="2.5" fill="{rg(a,0.12)}"/>
    </svg>""",

        # ── 爱心 ──
        "heart": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 爱心1 -->
      <path d="M60 70 C60 55 45 45 35 55 C25 65 25 80 60 105 C95 80 95 65 85 55 C75 45 60 55 60 70" fill="{rg(p,0.18)}"/>
      <!-- 爱心2 -->
      <path d="M700 90 C700 77 688 69 680 77 C672 85 672 98 700 120 C728 98 728 85 720 77 C712 69 700 77 700 90" fill="{rg(a,0.14)}"/>
      <!-- 爱心3 -->
      <path d="M45 900 C45 890 34 884 26 890 C18 896 18 906 45 928 C72 906 72 896 64 890 C56 884 45 890 45 900" fill="{rg(p,0.14)}"/>
      <!-- 爱心4 -->
      <path d="M710 950 C710 940 699 934 691 940 C683 946 683 956 710 978 C737 956 737 946 729 940 C721 934 710 940 710 950" fill="{rg(a,0.12)}"/>
      <!-- 小爱心散点 -->
      <path d="M180 60 C180 52 172 48 167 52 C162 56 162 64 180 76 C198 64 198 56 193 52 C188 48 180 52 180 60" fill="{rg(a,0.16)}"/>
      <path d="M550 70 C550 63 543 60 539 63 C535 66 535 73 550 82 C565 73 565 66 561 63 C557 60 550 63 550 70" fill="{rg(a,0.13)}"/>
      <path d="M280 940 C280 933 273 930 269 933 C265 936 265 943 280 952 C295 943 295 936 291 933 C287 930 280 933 280 940" fill="{rg(a,0.12)}"/>
      <path d="M480 920 C480 912 472 908 467 912 C462 916 462 924 480 934 C498 924 498 916 493 912 C488 908 480 912 480 920" fill="{rg(a,0.10)}"/>
    </svg>""",

        # ── 雨滴 ──
        "rain": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <path d="M50 50 Q55 70 50 90 Q45 70 50 50" fill="{rg(a,0.15)}"/>
      <path d="M80 80 Q85 100 80 120 Q75 100 80 80" fill="{rg(s,0.12)}"/>
      <path d="M40 150 Q45 170 40 190 Q35 170 40 150" fill="{rg(a,0.10)}"/>
      <path d="M700 60 Q705 80 700 100 Q695 80 700 60" fill="{rg(s,0.14)}"/>
      <path d="M720 110 Q725 130 720 150 Q715 130 720 110" fill="{rg(a,0.12)}"/>
      <path d="M680 140 Q685 160 680 180 Q675 160 680 140" fill="{rg(s,0.10)}"/>
      <path d="M60 880 Q65 900 60 920 Q55 900 60 880" fill="{rg(a,0.12)}"/>
      <path d="M90 920 Q95 940 90 960 Q85 940 90 960" fill="{rg(s,0.10)}"/>
      <path d="M680 870 Q685 890 680 910 Q675 890 680 870" fill="{rg(a,0.11)}"/>
      <path d="M710 920 Q715 940 710 960 Q705 940 710 960" fill="{rg(s,0.09)}"/>
      <!-- 斜雨 -->
      <path d="M300 30 Q305 45 302 60" stroke="{rg(a,0.10)}" stroke-width="1.5" fill="none"/>
      <path d="M350 20 Q355 35 352 50" stroke="{rg(s,0.08)}" stroke-width="1" fill="none"/>
      <path d="M450 40 Q455 55 452 70" stroke="{rg(a,0.09)}" stroke-width="1.5" fill="none"/>
    </svg>""",

        # ── 竹叶 ──
        "bamboo_leaf": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="50" cy="65" rx="40" ry="18" fill="{rg(a,0.14)}" transform="rotate(-25,50,65)"/>
      <ellipse cx="28" cy="100" rx="35" ry="16" fill="{rg(s,0.11)}" transform="rotate(-40,28,100)"/>
      <ellipse cx="55" cy="130" rx="32" ry="14" fill="{rg(a,0.09)}" transform="rotate(-15,55,130)"/>
      <ellipse cx="705" cy="90" rx="42" ry="19" fill="{rg(s,0.12)}" transform="rotate(22,705,90)"/>
      <ellipse cx="725" cy="135" rx="36" ry="16" fill="{rg(a,0.10)}" transform="rotate(38,725,135)"/>
      <ellipse cx="700" cy="165" rx="30" ry="13" fill="{rg(s,0.08)}" transform="rotate(12,700,165)"/>
      <ellipse cx="40" cy="880" rx="38" ry="17" fill="{rg(a,0.11)}" transform="rotate(-20,40,880)"/>
      <ellipse cx="22" cy="915" rx="32" ry="14" fill="{rg(s,0.09)}" transform="rotate(-35,22,915)"/>
      <ellipse cx="710" cy="950" rx="40" ry="18" fill="{rg(s,0.10)}" transform="rotate(18,710,950)"/>
      <ellipse cx="728" cy="985" rx="34" ry="15" fill="{rg(a,0.08)}" transform="rotate(32,728,985)"/>
    </svg>""",

        # ── 云朵 ──
        "cloud": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="100" cy="80" rx="65" ry="28" fill="{rg(s,0.12)}"/>
      <ellipse cx="70" cy="72" rx="45" ry="22" fill="{rg(a,0.09)}"/>
      <ellipse cx="130" cy="75" rx="40" ry="20" fill="{rg(p,0.07)}"/>
      <ellipse cx="660" cy="105" rx="60" ry="26" fill="{rg(a,0.11)}"/>
      <ellipse cx="690" cy="98" rx="42" ry="20" fill="{rg(s,0.08)}"/>
      <ellipse cx="640" cy="102" rx="35" ry="18" fill="{rg(p,0.06)}"/>
      <ellipse cx="80" cy="920" rx="55" ry="24" fill="{rg(s,0.10)}"/>
      <ellipse cx="55" cy="912" rx="38" ry="18" fill="{rg(a,0.07)}"/>
      <ellipse cx="695" cy="965" rx="58" ry="25" fill="{rg(a,0.09)}"/>
      <ellipse cx="720" cy="958" rx="40" ry="19" fill="{rg(s,0.07)}"/>
    </svg>""",

        # ── 粽叶 ──
        "zongye": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 宽长叶子 -->
      <path d="M40 40 Q50 100 35 180" stroke="{rg(a,0.15)}" stroke-width="3" fill="none"/>
      <ellipse cx="35" cy="60" rx="22" ry="40" fill="{rg(a,0.10)}" transform="rotate(-15,35,60)"/>
      <ellipse cx="40" cy="110" rx="20" ry="35" fill="{rg(s,0.08)}" transform="rotate(-10,40,110)"/>
      <ellipse cx="36" cy="155" rx="18" ry="30" fill="{rg(a,0.07)}" transform="rotate(-20,36,155)"/>
      <!-- 右侧 -->
      <path d="M720 60 Q710 130 725 200" stroke="{rg(s,0.14)}" stroke-width="3" fill="none"/>
      <ellipse cx="726" cy="85" rx="21" ry="38" fill="{rg(s,0.09)}" transform="rotate(15,726,85)"/>
      <ellipse cx="720" cy="138" rx="19" ry="33" fill="{rg(a,0.07)}" transform="rotate(10,720,138)"/>
      <!-- 底部 -->
      <path d="M50 870 Q58 930 45 1000" stroke="{rg(a,0.12)}" stroke-width="3" fill="none"/>
      <ellipse cx="44" cy="900" rx="18" ry="32" fill="{rg(a,0.08)}" transform="rotate(-12,44,900)"/>
      <path d="M700 920 Q708 975 695 1030" stroke="{rg(s,0.11)}" stroke-width="3" fill="none"/>
      <ellipse cx="694" cy="948" rx="17" ry="30" fill="{rg(s,0.07)}" transform="rotate(14,694,948)"/>
    </svg>""",

        # ── 元宝/金币 ──
        "coin": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 金币1 -->
      <circle cx="60" cy="75" r="22" fill="{rg(p,0.16)}"/>
      <circle cx="60" cy="75" r="17" fill="{rg(a,0.12)}"/>
      <circle cx="60" cy="75" r="12" fill="none" stroke="{rg(p,0.15)}" stroke-width="1"/>
      <text x="60" y="80" text-anchor="middle" font-size="14" font-weight="bold" fill="{rg(p,0.40)}">$</text>
      <!-- 金币2 -->
      <circle cx="700" cy="100" r="19" fill="{rg(p,0.14)}"/>
      <circle cx="700" cy="100" r="14" fill="{rg(a,0.10)}"/>
      <circle cx="700" cy="100" r="10" fill="none" stroke="{rg(p,0.12)}" stroke-width="1"/>
      <text x="700" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="{rg(p,0.35)}">$</text>
      <!-- 金币3 -->
      <circle cx="45" cy="920" r="18" fill="{rg(p,0.12)}"/>
      <circle cx="45" cy="920" r="14" fill="{rg(a,0.09)}"/>
      <text x="45" y="925" text-anchor="middle" font-size="11" font-weight="bold" fill="{rg(p,0.32)}">$</text>
      <!-- 金币4 -->
      <circle cx="710" cy="960" r="20" fill="{rg(p,0.11)}"/>
      <circle cx="710" cy="960" r="15" fill="{rg(a,0.08)}"/>
      <circle cx="710" cy="960" r="11" fill="none" stroke="{rg(p,0.10)}" stroke-width="1"/>
      <!-- 散落元宝 -->
      <path d="M90 140 Q100 130 105 140 Q115 150 105 155 Q100 165 90 155 Q80 150 90 140" fill="{rg(a,0.18)}"/>
      <path d="M650 200 Q658 192 662 200 Q670 208 662 212 Q658 220 650 212 Q642 208 650 200" fill="{rg(a,0.15)}"/>
    </svg>""",

        # ── 蝴蝶 ──
        "butterfly": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <!-- 蝴蝶1 -->
      <ellipse cx="70" cy="80" rx="25" ry="18" fill="{rg(a,0.15)}" transform="rotate(-20,70,80)"/>
      <ellipse cx="90" cy="75" rx="22" ry="16" fill="{rg(p,0.12)}" transform="rotate(15,90,75)"/>
      <ellipse cx="75" cy="100" rx="18" ry="12" fill="{rg(s,0.10)}" transform="rotate(-10,75,100)"/>
      <ellipse cx="90" cy="98" rx="15" ry="11" fill="{rg(a,0.09)}" transform="rotate(8,90,98)"/>
      <line x1="80" y1="85" x2="80" y2="110" stroke="{rg(p,0.20)}" stroke-width="1.5"/>
      <!-- 蝴蝶2 -->
      <ellipse cx="690" cy="110" rx="22" ry="16" fill="{rg(s,0.13)}" transform="rotate(18,690,110)"/>
      <ellipse cx="710" cy="105" rx="20" ry="14" fill="{rg(a,0.10)}" transform="rotate(-12,710,105)"/>
      <line x1="700" y1="112" x2="700" y2="135" stroke="{rg(s,0.18)}" stroke-width="1.5"/>
      <!-- 蝴蝶3 -->
      <ellipse cx="55" cy="920" rx="20" ry="14" fill="{rg(a,0.12)}" transform="rotate(-15,55,920)"/>
      <ellipse cx="72" cy="915" rx="18" ry="12" fill="{rg(p,0.09)}" transform="rotate(10,72,915)"/>
      <line x1="63" y1="925" x2="63" y2="948" stroke="{rg(p,0.16)}" stroke-width="1.2"/>
      <ellipse cx="700" cy="970" rx="22" ry="15" fill="{rg(s,0.11)}" transform="rotate(12,700,970)"/>
      <ellipse cx="718" cy="965" rx="19" ry="13" fill="{rg(a,0.08)}" transform="rotate(-8,718,965)"/>
      <!-- 蝴蝶须 -->
      <path d="M80 85 Q75 72 70 68" stroke="{rg(p,0.15)}" stroke-width="1" fill="none"/>
      <path d="M80 85 Q85 72 90 68" stroke="{rg(p,0.15)}" stroke-width="1" fill="none"/>
    </svg>""",

        # ── 光环 ──
        "halo": f"""
    <svg viewBox="0 0 750 1050" xmlns="http://www.w3.org/2000/svg">
      <circle cx="100" cy="80" r="35" fill="none" stroke="{rg(a,0.15)}" stroke-width="2"/>
      <circle cx="100" cy="80" r="45" fill="none" stroke="{rg(a,0.08)}" stroke-width="1.5"/>
      <circle cx="100" cy="80" r="55" fill="none" stroke="{rg(s,0.05)}" stroke-width="1"/>
      <circle cx="660" cy="110" r="30" fill="none" stroke="{rg(s,0.13)}" stroke-width="2"/>
      <circle cx="660" cy="110" r="40" fill="none" stroke="{rg(s,0.07)}" stroke-width="1.5"/>
      <circle cx="660" cy="110" r="50" fill="none" stroke="{rg(a,0.04)}" stroke-width="1"/>
      <circle cx="50" cy="920" r="28" fill="none" stroke="{rg(a,0.12)}" stroke-width="1.5"/>
      <circle cx="50" cy="920" r="38" fill="none" stroke="{rg(a,0.06)}" stroke-width="1"/>
      <circle cx="710" cy="960" r="32" fill="none" stroke="{rg(s,0.10)}" stroke-width="1.5"/>
      <circle cx="710" cy="960" r="42" fill="none" stroke="{rg(s,0.05)}" stroke-width="1"/>
    </svg>""",

    }

    return svgs.get(decor_type, svgs["roses"])


# ============================================================
# Google Fonts
# ============================================================
def get_font_import(style):
    base = "Noto+Serif+SC:wght@300;400;600;700&family=Noto+Sans+SC:wght@300;400&family=Ma+Shan+Zheng"
    if style["name_en"] in ("Tuscany", "Parisian", "Macaron", "Creamy", "HongKong"):
        base += "&family=ZCOOL+XiaoWei&family=ZCOOL+QingKe+HuangYou"
    return f"https://fonts.googleapis.com/css2?family={base}&display=swap"


# ============================================================
# CSS 生成
# ============================================================
def generate_css(style):
    return f"""
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    width: 750px;
    min-height: 1100px;
    background: {style['bg']};
    font-family: {style['body_font']};
    position: relative;
    overflow: hidden;
  }}

  /* 背景纹理层 - 细微底纹增加层次感 */
  body::before {{
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
      radial-gradient(ellipse at 20% 30%, {style['accent']}18 0%, transparent 50%),
      radial-gradient(ellipse at 80% 70%, {style['secondary']}15 0%, transparent 45%),
      radial-gradient(ellipse at 50% 50%, {style['primary']}08 0%, transparent 60%);
    z-index: 0;
    pointer-events: none;
  }}

  /* 背景细微纹理 */
  body::after {{
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    z-index: 0.1;
    pointer-events: none;
  }}

  /* 背景图 */
  .bg-image {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
  }}
  .bg-image img {{
    width: 100%; height: 100%;
    object-fit: cover;
  }}

  /* 背景遮罩（让文字更清晰，默认白色半透明） */
  .bg-overlay {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: {style.get("overlay_color", "rgba(255,255,255,0.75)")};
    z-index: 0.5;
  }}

  .decor {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 1;
  }}

  .container {{
    position: relative;
    z-index: 2;
    padding: 40px 38px 36px;
  }}

  .header {{
    text-align: center;
    margin-bottom: 22px;
  }}

  .greeting {{
    font-family: {style['label_font']};
    font-size: 20px;
    font-weight: 600;
    color: {style['text']};
    letter-spacing: 7px;
    margin-bottom: 5px;
  }}

  .date-label {{
    font-family: {style['greeting_font']};
    font-size: {style['greeting_size']};
    color: {style['date_color']};
    padding: 6px 20px;
    letter-spacing: 3px;
    margin-bottom: 6px;
  }}

  .weekday-badge {{
    display: inline-block;
    background: {style['card_bg']};
    color: {style['date_color']};
    font-size: 16px;
    font-weight: 400;
    letter-spacing: 2px;
    padding: 5px 20px;
    border-radius: 20px;
    box-shadow: 0 4px 16px {style['primary']}20;
    backdrop-filter: blur(8px);
  }}

  .divider {{
    text-align: center;
    margin: 14px 0 18px;
    color: {style['text_light']};
    font-size: 14px;
    letter-spacing: 10px;
    font-family: serif;
  }}

  .poem-wrap {{
    text-align: center;
    margin-bottom: 12px;
    padding: 12px 18px 10px;
    background: {style['card_bg']};
    border-radius: {style['card_radius']};
    border: 1px solid {style['secondary']}40;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 24px {style['primary']}15;
  }}

  .poem-text {{
    font-family: {style['body_font']};
    font-size: 17px;
    font-weight: 400;
    color: {style['text']};
    line-height: 2.4;
    letter-spacing: 1.5px;
    font-style: italic;
  }}

  .poem-text + .poem-text {{
    margin-top: 6px;
    padding-top: 8px;
    border-top: 1px dashed {style['secondary']}30;
  }}

  .section-label {{
    font-family: {style['label_font']};
    font-size: 14px;
    font-weight: 300;
    color: {style['text_light']};
    letter-spacing: 3px;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 6px;
  }}

  .weather-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-bottom: 12px;
  }}

  .city-card {{
    background: {style['card_bg']};
    border-radius: {style['card_radius']};
    padding: 10px 8px 8px;
    text-align: center;
    border: 1px solid {style['secondary']}35;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px {style['primary']}12;
  }}

  .city-name {{
    font-family: {style['label_font']};
    font-size: 14px;
    font-weight: 400;
    color: {style['text_light']};
    letter-spacing: 2px;
    margin-bottom: 3px;
  }}

  .temp-main {{
    font-family: {style['body_font']};
    font-size: 34px;
    font-weight: 700;
    color: {style['primary']};
    line-height: 1.1;
    margin-bottom: 3px;
  }}

  .temp-desc {{
    font-size: 15px;
    font-weight: 400;
    color: {style['text_light']};
  }}

  .weather-info {{
    margin: 5px 0;
    padding: 3px 0;
    border-top: 1px dashed {style['secondary']}25;
    border-bottom: 1px dashed {style['secondary']}25;
  }}

  .info-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: {style['label_font']};
    font-size: 14px;
    color: {style['text_light']};
    margin-bottom: 2px;
  }}

  .info-row:last-child {{
    margin-bottom: 0;
  }}

  .info-label {{
    font-weight: 500;
    color: {style['text_light']};
  }}

  .info-value {{
    color: {style['text']};
  }}


  .tips-row {{
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin-top: 6px;
  }}

  .tip-item {{
    font-family: {style['label_font']};
    font-size: 14px;
    color: {style['text_light']};
    letter-spacing: 0.5px;
  }}

  .indices-row {{
    display: flex;
    flex-wrap: nowrap;
    justify-content: center;
    gap: 4px;
    margin-top: 5px;
    padding-top: 5px;
    border-top: 1px dashed {style['secondary']}30;
    overflow: hidden;
  }}

  .idx-item {{
    font-family: {style['label_font']};
    font-size: 12px;
    color: {style['text_light']};
    background: {style['secondary']}15;
    padding: 2px 4px;
    border-radius: 4px;
    white-space: nowrap;
  }}

  .restriction-wrap {{
    background: {style['card_bg']};
    border-radius: {style['card_radius']};
    padding: 10px 16px;
    margin-bottom: 12px;
    border: 1px solid {style['secondary']}40;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px {style['primary']}15;
  }}

  .restriction-title {{
    font-family: {style['label_font']};
    font-size: 14px;
    font-weight: 300;
    color: {style['text_light']};
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
    text-align: center;
  }}

  .r-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px dashed {style['secondary']}30;
  }}

  .r-row:last-child {{ border-bottom: none; padding-bottom: 0; }}

  .r-day {{
    font-family: {style['label_font']};
    font-size: 14px;
    color: {style['text']};
  }}

  .r-num {{
    font-family: {style['body_font']};
    font-size: 15px;
    color: {style['primary']};
    font-weight: 600;
    background: {style['secondary']}25;
    padding: 3px 12px;
    border-radius: 14px;
  }}

  .no-restriction {{
    background: {style['secondary']}35;
    color: {style['primary']};
  }}

  .skincare-wrap {{
    background: {style['card_bg']};
    border-radius: {style['card_radius']};
    padding: 10px 16px;
    margin-bottom: 12px;
    border: 1px solid {style['secondary']}35;
    border-left: 3px solid {style['accent']};
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px {style['primary']}10;
  }}

  .sk-title {{
    font-family: {style['label_font']};
    font-size: 14px;
    font-weight: 400;
    color: {style['secondary']};
    letter-spacing: 3px;
    margin-bottom: 6px;
  }}

  .sk-content {{
    font-family: {style['body_font']};
    font-size: 16px;
    color: {style['text']};
    line-height: 2.2;
    letter-spacing: 0.5px;
  }}

  .footer {{
    text-align: center;
    padding-top: 6px;
  }}

  .footer-ornament {{
    color: {style['text_light']};
    font-size: 13px;
    letter-spacing: 14px;
    display: block;
    margin-bottom: 3px;
  }}

  .footer-text {{
    font-family: {style['greeting_font']};
    font-size: 17px;
    color: {style['text_light']};
    letter-spacing: 4px;
  }}

  .logo-wrap {{
    position: fixed;
    top: 24px;
    left: 24px;
    z-index: 100;
  }}

  .logo-wrap img {{
    max-height: 40px;
    max-width: 120px;
    object-fit: contain;
    opacity: 0.85;
  }}
"""






# ============================================================
# 构建 HTML
# ============================================================
def build_html(data, style=None):
    if style is None:
        style = get_style_for_date()

    # date_color 适配主题色，默认为 text 色
    if style.get('date_color') is None:
        style['date_color'] = style['text']

    # 背景使用预设的渐变色，不使用网搜图片
    bg_image_html = ""

    # 美文处理：短美文显示两条，长美文显示一条
    poem1 = data['poem1']
    poem2 = data['poem2']
    if len(poem1) >= 22:
        poem2_html = ""  # 长美文只显示一条
    else:
        poem2_html = f'      <div class="poem-text">{poem2}</div>\n'  # 短美文显示两条

    weather_list = data["weather_list"]
    restriction = data["restriction"]
    date_str = data["date"]
    weekday = data["weekday"]

    city_cards_html = ""
    for w in weather_list:
        city = w.get("city", "")
        now = w.get("now", {})
        today_f = w.get("today", {})
        tomorrow_f = w.get("tomorrow", {})
        uv = w.get("uv", "")
        dress = w.get("dress", "")
        air = w.get("air", "--")
        indices = w.get("indices", {})
        icon = weather_icon(now.get("text", ""))
        
        # 提取紫外线指数（更清晰的文字）
        if uv:
            uv_level = uv.split("（")[0] if "（" in uv else uv
            uv_text = f"紫外线 {uv_level}"
        else:
            uv_text = "紫外线 --"
        
        # 简化穿衣提示（去掉图标）
        dress_text = ""
        if dress:
            if "长袖" in dress:
                dress_text = "穿衣 长袖"
            elif "外套" in dress:
                dress_text = "穿衣 外套"
            elif "短袖" in dress:
                dress_text = "穿衣 短袖"
            elif "T恤" in dress:
                dress_text = "穿衣 T恤"
            else:
                dress_text = f"穿衣 {dress[:6]}"

        # AQI等级映射（去掉图标，改用完整文字）
        if isinstance(air, str):
            try:
                aqi_val = int(air)
                if aqi_val <= 50:
                    aqi_text = f"空气 {air} 优"
                elif aqi_val <= 100:
                    aqi_text = f"空气 {air} 良"
                elif aqi_val <= 150:
                    aqi_text = f"空气 {air} 轻度污染"
                elif aqi_val <= 200:
                    aqi_text = f"空气 {air} 中度污染"
                elif aqi_val <= 300:
                    aqi_text = f"空气 {air} 重度污染"
                else:
                    aqi_text = f"空气 {air} 严重污染"
            except:
                aqi_text = f"空气 {air}"
        else:
            aqi_text = "空气 --"

        # 风力描述
        wind_info = f"{now.get('windDir', '')}{now.get('windScale', '')}" if now.get('windScale') else ""
        
        # 构建天气描述: 当前天气 → 今日天气（风力）
        if wind_info:
            weather_desc = f"{now.get('text', '--')} → {today_f.get('textDay', '--')}（{wind_info}）"
        else:
            weather_desc = f"{now.get('text', '--')} → {today_f.get('textDay', '--')}"

        # 和风天气生活指数
        indices = w.get("indices", {})
        
        # 运动指数 (type=1)
        sport_idx = indices.get("1", {})
        sport_text = sport_idx.get("category", "") if sport_idx else ""
        
        # 洗车指数 (type=2)
        car_idx = indices.get("2", {})
        car_text = car_idx.get("category", "") if car_idx else ""
        
        # 过敏指数 (type=7)
        allergy_idx = indices.get("7", {})
        allergy_text = allergy_idx.get("category", "") if allergy_idx else ""
        
        # 太阳镜指数 (type=12)
        sunglass_idx = indices.get("12", {})
        sunglass_text = sunglass_idx.get("category", "") if sunglass_idx else ""

        city_cards_html += f"""
        <div class="city-card">
            <div class="city-name">{city}</div>
            <div class="temp-main">{now.get('temp', '--')}° <span class="temp-desc">{icon} {weather_desc}</span></div>
            <div class="weather-info">
                <div class="info-row">
                    <span class="info-label">今日</span>
                    <span class="info-value">{today_f.get('textDay', '--')} {today_f.get('tempMin', '--')}° ~ {today_f.get('tempMax', '--')}°</span>
                </div>
                <div class="info-row">
                    <span class="info-label">明日</span>
                    <span class="info-value">{tomorrow_f.get('textDay', '--')} {tomorrow_f.get('tempMin', '--')}° ~ {tomorrow_f.get('tempMax', '--')}°</span>
                </div>
                <div class="info-row">
                    <span class="info-label">湿度</span>
                    <span class="info-value">{now.get('humidity', '--')}%</span>
                </div>
            </div>
            <div class="tips-row">
                <span class="tip-item">{uv_text}</span>
                <span class="tip-item">{dress_text}</span>
                <span class="tip-item">{aqi_text}</span>
            </div>
            <div class="indices-row">
                <span class="idx-item">🏃 {sport_text}</span>
                <span class="idx-item">🚗<sup>🚿</sup> {car_text}</span>
                <span class="idx-item">🕶 {sunglass_text}</span>
                <span class="idx-item">🤧 {allergy_text}</span>
            </div>
        </div>"""

    today_r = restriction["today_restriction"]
    tomorrow_r = restriction["tomorrow_restriction"]
    today_date = restriction["today_date"]
    today_week = restriction["today_week"]
    tomorrow_date = restriction["tomorrow_date"]
    tomorrow_week = restriction["tomorrow_week"]

    # 根据风格选择合适的 LOGO
    logo_path = select_logo_by_style(style)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Daily Card</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="{get_font_import(style)}" rel="stylesheet">
<style>{generate_css(style)}</style>
</head>
<body>
  {bg_image_html}
  <div class="decor">
    {get_decoration(style['decor'], style)}
  </div>

  <div class="logo-wrap">
    <img src="file:///{logo_path.replace(chr(92), '/')}" alt="logo">
  </div>

  <div class="container">
    <div class="header">
      <div class="greeting">{style['greeting']}</div>
      <div class="date-label">{date_str}</div>
      <div class="weekday-badge">{weekday}</div>
    </div>

    <div class="divider">{style['divider']}</div>

    <div class="poem-wrap">
      <div class="poem-text">{poem1}</div>
{poem2_html}    </div>

    <div class="section-label">今日天气</div>
    <div class="weather-grid">{city_cards_html}</div>

    <div class="restriction-wrap">
      <div class="restriction-title">成都限号</div>
      <div class="r-row">
        <span class="r-day">{today_date} {today_week}</span>
        <span class="r-num {'no-restriction' if '不限' in today_r else ''}">{today_r}</span>
      </div>
      <div class="r-row">
        <span class="r-day">{tomorrow_date} {tomorrow_week}</span>
        <span class="r-num {'no-restriction' if '不限' in tomorrow_r else ''}">{tomorrow_r}</span>
      </div>
    </div>

    <div class="skincare-wrap">
      <div class="sk-title">✧ 今日护肤小贴士</div>
      <div class="sk-content">{data['skincare_tip']}</div>
    </div>

    <div class="footer">
      <span class="footer-ornament">{style['divider']}</span>
      <div class="footer-text">{style['footer']}</div>
    </div>
  </div>
</body>
</html>"""


# ============================================================
# 生成图片
# ============================================================
def generate_image(data, output_path, style=None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    html_content = build_html(data, style)

    tmp_html = os.path.join(tempfile.gettempdir(), "daily_card_tmp.html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    file_url = "file:///" + tmp_html.replace("\\", "/")

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge", headless=True)
            page = browser.new_page(viewport={"width": 750, "height": 1100})
            page.goto(file_url, wait_until="networkidle", timeout=25000)
            page.wait_for_timeout(1500)
            page.screenshot(path=output_path, type="png")
            browser.close()
        print(f"[✓] {output_path}")
        return True
    except Exception as e:
        print(f"[✗] 失败: {e}")
        return False


def generate_images(data, output_paths, styles):
    """
    批量生成多张日签图片
    
    Args:
        data: 日签数据
        output_paths: 输出路径列表
        styles: 主题列表（与output_paths一一对应）
    
    Returns:
        bool: 是否全部成功
    """
    results = []
    for i, (path, style) in enumerate(zip(output_paths, styles)):
        style_name = style.get('name', f'Style-{i+1}')
        print(f"  [{i+1}/{len(output_paths)}] 生成 {style_name} ...", end=" ", flush=True)
        ok = generate_image(data, path, style)
        results.append(ok)
        if not ok:
            print(f"[重试]", end=" ", flush=True)
            ok = generate_image(data, path, style)
            results[-1] = ok
        print("✓" if ok else "✗")
    
    return all(results)


# ============================================================
# 生成所有 96 种风格预览（72种常规 + 24种节日）
# ============================================================
if __name__ == "__main__":
    test_data = {
        "date": "2026年04月03日",
        "weekday": "周五",
        "weather_list": [
            {"city": "仁寿", "now": {"temp": "18", "text": "多云"}, "today": {"tempMax": "22", "tempMin": "14"}, "uv": "较弱防晒", "dress": "薄外套", "air": "良"},
            {"city": "成都", "now": {"temp": "17", "text": "阴"}, "today": {"tempMax": "20", "tempMin": "13"}, "uv": "无需防晒", "dress": "外套", "air": "良"},
        ],
        "restriction": {
            "today_date": "04月03日", "today_week": "周五", "today_restriction": "尾号 5、0 限行",
            "tomorrow_date": "04月04日", "tomorrow_week": "周六", "tomorrow_restriction": "不限行",
        },
        "skincare_tip": "春季皮肤敏感，换季时请先做局部测试再更换新护肤品。",
        "poem1": "春水初生，春林初盛，春风十里，不如你。—— 冯唐",
        "poem2": "愿你所有的清晨都明亮，所有的傍晚都温柔。",
    }

    output_dir = os.path.dirname(os.path.abspath(__file__)) + "/output"
    os.makedirs(output_dir, exist_ok=True)

    # 生成全部 72 种常规风格预览
    print("=" * 50)
    print("生成全部 72 种常规风格预览 (S01-S72)...")
    print("=" * 50)

    for i, style in enumerate(REGULAR_STYLES):
        name_safe = style["name_en"]
        output = os.path.join(output_dir, f"S{i+1:02d}_{name_safe}.png")
        print(f"[{i+1:02d}/72] {style['name']} ({name_safe})", end=" ... ")
        ok = generate_image(test_data, output, style)
        if not ok:
            print(f"  [重试]", end=" ")
            generate_image(test_data, output, style)

    # 生成全部 24 种节日风格预览
    print("\n" + "=" * 50)
    print("生成全部 24 种节日风格预览 (H01-H24)...")
    print("=" * 50)

    for i, style in enumerate(HOLIDAY_STYLES):
        name_safe = style["name_en"]
        output = os.path.join(output_dir, f"H{i+1:02d}_{name_safe}.png")
        print(f"[{i+1:02d}/24] {style['name']} ({name_safe})", end=" ... ")
        ok = generate_image(test_data, output, style)
        if not ok:
            print(f"  [重试]", end=" ")
            generate_image(test_data, output, style)

    print("\n" + "=" * 50)
    print(f"✓ 完成！共生成 96 种风格预览")
    print(f"  - 常规主题: 72 种 (S01-S72)")
    print(f"  - 节日主题: 24 种 (H01-H24)")
    print(f"  - 保存位置: {output_dir}")
    print("=" * 50)
