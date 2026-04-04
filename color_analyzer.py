"""
图片配色分析模块
使用 colorthief 提取图片主色调，生成配色方案和匹配尾文
"""
import requests
import io
import datetime
from colorthief import ColorThief


def analyze_background_colors(image_url: str) -> dict:
    """
    分析背景图颜色，生成配色方案
    
    Returns:
        dict: {
            'primary_color': '#RRGGBB',
            'secondary_color': '#RRGGBB',
            'text_color': '#RRGGBB',  # 适合文字的颜色
            'accent_color': '#RRGGBB',
            'tone': '暖色调/冷色调/中性',
            'mood': '描述图片氛围的关键词'
        }
    """
    try:
        # 下载图片
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        image_data = io.BytesIO(response.content)
        
        # 使用 colorthief 提取主色调
        color_thief = ColorThief(image_data)
        
        # 获取主色
        primary_rgb = color_thief.get_color(quality=3)
        # 获取调色板（5个颜色）
        palette = color_thief.get_palette(color_count=5, quality=3)
        
        # 转换为16进制
        primary = '#{:02x}{:02x}{:02x}'.format(*primary_rgb)
        
        # 选择对比度较好的次色
        secondary = '#{:02x}{:02x}{:02x}'.format(*palette[1]) if len(palette) > 1 else primary
        
        # 分析色调
        r, g, b = primary_rgb
        if r > 150 and g > 120 and b > 100:
            tone = "暖色调"
            mood = "温暖阳光"
        elif r < 100 and g < 120 and b > 150:
            tone = "冷色调"
            mood = "宁静清凉"
        elif r > 150 and g < 120 and b < 120:
            tone = "红色调"
            mood = "热烈活力"
        elif r < 120 and g > 150 and b < 120:
            tone = "绿色调"
            mood = "自然清新"
        elif r > 150 and g > 150 and b < 120:
            tone = "橙黄色调"
            mood = "明快活力"
        else:
            tone = "中性色调"
            mood = "沉稳内敛"
        
        # 计算适合文字的颜色（根据背景亮度）
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        if brightness > 128:
            text_color = '#1a1a1a'  # 深色文字
            accent_color = '#333333'
        else:
            text_color = '#ffffff'  # 浅色文字
            accent_color = '#f0f0f0'
        
        return {
            'primary_color': primary,
            'secondary_color': secondary,
            'text_color': text_color,
            'accent_color': accent_color,
            'tone': tone,
            'mood': mood
        }
        
    except Exception as e:
        print(f"[颜色分析] 分析失败: {e}")
        # 返回默认配色
        return {
            'primary_color': '#4A90A4',
            'secondary_color': '#F5F5F5',
            'text_color': '#333333',
            'accent_color': '#666666',
            'tone': '中性色调',
            'mood': '沉稳内敛'
        }


def generate_tail_text(mood: str, tone: str) -> str:
    """
    根据图片氛围生成匹配的尾文
    
    Args:
        mood: 图片氛围描述
        tone: 图片色调
    
    Returns:
        str: 8-12字的中文尾文
    """
    today = datetime.date.today()
    weekday = today.weekday()
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    day_name = weekdays[weekday]
    
    # 尾文模板库（按氛围分类）
    tail_templates = {
        "温暖阳光": [
            "阳光正好，未来可期",
            "温暖前行，不负韶华",
            "阳光万里，岁月静好",
            "温暖如初，生活明朗"
        ],
        "宁静清凉": [
            "心静如水，岁月安然",
            "清凉一夏，宁静致远",
            "静享时光，岁月温柔",
            "宁静淡雅，心生欢喜"
        ],
        "热烈活力": [
            "热爱生活，逐梦前行",
            "激情燃烧，奔赴山海",
            "心怀热忱，不负热爱",
            "活力满满，未来可期"
        ],
        "自然清新": [
            "自然相伴，心生明媚",
            "清新自在，岁月如歌",
            "绿意盎然，生活可爱",
            "自然之美，心旷神怡"
        ],
        "明快活力": [
            "明亮前行，万事可期",
            "阳光满路，温暖如初",
            "明朗坦荡，所向披靡",
            "光明在望，勇敢前行"
        ],
        "沉稳内敛": [
            "静水深流，厚积薄发",
            "沉稳有力，行稳致远",
            "低调内敛，高调前行",
            "沉稳岁月，静待花开"
        ]
    }
    
    # 根据星期微调
    if weekday in [0, 1]:  # 周一、周二 - 鼓励型
        modifiers = ["新的一周，加油！", "美好开始", "元气满满"]
    elif weekday in [2, 3]:  # 周三、周四 - 坚持型
        modifiers = ["坚持就是胜利", "继续努力", "不负期待"]
    else:  # 周五、周六、周日 - 放松型
        modifiers = ["周末愉快", "放松一下", "享受生活"]
    
    # 获取对应氛围的尾文
    templates = tail_templates.get(mood, tail_templates["沉稳内敛"])
    import random
    base_text = random.choice(templates)
    modifier = random.choice(modifiers)
    
    return f"{base_text} · {modifier}"


if __name__ == "__main__":
    # 测试
    test_url = "https://picsum.photos/seed/dailycard-20260403/750/1100"
    print("分析背景图颜色...")
    colors = analyze_background_colors(test_url)
    print(f"主色调: {colors['primary_color']} ({colors['tone']})")
    print(f"氛围: {colors['mood']}")
    print(f"文字色: {colors['text_color']}")
    
    print("\n生成尾文:")
    tail = generate_tail_text(colors['mood'], colors['tone'])
    print(tail)
