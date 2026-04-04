import requests
import re

url = 'https://www.msn.cn/zh-cn/weather/forecast/in-%E5%9B%9B%E5%B7%9D%E7%9C%89%E5%B1%B1%E5%B8%82'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    resp = requests.get(url, headers=headers, timeout=15)
    print(f'Status: {resp.status_code}')
    print(f'Length: {len(resp.text)} chars')

    text = resp.text

    # 查找温度模式
    temps = re.findall(r'(\d+)[°℃]', text)
    print(f'找到温度: {temps[:10]}')

    # 查找中文天气描述
    weather_keywords = ['多云', '晴', '阴', '雨', '雪', '雾', '霾', '风', '晴朗']
    found = [kw for kw in weather_keywords if kw in text]
    print(f'天气关键词: {found}')

    # 尝试找 JSON 数据
    json_pattern = r'weatherData["\s:]+({[^}]+})'
    matches = re.findall(json_pattern[:30], text)
    if matches:
        print(f'找到JSON片段: {matches[:3]}')

except Exception as e:
    print(f'Error: {e}')
