import requests
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 聚合数据
juhe_key = '9aa7a6306d7bb369e673afc85ea67dfd'

# 和风API
he_host = 'n73aaqth6t.re.qweatherapi.com'
he_key = 'efb9550ae81043d1a073e20a03bde3f2'
he_location = '101270403'  # 仁寿

city = '仁寿'

print('='*60)
print('API 返回数据对比 - ' + city)
print('='*60)

# 1. 聚合数据
print('\n>>> 聚合数据 (simpleWeather) <<<')
url = f'http://apis.juhe.cn/simpleWeather/query?city={city}&key={juhe_key}'
resp = requests.get(url, timeout=10)
juhe_data = resp.json()

if juhe_data.get('result'):
    r = juhe_data['result']
    print(f'当前温度: {r["realtime"]["temperature"]} C')
    print(f'湿度: {r["realtime"]["humidity"]}%')
    print(f'天气: {r["realtime"]["info"]}')
    print(f'风向风力: {r["realtime"]["direct"]} {r["realtime"]["power"]}')
    print(f'AQI: {r["realtime"]["aqi"]}')
    print(f'今日预报: {r["future"][0]["weather"]} {r["future"][0]["temperature"]}')

# 2. 和风API - 实时天气
print('\n>>> 和风天气 (v7/weather/now) <<<')
url2 = f'https://{he_host}/v7/weather/now?location={he_location}&key={he_key}&lang=zh'
resp2 = requests.get(url2, timeout=10)
he_now = resp2.json()

if he_now.get('code') == '200':
    now = he_now['now']
    print(f'当前温度: {now["temp"]} C')
    print(f'湿度: {now["humidity"]}%')
    print(f'天气: {now["text"]}')
    print(f'风向风力: {now["windDir"]} {now["windScale"]}级')
    print(f'体感温度: {now["feelsLike"]} C')
    print(f'AQI(PC): {now.get("air", "N/A")}')

# 3. 和风API - 7天预报
print('\n>>> 和风天气 (v7/weather/7d - 7天预报) <<<')
url3 = f'https://{he_host}/v7/weather/7d?location={he_location}&key={he_key}&lang=zh'
resp3 = requests.get(url3, timeout=10)
he_7d = resp3.json()

if he_7d.get('code') == '200':
    daily = he_7d['daily']
    print(f'今日: {daily[0]["textDay"]} {daily[0]["tempMin"]}~{daily[0]["tempMax"]} C')
    print(f'明日: {daily[1]["textDay"]} {daily[1]["tempMin"]}~{daily[1]["tempMax"]} C')

# 4. 和风API - 生活指数
print('\n>>> 和风天气 (v7/indices/1d - 生活指数) <<<')
url4 = f'https://{he_host}/v7/indices/1d?location={he_location}&key={he_key}&lang=zh&type=1,2,3,5,8'
resp4 = requests.get(url4, timeout=10)
he_idx = resp4.json()

if he_idx.get('code') == '200':
    print('生活指数:')
    for item in he_idx['daily'][:5]:
        print(f'  {item["name"]}: {item["text"]}')

print('\n' + '='*60)
print('数据对比总结')
print('='*60)
