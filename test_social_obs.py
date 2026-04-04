# -*- coding: utf-8 -*-
"""测试社会化观测API"""
import requests
from config import CAIYUN_TOKEN

# 仁寿的经纬度
lat = 29.995556
lon = 104.134167

url = "https://api.caiyunapp.com/v1/social_observation"
params = {
    "longitude": lon,
    "latitude": lat,
    "main_info": 0,
    "sub_info": "0,0",
    "user_id": "daily_card_bot",
    "token": CAIYUN_TOKEN,
}

print(f"Testing Caiyun Social Observation API...")
print(f"URL: {url}")
print(f"Params: {params}")

try:
    resp = requests.get(url, params=params, timeout=10)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
