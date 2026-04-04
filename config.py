# =============================================================
# 配置文件 - 请在此填入您的实际配置
# =============================================================

# 企业微信机器人 Webhook URL
# 格式: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key
WECOM_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=51614b3a-83bb-477c-b29a-bc82de067b89"

# 彩之颜天气 API（主数据源）
# 申请地址: https://www.caiyunapp.com/
CAIYUN_TOKEN = "MebS8wFl8kAfhA4h"

# 城市经纬度（彩之颜使用经纬度定位，和风天气使用location_id）
# 仁寿县: 29°59′44″N 104°08′03″E, 和风ID: 101271502
# 成都市: 30°39′36″N 104°03′48″E, 和风ID: 101270101
CITIES = [
    {"name": "仁寿", "lat": 29.995556, "lon": 104.134167, "location_id": "101271502"},
    {"name": "成都", "lat": 30.66, "lon": 104.063333, "location_id": "101270101"},
]

# 和风天气 API Key（补充数据源：紫外线、穿衣建议）
# 申请地址: https://dev.qweather.com/
# 免费版每天1000次请求，完全够用
# 和风天气 API（私有化部署）
QWEATHER_API_HOST = "n73aaqth6t.re.qweatherapi.com"
QWEATHER_API_KEY = "efb9550ae81043d1a073e20a03bde3f2"

# 图片输出路径
OUTPUT_IMAGE_PATH = "C:/Users/30286/WorkBuddy/20260403180838/daily-card/output/daily_card.png"

# 小红书 Cookie（用于抓取内容）
XHS_COOKIE = "abRequestId=b39c4886-7ec1-5de8-9022-366bd9ea71f9; ets=1775224658142; webBuild=6.3.0; xsecappid=xhs-pc-web; loadts=1775224658285; a1=19d53a29978u4pxiep24gzdpr9md8pf9qiidughsr50000339811; webId=6e0d9dc55885a0e61985bed24507fb34; websectiga=59d3ef1e60c4aa37a7df3c23467bd46d7f1da0b1918cf335ee7f2e9e52ac04cf; sec_poison_id=d2085868-2e24-471c-9e2b-95b22596d46d; gid=yjf2q0J0KDA2yjf2q0Jjj3kxWY74UC3dUJ4k3MFufUFj6f28fYUij7888qqjYyy84yJ4DJ8K; unread={%22ub%22:%2269c50b5e0000000023022816%22%2C%22ue%22:%2269cd2fcd00000000220038c8%22%2C%22uc%22:29}"
