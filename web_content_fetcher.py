"""
全网内容搜索模块 v3
使用全网搜索获取美文和护肤贴士
"""
import requests, random, re
from datetime import datetime
from bs4 import BeautifulSoup

POLITICAL_WORDS = ["领导", "主席", "总理", "总书记", "台独", "港独", "藏独", "国民党", "共产党", "党中央", "国务院"]

def _is_safe(text):
    for w in POLITICAL_WORDS:
        if w in text:
            return False
    return True

def _fetch_ddg(keyword, limit=10):
    try:
        url = f"https://html.duckduckgo.com/html/?q={keyword}"
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for item in soup.select(".result__snippet")[:limit]:
            text = item.get_text()
            text = re.sub(r"<[^>]+>", "", text).strip()
            if 15 < len(text) < 200:
                results.append(text)
        return results
    except:
        return []

def _fetch_zhihu():
    try:
        url = "https://www.zhihu.com/api/v4/articles/topstory/hot-lists/total?limit=10"
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        data = resp.json()
        results = []
        for item in data.get("data", [])[:5]:
            text = item.get("excerpt") or item.get("title", "")
            if 15 < len(text) < 150 and _is_safe(text):
                results.append(text)
        return results
    except:
        return []

BEAUTY_TEXTS = {
    "spring": ["春水初生，春林初盛，春风十里，不如你。", "人间四月天，最美是烟雨，最暖是晴日。", "愿你所有的清晨都明亮，所有的傍晚都温柔。", "没有一个春天不会到来，没有一个早晨不会开始。", "微风吹梦，星光落肩，今天也是被偏爱的一天。", "愿你眼里有光，心里有爱，遇见皆是温柔。", "春暖花开，奔你而来。", "春天来了，所有的美好都会如约而至。"],
    "summer": ["夏天的风吹过，带走了所有的烦恼和忧愁。", "愿你的夏天有西瓜、有空调、有好心情。", "阳光很暖，电量很满，今天也是元气满满的一天。", "夏日悠悠，愿你所得皆所愿，所遇皆所求。", "热烈的夏天，要有炽热的梦想和滚烫的人生。", "蝉鸣是夏天的信使。", "西瓜空调冰淇淋，陪你度过整个夏天。"],
    "autumn": ["秋风起，叶落知多少，愿你心里有暖阳。", "人间朝暮，叶落惊秋，愿你从容又温柔。", "莫道桑榆晚，为霞尚满天。", "秋天适合思念，更适合见面。", "人间值得，余生漫长，请你慢慢来。", "一叶知秋。", "糖炒栗子和枫叶是秋天的出生证明。"],
    "winter": ["冬日暖阳，好日常在，人间烟火，谁能不爱。", "愿你三冬暖，愿你春不寒，愿你天黑有灯下雨有伞。", "把每一个平凡的日子，过成诗意的模样。", "在最冷的季节，做最温暖的自己。", "围炉煮茶，岁月静好。", "冬天来了，春天还会远吗？"],
    "holiday": ["新年快乐！愿你在新的一年里，所有的美好都会发生。", "爆竹声中一岁除，春风送暖入屠苏。", "愿你眉目舒展，顺问冬安。", "愿得一人心，白首不相离。", "三尺讲台，三寸舌，三千桃李。感谢恩师！"],
    "default": ["每一个清晨都是新的开始，愿你的笑容比阳光更灿烂。", "生活不在别处，就在当下这一刻。", "愿你被世界温柔以待，也愿你温柔待这个世界。", "世间美好，与你环环相扣。", "心有阳光，何惧风雨。", "愿你眼中总有光芒，活成你想要的模样。", "时光不语，却温柔回答了所有问题。", "一花一叶，皆是风景；一朝一暮，皆是良辰。", "世界辽阔，生活温柔。", "温柔半两，从容一生。"],
}

SKINCARE_TIPS = {
    "spring": ["【换季护肤】春季皮肤屏障脆弱，换新护肤品时请先在耳后做24小时局部测试。", "【防敏攻略】春季花粉浓度高，外出回家后用温和氨基酸洁面彻底清洁。", "【防晒升级】春季紫外线指数上升，建议将防晒升级至SPF50+，阴天也要涂！", "【补水黄金期】春季皮肤新陈代谢加快，是补水的最佳时节。"],
    "summer": ["【防晒补涂】高温出汗多，防晒霜建议2小时补涂一次，重点照顾额头、鼻翼。", "【控油攻略】夏季油脂分泌旺盛，早晚用清爽型洁面，配合含茶树产品。", "【防晒真相】防晒是最具性价比的抗衰投资，比任何贵妇精华都管用！", "【晒后修复】皮肤被晒红后，用芦荟胶或冷藏补水面膜镇定。"],
    "autumn": ["【换季过渡】秋季湿度下降，角质层变薄，暂停强功效型产品，以修护屏障为主。", "【保湿成分】秋季推荐含玻尿酸、神经酰胺、角鲨烷的护肤品。", "【维A醇时机】秋季凉爽，是使用维A醇（抗衰金标准）的最佳季节。"],
    "winter": ["【水温控制】冬季洗脸水温38℃最佳，过热会破坏皮脂膜。", "【锁水步骤】冬季护肤顺序：爽肤水→精华→面霜，层层锁水。", "【以油养肤】冬季可尝试在面霜中滴入1-2滴玫瑰果油，保湿力显著提升。", "【唇部护理】睡前厚涂凡士林或专业唇膜，第二天嘴唇超级嫩滑。"],
}

def _get_season():
    month = datetime.now().month
    if 3 <= month <= 5: return "spring"
    elif 6 <= month <= 8: return "summer"
    elif 9 <= month <= 11: return "autumn"
    else: return "winter"

def _is_holiday():
    """检测今天是否是节日"""
    m, d = datetime.now().month, datetime.now().day
    holidays = {(1, 1): '元旦', (2, 14): '情人节', (3, 8): '妇女节',
                (5, 1): '劳动节', (6, 1): '儿童节', (10, 1): '国庆',
                (12, 25): '圣诞', (12, 31): '跨年'}
    return (m, d) in holidays

def fetch_beauty_texts(count=3):
    results = []
    # 节日抓取特殊关键词
    holiday_keywords = {"元旦": "新年文案", "情人节": "爱情文案", "妇女节": "女性力量",
                       "劳动节": "奋斗文案", "儿童节": "童心文案", "国庆": "爱国文案",
                       "圣诞": "圣诞文案", "跨年": "跨年文案"}
    
    zhihu = _fetch_zhihu()
    results.extend([t for t in zhihu if _is_safe(t)])
    
    # 节日优先抓取
    if _is_holiday():
        for kw in holiday_keywords.values():
            items = _fetch_ddg(kw)
            results.extend([t for t in items if _is_safe(t)])
    else:
        keywords = ["早安文案", "励志文案", "治愈文案"]
        for kw in keywords:
            items = _fetch_ddg(kw)
            results.extend([t for t in items if _is_safe(t)])
    
    # 本地备用
    season = _get_season()
    fallback = BEAUTY_TEXTS.get(season, BEAUTY_TEXTS["default"])
    if _is_holiday():
        fallback += BEAUTY_TEXTS.get("holiday", [])
    fallback += BEAUTY_TEXTS["default"]
    results.extend(random.sample(fallback, min(5, len(fallback))))
    unique = list(dict.fromkeys(results))
    return random.sample(unique, min(count, len(unique)))

def fetch_skincare_tips(count=3):
    results = []
    season = _get_season()
    keywords = {"spring": ["春季护肤", "换季护肤"], "summer": ["夏季护肤", "控油防晒"], 
                "autumn": ["秋季护肤", "保湿修护"], "winter": ["冬季护肤", "保湿补水"]}
    
    # 节日护肤关键词
    holiday_keywords = {"元旦": "新年护肤", "情人节": "约会护肤", "妇女节": "女性护肤",
                       "劳动节": "旅行护肤", "儿童节": "护肤", "国庆": "假期护肤",
                       "圣诞": "派对护肤", "跨年": "熬夜护肤"}
    
    for kw in keywords.get(season, keywords["spring"])[:2]:
        items = _fetch_ddg(kw, limit=8)
        results.extend([t for t in items if 20 < len(t) < 150])
    
    fallback = SKINCARE_TIPS.get(season, SKINCARE_TIPS["spring"])
    if _is_holiday():
        fallback += SKINCARE_TIPS.get("holiday", [])
    results.extend(random.sample(fallback, min(5, len(fallback))))
    unique = list(dict.fromkeys(results))
    return random.sample(unique, min(count, len(unique)))

def get_beauty_text():
    texts = fetch_beauty_texts(3)
    return texts[0] if texts else "早安，愿你今天心情美好。"

def get_skincare_tip():
    tips = fetch_skincare_tips(3)
    return tips[0] if tips else "今日建议：做好基础保湿，保持好心情。"

if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    print("=" * 50)
    print(f"当前季节: {_get_season()}")
    print("=" * 50)
    print("\n[美文抓取]")
    for t in fetch_beauty_texts(3):
        print(f"  > {t[:60]}...")
    print("\n[护肤贴士抓取]")
    for t in fetch_skincare_tips(3):
        print(f"  > {t[:60]}...")