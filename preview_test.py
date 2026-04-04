"""
快速生成 HTML 预览（不需要 Playwright，直接查看效果）
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from card_generator import build_html

test_data = {
    "date": "2026年04月03日",
    "weekday": "周五",
    "weather_list": [
        {
            "city": "仁寿",
            "now": {"temp": "18", "text": "多云", "humidity": "75", "windDir": "东北风", "windScale": "2"},
            "today": {"tempMax": "22", "tempMin": "14", "textDay": "多云", "textNight": "小雨"},
            "uv": "较弱（建议涂SPF30）",
            "dress": "建议穿薄外套，内搭长袖",
            "air": "良",
        },
        {
            "city": "成都",
            "now": {"temp": "17", "text": "阴", "humidity": "80", "windDir": "东风", "windScale": "1"},
            "today": {"tempMax": "20", "tempMin": "13", "textDay": "阴", "textNight": "阵雨"},
            "uv": "弱（无需特别防晒）",
            "dress": "外套+雨伞备用",
            "air": "良",
        },
    ],
    "restriction": {
        "today_date": "04月03日",
        "today_week": "周五",
        "today_restriction": "尾号 5、0 限行",
        "tomorrow_date": "04月04日",
        "tomorrow_week": "周六",
        "tomorrow_restriction": "不限行",
    },
    "skincare_tip": "春季皮肤敏感期，换季时请先做局部测试再更换新护肤品。建议精简护肤步骤，以修护屏障为主。",
    "poem1": "春水初生，春林初盛，春风十里，不如你。—— 冯唐",
    "poem2": "愿你所有的清晨都明亮，所有的傍晚都温柔。",
}

html = build_html(test_data)
output_path = "C:/Users/30286/WorkBuddy/20260403180838/daily-card/output/preview.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"HTML预览已生成: {output_path}")
