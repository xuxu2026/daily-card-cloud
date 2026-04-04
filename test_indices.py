"""测试更多和风天气API的生活指数"""
import requests
from config import QWEATHER_API_KEY, QWEATHER_API_HOST

params = {'location': '101270108', 'lang': 'zh', 'key': QWEATHER_API_KEY}
base = f'https://{QWEATHER_API_HOST}/v7'
indices_url = f'{base}/indices/1d'

# 测试更多类型
test_types = ['4', '5', '6', '7', '8', '9', '10', '11', '12', '15', '16', '17', '18', '19', '20']

for t in test_types:
    resp = requests.get(indices_url, params={**params, 'type': t}, timeout=10)
    data = resp.json()
    if data.get('code') == '200':
        daily = data.get('daily', [])
        if daily:
            idx = daily[0]
            text = idx.get('text', '')[:40]
            print(f"Type {t}: {idx.get('name')} = {idx.get('category')} ({text})")
    else:
        print(f"Type {t}: Error - {data.get('error', {}).get('detail', 'Unknown')}")
