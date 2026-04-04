# -*- coding: utf-8 -*-
"""查询和风天气城市ID"""
import requests
from config import QWEATHER_API_KEY, QWEATHER_API_HOST

# 和风天气城市查询API
base_url = f"https://{QWEATHER_API_HOST}/geo/v2"

# 查询仁寿
params_renshou = {"location": "仁寿", "key": QWEATHER_API_KEY, "lang": "zh"}
print(f"查询仁寿...")
resp = requests.get(f"{base_url}/city/lookup", params=params_renshou, timeout=10)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text[:1000]}")

# 查询成都
params_chengdu = {"location": "成都", "key": QWEATHER_API_KEY, "lang": "zh"}
print(f"\n查询成都...")
resp = requests.get(f"{base_url}/city/lookup", params=params_chengdu, timeout=10)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text[:1000]}")
