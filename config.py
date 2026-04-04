# =============================================================
# 配置文件 - 支持本地和 GitHub Actions 环境变量
# =============================================================
import os
from datetime import datetime, timezone, timedelta

# ─────────────────────────────────────────────────────────────
# 统一北京时间工具（解决 GitHub Actions UTC vs 北京时间不一致问题）
# 整个项目所有日期计算都用这个，不直接用 datetime.date.today()
# ─────────────────────────────────────────────────────────────
BJ_TZ = timezone(timedelta(hours=8))

def bj_now():
    """返回北京时间 datetime（带时区）"""
    return datetime.now(timezone.utc).astimezone(BJ_TZ)

def bj_date():
    """返回北京时间的日期（date 对象）"""
    return bj_now().date()

def bj_year():
    return bj_now().year

def bj_month():
    return bj_now().month

def bj_day():
    return bj_now().day

# 企业微信机器人 Webhook URL
# 格式: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key
WECOM_WEBHOOK_URL = os.environ.get("WECOM_WEBHOOK_URL", "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=51614b3a-83bb-477c-b29a-bc82de067b89")

# 彩之颜天气 API（主数据源）
# 申请地址: https://www.caiyunapp.com/
CAIYUN_TOKEN = os.environ.get("CAIYUN_TOKEN", "MebS8wFl8kAfhA4h")

# 城市经纬度（彩之颜使用经纬度定位，和风天气使用location_id）
# 仁寿县: 29°59′44″N 104°08′03″E, 和风ID: 101271502
# 成都市: 104.080989 / 30.657689, 和风ID: 101270101
CITIES = [
    {"name": "仁寿", "lat": 29.995556, "lon": 104.134167, "location_id": "101271502"},
    {"name": "成都", "lat": 30.657689, "lon": 104.080989, "location_id": "101270101"},
]

# 和风天气 API Key（补充数据源：紫外线、穿衣建议）
# 申请地址: https://dev.qweather.com/
# 免费版每天1000次请求，完全够用
# 和风天气 API（私有化部署）
QWEATHER_API_HOST = os.environ.get("QWEATHER_API_HOST", "n73aaqth6t.re.qweatherapi.com")
QWEATHER_API_KEY = os.environ.get("QWEATHER_API_KEY", "efb9550ae81043d1a073e20a03bde3f2")

# 图片输出路径
OUTPUT_IMAGE_PATH = "C:/Users/30286/WorkBuddy/20260403180838/daily-card/output/daily_card.png"

# 小红书 Cookie（用于抓取内容）
XHS_COOKIE = os.environ.get("XHS_COOKIE", "")
