"""
数据获取模块
- 和风天气 API 获取天气、紫外线数据
- 成都机动车限号规则计算
- 护肤/化妆贴士（多源抓取）
- 诗意美文（多源抓取）
"""

import requests
import datetime
import random
from config import CAIYUN_TOKEN, QWEATHER_API_KEY, QWEATHER_API_HOST, CITIES, bj_date

# 聚合数据API配置（备用）
JUHE_API_KEY = "9aa7a6306d7bb369e673afc85ea67dfd"

# 天气现象映射（彩之颜 -> 中文）
SKYCON_MAP = {
    "CLEAR_NIGHT": "晴（夜）",
    "CLEAR_DAY": "晴",
    "PARTLY_CLOUDY_DAY": "多云",
    "PARTLY_CLOUDY_NIGHT": "多云（夜）",
    "CLOUDY": "阴",
    "FOG": "雾",
    "HAZE": "霾",
    "LIGHT_RAIN": "小雨",
    "MODERATE_RAIN": "中雨",
    "HEAVY_RAIN": "大雨",
    "STORM_RAIN": "暴雨",
    "THUNDER_SHOWER": "雷阵雨",
    "LIGHT_SNOW": "小雪",
    "MODERATE_SNOW": "中雪",
    "HEAVY_SNOW": "大雪",
    "SNOW": "雪",
    "DRIZZLE": "毛毛雨",
    "SLEET": "雨夹雪",
    "WIND": "大风",
    "UNKNOWN": "未知",
}

# 导入内容抓取模块（优先全网搜索，备用本地）
# 注意：需要 beautifulsoup4 + lxml，缺一不可，导入失败则降级本地库
try:
    from web_content_fetcher import get_beauty_text as net_get_beauty, get_skincare_tip as net_get_skincare, fetch_beauty_texts
    HAS_CONTENT_FETCHER = True
except ImportError:
    HAS_CONTENT_FETCHER = False


# ─────────────────────────────────────────────
# 1. 天气数据（彩之颜为主 + 和风天气补充）
# ─────────────────────────────────────────────

def get_weather_caiyun(lat: float, lon: float) -> dict:
    """使用彩之颜API获取天气信息（主数据源）"""
    url = f"https://api.caiyunapp.com/v2.6/{CAIYUN_TOKEN}/{lon},{lat}/weather"
    params = {"dailysteps": 3}  # 获取3天预报
    result = {
        "temp": "--",
        "text": "--",
        "humidity": "--",
        "windDir": "--",
        "windScale": "--",
        "aqi": "--",
        "aqi_level": "--",
        "uv": "",
        "dress": "",
        "daily": {},
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        if data.get("status") == "ok" and data.get("result"):
            r = data["result"]
            
            # 实况天气
            realtime = r.get("realtime", {})
            result["temp"] = str(int(realtime.get("temperature", 0)))
            skycon = realtime.get("skycon", "UNKNOWN")
            result["text"] = SKYCON_MAP.get(skycon, skycon)
            result["humidity"] = str(int(float(realtime.get("humidity", 0)) * 100))
            
            # 风力风向
            wind = realtime.get("wind", {})
            wind_speed = wind.get("speed", 0)
            wind_dir = wind.get("direction", 0)
            # 风向角度转文字
            dirs = ["北", "东北", "东", "东南", "南", "西南", "西", "西北"]
            dir_idx = int((wind_dir + 22.5) / 45) % 8
            result["windDir"] = dirs[dir_idx]
            result["windScale"] = wind_speed_to_scale(wind_speed)
            
            # 空气质量（彩之颜直接提供AQI）
            air = realtime.get("air_quality", {})
            aqi_data = air.get("aqi", {})
            if isinstance(aqi_data, dict):
                aqi_val = aqi_data.get("chn", 0)
            else:
                aqi_val = int(aqi_data) if aqi_data else 0
            if aqi_val > 0:
                result["aqi"] = str(aqi_val)
                result["aqi_level"] = get_aqi_level(aqi_val)
            
            # 每日预报（今天和明天）
            daily = r.get("daily", {})
            result["daily"] = daily
            
            # 彩之颜生活指数（紫外线、穿衣）
            life_index = daily.get("life_index", {})
            uv_data = life_index.get("ultraviolet", [{}])[0]
            dress_data = life_index.get("dressing", [{}])[0]
            uv_desc = uv_data.get("desc", "")
            uv_text = uv_data.get("text", "")
            result["uv"] = f"{uv_desc}（{uv_text}）" if uv_text else uv_desc
            result["dress"] = dress_data.get("desc", "")
            
    except Exception as e:
        result["error"] = str(e)
    return result


def wind_speed_to_scale(speed: float) -> str:
    """将风速(m/s)转换为风力等级描述"""
    if speed < 1:
        return "微风"
    elif speed < 6:
        return "1-2级"
    elif speed < 12:
        return "3-4级"
    elif speed < 20:
        return "4-5级"
    elif speed < 29:
        return "5-6级"
    elif speed < 40:
        return "6-7级"
    else:
        return "7级以上"


def get_aqi_level(aqi: int) -> str:
    """将AQI数值转换为等级描述"""
    if aqi <= 50:
        return "优"
    elif aqi <= 100:
        return "良"
    elif aqi <= 150:
        return "轻度"
    elif aqi <= 200:
        return "中度"
    elif aqi <= 300:
        return "重度"
    else:
        return "严重"


def get_weather_hefeng_supplement(location_id: str) -> dict:
    """使用和风天气API获取补充数据（紫外线 + 穿衣建议 + 更多生活指数）"""
    base = f"https://{QWEATHER_API_HOST}/v7"
    params = {"location": location_id, "lang": "zh", "key": QWEATHER_API_KEY}
    result = {"uv": "", "dress": "", "dressIndex": "", "indices": {}}
    try:
        # 生活指数
        # 1=运动, 2=洗车, 3=穿衣, 5=紫外线, 7=过敏, 12=太阳镜
        indices_url = f"{base}/indices/1d"
        indices_resp = requests.get(indices_url, params={**params, "type": "1,2,3,5,7,12"}, timeout=15).json()
        if indices_resp.get("code") == "200":
            for idx in indices_resp.get("daily", []):
                idx_type = idx.get("type")
                name = idx.get("name", "")
                category = idx.get("category", "")
                text = idx.get("text", "")[:40]
                result["indices"][idx_type] = {"name": name, "category": category, "text": text}
                
                if idx_type == "5":
                    result["uv"] = f"{category}（{text}）"
                elif idx_type == "3":
                    result["dress"] = idx["text"][:40]
                    result["dressIndex"] = str(idx.get("level", ""))
    except Exception:
        pass
    return result


def get_social_observation(lat: float, lon: float) -> dict:
    """使用彩之颜社会化观测API获取观测数据"""
    url = "https://api.caiyunapp.com/v1/social_observation"
    params = {
        "longitude": lon,
        "latitude": lat,
        "main_info": 0,
        "sub_info": "0,0",
        "user_id": "daily_card_bot",
        "token": CAIYUN_TOKEN,
    }
    result = {"status": "unavailable"}
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get("status") == "ok" and data.get("result"):
            result = data.get("result", {})
            result["status"] = "ok"
    except Exception as e:
        result["error"] = str(e)
    return result


def get_weather(lat: float, lon: float, location_id: str = "") -> dict:
    """
    获取单个城市的天气信息（彩之颜为主 + 和风天气补充）
    - 彩之颜提供：温度、湿度、天气、风向风力、AQI、今明预报、紫外线、穿衣建议
    - 和风天气补充：运动、洗车、过敏、太阳镜等生活指数
    """
    # 彩之颜（主数据源）
    caiyun_data = get_weather_caiyun(lat, lon)

    # 构建结果
    result = {
        "now": {
            "temp": caiyun_data.get("temp", "--"),
            "text": caiyun_data.get("text", "--"),
            "humidity": caiyun_data.get("humidity", "--"),
            "windDir": caiyun_data.get("windDir", "--"),
            "windScale": caiyun_data.get("windScale", "--"),
        },
        "today": {},
        "tomorrow": {},
        "uv": caiyun_data.get("uv", ""),
        "dress": caiyun_data.get("dress", ""),
        "air": caiyun_data.get("aqi", "--"),
        "air_level": caiyun_data.get("aqi_level", "--"),
        "daily": caiyun_data.get("daily", {}),
        "indices": {},  # 和风天气生活指数
        "social_obs": {},  # 彩之颜社会化观测
    }

    # 从彩之颜daily中提取今明两天
    daily = caiyun_data.get("daily", {})
    temperature = daily.get("temperature", [])
    skycon = daily.get("skycon", [])
    
    if temperature and len(temperature) >= 1:
        t = temperature[0]
        result["today"] = {
            "tempMax": str(int(t.get("max", 0))),
            "tempMin": str(int(t.get("min", 0))),
            "textDay": SKYCON_MAP.get(skycon[0].get("value", "UNKNOWN") if skycon else "UNKNOWN", "--"),
        }
    
    if temperature and len(temperature) >= 2:
        t = temperature[1]
        result["tomorrow"] = {
            "tempMax": str(int(t.get("max", 0))),
            "tempMin": str(int(t.get("min", 0))),
            "textDay": SKYCON_MAP.get(skycon[1].get("value", "UNKNOWN") if len(skycon) > 1 else "UNKNOWN", "--"),
        }

    # 和风天气补充（生活指数）
    if location_id:
        hefeng = get_weather_hefeng_supplement(location_id)
        result["indices"] = hefeng.get("indices", {})
        if not result["uv"] and hefeng.get("uv"):
            result["uv"] = hefeng["uv"]
        if not result["dress"] and hefeng.get("dress"):
            result["dress"] = hefeng["dress"]

    # 彩之颜社会化观测
    result["social_obs"] = get_social_observation(lat, lon)

    return result


def get_all_weather() -> list:
    """获取所有城市天气（彩之颜为主 + 和风补充）"""
    results = []
    for city in CITIES:
        try:
            lat = city.get("lat")
            lon = city.get("lon")
            location_id = city.get("location_id", "")  # 和风天气用的旧字段，兼容
            w = get_weather(lat, lon, location_id)
            w["city"] = city["name"]
            results.append(w)
        except Exception as e:
            results.append({
                "city": city["name"],
                "error": str(e),
                "now": {"temp": "--", "text": "获取失败"},
                "today": {"tempMax": "--", "tempMin": "--", "textDay": "--"},
                "uv": "--",
                "dress": "--",
            })
    return results


# ─────────────────────────────────────────────
# 2. 成都机动车限号
# ─────────────────────────────────────────────

def get_chengdu_restriction() -> dict:
    """
    成都限号规则（早7:30-9:00，晚17:00-19:00，周一到周五）
    尾号轮换规则（每月第一个工作日起）：
      周一: 1、6
      周二: 2、7
      周三: 3、8
      周四: 4、9
      周五: 5、0
    说明：成都限号每月轮换，但官方规则需以实际公告为准。
    此处采用固定星期对应规则（适合大多数月份）。
    """
    WEEKDAY_NUMBERS = {
        0: ("1、6", "Monday"),
        1: ("2、7", "Tuesday"),
        2: ("3、8", "Wednesday"),
        3: ("4、9", "Thursday"),
        4: ("5、0", "Friday"),
    }

    today = bj_date()
    tomorrow = today + datetime.timedelta(days=1)

    def get_restriction_for_day(d: datetime.date) -> str:
        wd = d.weekday()  # 0=周一 ... 6=周日
        if wd >= 5:  # 周末不限
            return "不限行"
        numbers, _ = WEEKDAY_NUMBERS[wd]
        return f"尾号 {numbers} 限行"

    today_str = get_restriction_for_day(today)
    tomorrow_str = get_restriction_for_day(tomorrow)

    return {
        "today_date": f"{today.month:02d}月{today.day:02d}日",
        "today_week": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][today.weekday()],
        "today_restriction": today_str,
        "tomorrow_date": f"{tomorrow.month:02d}月{tomorrow.day:02d}日",
        "tomorrow_week": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][tomorrow.weekday()],
        "tomorrow_restriction": tomorrow_str,
    }


# ─────────────────────────────────────────────
# 3. 护肤/化妆贴士（按季节）
# ─────────────────────────────────────────────

SKINCARE_TIPS = {
    "spring": [  # 3-5月
        "春季皮肤敏感期，换季时请先做局部测试再更换新护肤品。",
        "春季花粉飘散，外出回来后用温和洁面乳彻底清洁，避免过敏反应。",
        "春天紫外线逐渐增强，防晒乳建议从SPF30升级至SPF50+。",
        "春季保湿不可忽视，补水精华+锁水面霜是最佳搭档。",
        "春季底妆建议选择轻薄气垫，既保湿又能防止闷痘。",
        "化妆前先做5分钟保湿面膜，妆效更服帖、持久。",
        "唇部春季易干裂，睡前涂厚厚一层凡士林，早起唇部水润满分。",
    ],
    "summer": [  # 6-8月
        "高温出汗多，防晒记得2小时补涂一次，特别是额头和鼻翼。",
        "夏季控油：早晚用清爽型洗面奶，T区用吸油纸轻压，不要反复擦拭。",
        "防晒是最平价的抗衰手段，比任何贵妇护肤品都管用！",
        "夏季底妆用定妆喷雾代替散粉，保湿同时控制浮粉。",
        "西瓜汁冷藏后用化妆棉湿敷5分钟，天然镇静+补水效果极好。",
        "夏天卸妆要格外彻底，防晒残留是毛孔堵塞的主要原因之一。",
    ],
    "autumn": [  # 9-11月
        "秋季换季时角质层变薄，暂停去角质与刷酸，以修护屏障为主。",
        "秋燥当道，增加玻尿酸、神经酰胺类成分，皮肤屏障更强韧。",
        "秋季是使用维A醇的好时机，夜间少量涂抹，告别细纹与暗沉。",
        "眼部保湿不可少，细纹从缺水开始，眼霜要轻轻叩击，不要拉扯。",
        "口红选色：秋季大地色系最显气质，豆沙色、焦糖色百搭又高级。",
        "秋季嘴唇易起皮，用湿润的棉签轻轻打圈去角质，再涂唇膜。",
    ],
    "winter": [  # 12-2月
        "冬季洗脸水温38℃最佳，过热会破坏皮肤天然油脂保护膜。",
        "冬天护肤顺序：爽肤水→精华→面霜，层层锁水，不留死角。",
        "空调房里放一盆水或加湿器，皮肤水分蒸发速度可降低30%。",
        "冬季面霜可以加一滴玫瑰果油混合使用，保湿力翻倍，皮肤亮泽。",
        "冬天口红显色好，哑光色系最耐看，但记得唇部打底防止卡纹。",
        "颈部、手部也需要防晒！这两个部位最容易暴露真实年龄。",
    ],
}

POETIC_SENTENCES = [
    ("春水初生，春林初盛，春风十里，不如你。", "冯唐"),
    ("人间四月天，最美是烟雨，最暖是晴日，最好是你出现的样子。", ""),
    ("愿你所有的清晨都明亮，所有的傍晚都温柔。", ""),
    ("山有木兮木有枝，心悦君兮君不知。", "《越人歌》"),
    ("若有诗书藏在心，岁月从不败美人。", ""),
    ("时光不语，却温柔回答了所有问题。", ""),
    ("你喜欢春天，我便在你的四月等候。", ""),
    ("日暮苍山远，天寒白屋贫。柴门闻犬吠，风雪夜归人。", "刘长卿"),
    ("世界辽阔，生活温柔，总有人在路口等你。", ""),
    ("一花一叶，皆是风景；一朝一暮，皆是良辰。", ""),
    ("愿你三冬暖，愿你春不寒，愿你天黑有灯下雨有伞。", ""),
    ("没有一个春天不会到来，没有一个早晨不会开始。", ""),
    ("微风吹梦，星光落肩，今天也是被偏爱的一天。", ""),
    ("最美的风景，不在远方，而在你抬眼的瞬间。", ""),
    ("岁月不是铁锹，把你铲走；岁月是一把梳子，把你梳得越来越好看。", ""),
    ("人间值得，余生漫长，请你慢慢来。", ""),
    ("春风得意马蹄疾，一日看尽长安花。", "孟郊"),
    ("江南无所有，聊赠一枝春。", "陆凯"),
    ("人生若只如初见，何事秋风悲画扇。", "纳兰性德"),
    ("莫道桑榆晚，为霞尚满天。", "刘禹锡"),
]


def get_skincare_tip() -> str:
    """
    获取护肤贴士（优先全网搜索，备用本地库）
    保证永远返回非空内容
    """
    DEFAULT_TIP = "今日建议：做好基础保湿，保持好心情，早睡早起皮肤好。"

    if HAS_CONTENT_FETCHER:
        try:
            tip = net_get_skincare()
            if tip and tip.strip():
                return tip
        except Exception:
            pass  # 降级本地库

    # 备用：本地季节库
    month = bj_date().month
    if 3 <= month <= 5:
        season = "spring"
    elif 6 <= month <= 8:
        season = "summer"
    elif 9 <= month <= 11:
        season = "autumn"
    else:
        season = "winter"
    tips = SKINCARE_TIPS.get(season, SKINCARE_TIPS["spring"])
    return random.choice(tips) if tips else DEFAULT_TIP


def get_poetic_sentences() -> tuple:
    """
    获取美文（优先全网搜索，备用本地库）
    确保 poem1 和 poem2 不重复
    """
    if HAS_CONTENT_FETCHER:
        try:
            p1 = net_get_beauty()
            # 获取多条，确保 p2 与 p1 不同
            texts = fetch_beauty_texts(5)
            p2 = None
            for t in texts:
                if t != p1:
                    p2 = t
                    break
            # 如果网上只抓到1条或全部相同，从本地备用库补一条
            if p2 is None or p2 == p1:
                local_poems = [t for t, _ in POETIC_SENTENCES if t != p1]
                if local_poems:
                    p2 = random.choice(local_poems)
                else:
                    p2 = p1
            return p1, p2
        except Exception:
            pass  # 降级本地库

    # 备用：本地库（保证两条不重复）
    chosen = random.sample(POETIC_SENTENCES, 2)
    result = []
    for text, author in chosen:
        if author:
            result.append(f"{text} —— {author}")
        else:
            result.append(text)
    return result[0], result[1]


# ─────────────────────────────────────────────
# 4. 汇总所有数据
# ─────────────────────────────────────────────

def fetch_all_data() -> dict:
    """汇总所有数据，供图片生成使用"""
    today = bj_date()
    weather_list = get_all_weather()
    restriction = get_chengdu_restriction()
    skincare = get_skincare_tip()
    poem1, poem2 = get_poetic_sentences()

    return {
        "date": f"{today.year}年{today.month:02d}月{today.day:02d}日",
        "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][today.weekday()],
        "weather_list": weather_list,
        "restriction": restriction,
        "skincare_tip": skincare,
        "poem1": poem1,
        "poem2": poem2,
    }


if __name__ == "__main__":
    import json
    data = fetch_all_data()
    print(json.dumps(data, ensure_ascii=False, indent=2))
