"""
小红书内容抓取模块
直接从网页版 API 获取美文和护肤贴士
"""

import requests
import random
import re
from datetime import datetime


# 小红书搜索接口（网页版）
XHS_SEARCH_URL = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.xiaohongshu.com",
}

# 缓存
_cache = {
    "beauty_texts": [],
    "skincare_tips": [],
    "last_fetch": None
}


def _make_request(keyword: str, page: int = 1) -> list:
    """搜索小红书笔记"""
    try:
        payload = {
            "keyword": keyword,
            "page": page,
            "page_size": 20,
            "search_id": "".join(random.choices("0123456789abcdef", k=32)),
            "sort": "general",  # 综合排序
            "note_type": "normal",
            "ext_flags": [],
            "image_formats": ["jpg", "webp", "avif"]
        }
        
        resp = requests.post(XHS_SEARCH_URL, json=payload, headers=HEADERS, timeout=10)
        data = resp.json()
        
        if data.get("success") and "items" in data.get("data", {}):
            return data["data"]["items"]
        return []
    except Exception as e:
        print(f"[小红书抓取失败] {keyword}: {e}")
        return []


def _extract_text(item: dict) -> str:
    """从笔记项中提取正文内容"""
    try:
        note_card = item.get("note_card", {})
        # 尝试不同字段
        title = note_card.get("title", "")
        desc = note_card.get("desc", "")
        
        # 清理 HTML 标签和特殊字符
        text = desc or title
        text = re.sub(r'<[^>]+>', '', text)  # 去除 HTML 标签
        text = re.sub(r'\[.*?\]', '', text)  # 去除表情标签
        text = re.sub(r'#\S+', '', text)     # 去除话题标签
        text = re.sub(r'\n+', ' ', text)     # 换行变空格
        text = text.strip()
        
        return text if len(text) >= 10 else ""
    except:
        return ""


def fetch_beauty_texts(count: int = 5) -> list:
    """
    获取美文/励志文案
    搜索关键词：早安文案、励志文案、治愈文案
    """
    keywords = ["早安文案", "励志文案", "治愈文案", "温暖文案", "生活文案"]
    texts = []
    
    for kw in keywords[:3]:  # 最多搜索3个关键词
        items = _make_request(kw)
        for item in items[:3]:  # 每个关键词取3条
            text = _extract_text(item)
            if text and text not in texts:
                texts.append(text)
            if len(texts) >= count * 2:
                break
        if len(texts) >= count * 2:
            break
    
    if texts:
        _cache["beauty_texts"] = texts
        return random.sample(texts, min(count, len(texts)))
    
    # 备用本地库
    return _get_fallback_beauty_texts(count)


def fetch_skincare_tips(count: int = 5) -> list:
    """
    获取护肤贴士
    根据当前季节搜索相关护肤内容
    """
    month = datetime.now().month
    
    # 根据季节选择关键词
    if 3 <= month <= 5:
        season_keywords = ["春季护肤", "换季护肤", "春天护肤小知识", "敏感肌护肤"]
    elif 6 <= month <= 8:
        season_keywords = ["夏季护肤", "控油防晒", "夏天护肤", "油皮护肤"]
    elif 9 <= month <= 11:
        season_keywords = ["秋季护肤", "换季护肤", "秋冬护肤", "保湿护肤"]
    else:
        season_keywords = ["冬季护肤", "保湿补水", "冬天护肤", "干皮护肤"]
    
    tips = []
    
    for kw in season_keywords:
        items = _make_request(kw)
        for item in items[:3]:
            text = _extract_text(item)
            # 过滤太短或太长的内容
            if 20 <= len(text) <= 200 and text not in tips:
                tips.append(text)
            if len(tips) >= count * 2:
                break
        if len(tips) >= count * 2:
            break
    
    if tips:
        _cache["skincare_tips"] = tips
        return random.sample(tips, min(count, len(tips)))
    
    # 备用本地库
    return _get_fallback_skincare_tips(count)


def _get_fallback_beauty_texts(count: int) -> list:
    """本地备用美文库"""
    fallbacks = [
        "每一个清晨都是新的开始，愿你的笑容比阳光更灿烂。",
        "生活不在别处，就在当下这一刻，珍惜眼前人，做好眼前事。",
        "愿你被世界温柔以待，也愿你温柔待这个世界。",
        "早安！今天也要元气满满地生活呀。",
        "世间美好，与你环环相扣，愿你的每一天都闪闪发光。",
        "心有阳光，何惧风雨，愿你眼中总有光芒，活成你想要的模样。",
    ]
    return random.sample(fallbacks, min(count, len(fallbacks)))


def _get_fallback_skincare_tips(count: int) -> list:
    """本地备用护肤库（按季节）"""
    month = datetime.now().month
    
    if 3 <= month <= 5:
        tips = [
            "春季皮肤敏感，换新护肤品时请先在耳后测试。",
            "春季花粉增多，外出回来记得用温水清洁面部。",
            "春季保湿很重要，补水精华+锁水面霜是黄金搭档。",
            "春天紫外线渐强，防晒建议升级到SPF50+。",
        ]
    elif 6 <= month <= 8:
        tips = [
            "夏季高温出汗多，防晒记得2小时补涂一次。",
            "控油是夏季重点，T区可用吸油纸轻压。",
            "夏季卸妆要彻底，防晒残留会堵塞毛孔。",
            "定妆喷雾代替散粉，保湿又控油。",
        ]
    elif 9 <= month <= 11:
        tips = [
            "秋季换季暂停去角质，以修护屏障为主。",
            "秋燥当道，增加玻尿酸、神经酰胺类成分。",
            "秋季是使用维A醇的好时机，夜间少量涂抹。",
            "眼部保湿不可少，细纹从缺水开始。",
        ]
    else:
        tips = [
            "冬季洗脸水温38℃最佳，过热破坏天然油脂。",
            "层层锁水：爽肤水→精华→面霜，不留死角。",
            "空调房放加湿器，皮肤水分蒸发速度降低30%。",
            "加一滴玫瑰果油混合面霜，保湿力翻倍。",
        ]
    
    return random.sample(tips, min(count, len(tips)))


def get_beauty_text() -> str:
    """获取单条美文"""
    texts = fetch_beauty_texts(5)
    return texts[0] if texts else "早安，愿你今天心情美好。"


def get_skincare_tip() -> str:
    """获取单条护肤贴士"""
    tips = fetch_skincare_tips(5)
    return tips[0] if tips else "今日护肤建议：做好基础保湿，保持好心情。"


def fetch_daily_card_background() -> str:
    """
    获取每日日签背景图
    根据季节智能选择主题：
    - 春夏（3-8月）：暖色系、海蓝、盛放的花、湖蓝、绿树、花海、海边
    - 秋天（9-11月）：可出现秋天意象
    - 冬天（12-2月）：永远不出现冬天意象，改用温暖室内/暖色系
    """
    import datetime
    
    today = datetime.date.today()
    month = today.month
    
    # 春夏（3-8月）：暖色系/海蓝/花卉/绿树/花海/海边
    spring_summer_seeds = [
        "pink-flowers-garden", "blue-ocean-beach", "lavender-field-purple",
        "sunny-meadow-green", "rose-garden-red", "blue-lake-water",
        "cherry-blossom-pink", "tropical-beach-sunset", "flower-field-colors",
        "green-forest-light", "ocean-waves-blue", "tulip-garden-spring",
        "yellow-sunflower-field", "seaside-morning-sun", "pink-peonies-bloom",
        "turquoise-sea-calm", "wildflower-meadow", "sunrise-over-ocean",
        "lotus-pond-pink", "coastal-sunshine", "butterfly-flowers",
        "iris-purple-blue", "hydrangea-blue-pink", "coral-reef-ocean"
    ]
    
    # 秋天（9-11月）：可以出现秋天意象
    autumn_seeds = [
        "autumn-leaves-orange", "golden-forest-fall", "pumpkin-patch",
        "maple-red-leaves", "fall-sunrise-warm", "harvest-golden-field",
        "autumn-pathway", "fall-foliage-colors", "rustic-harvest",
        "golden-hour-autumn", "warm-autumn-sun", "fall-lake-calm"
    ]
    
    # 冬天（12-2月）：永远不出现冬天意象，用温暖室内/暖色/艺术
    winter_seeds = [
        "warm-cozy-interior", "golden-hour-light", "candlelight-warm",
        "sunlit-curtains", "cozy-reading-corner", "warm-rose-petals",
        "soft-pink-silk", "champagne-golden", "elegant-pearl-white",
        "sunrise-pink-horizon", "warm-terracotta", "burgundy-wine",
        "antique-gold-frame", "velvet-rose", "copper-metallic-shine"
    ]
    
    # 根据季节选择seed池
    if 3 <= month <= 5:  # 春季
        seed_pool = spring_summer_seeds[:16]  # 纯春季+春日感
    elif 6 <= month <= 8:  # 夏季
        seed_pool = [s for s in spring_summer_seeds if any(k in s for k in ['ocean', 'beach', 'blue', 'sea', 'sunset', 'tropical', 'sunshine', 'coastal'])] + spring_summer_seeds[:8]
        seed_pool = list(dict.fromkeys(seed_pool))  # 去重
    elif 9 <= month <= 11:  # 秋季
        # 秋天可以混合：60%秋天色 + 40%春夏暖色
        seed_pool = autumn_seeds + spring_summer_seeds[:10]
    else:  # 冬天（12-2月）
        # 永远不用冬天意象，用温暖室内/暖色
        seed_pool = winter_seeds + [s for s in spring_summer_seeds if any(k in s for k in ['sun', 'warm', 'golden', 'rose', 'pink'])][:5]
    
    # 用日期作为随机种子，确保同一天固定图片
    import hashlib
    day_seed = f"daily-{today.year}{today.month:02d}{today.day:02d}"
    hash_val = int(hashlib.md5(day_seed.encode()).hexdigest()[:8], 16)
    random.seed(hash_val)
    
    chosen_seed = random.choice(seed_pool)
    print(f"[季节背景] {month}月，选择主题: {chosen_seed}")
    
    # 恢复随机种子（不影响其他随机逻辑）
    random.seed()
    
    # Lorem Picsum URL
    image_url = f"https://picsum.photos/seed/{chosen_seed}/750/1100"
    print(f"[免费图库] 获取背景图: {image_url}")
    return image_url


if __name__ == "__main__":
    print("=== 测试小红书抓取 ===")
    print("\n美文：")
    for t in fetch_beauty_texts(3):
        print(f"  - {t[:50]}...")
    
    print("\n护肤贴士：")
    for t in fetch_skincare_tips(3):
        print(f"  - {t[:50]}...")
