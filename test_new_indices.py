# -*- coding: utf-8 -*-
"""测试社会化观测API和新增指数"""
from data_fetcher import fetch_all_data
import json

data = fetch_all_data()
print('=== Weather Data Test ===')
for w in data['weather_list']:
    city = w['city']
    now = w.get('now', {})
    today_f = w.get('today', {})
    wind_info = f"{now.get('windDir', '')}{now.get('windScale', '')}"
    print(f"\n【{city}】")
    print(f"  Weather: {now.get('text', '--')} -> {today_f.get('textDay', '--')} ({wind_info})")
    print(f"  Temp: {now.get('temp', '--')}C | Humidity: {now.get('humidity', '--')}%")
    
    # 和风指数
    indices = w.get('indices', {})
    print(f"  Indices:")
    print(f"    Sport: {indices.get('1', {}).get('category', '-')}")
    print(f"    CarWash: {indices.get('2', {}).get('category', '-')}")
    print(f"    Allergy: {indices.get('7', {}).get('category', '-')}")
    print(f"    Comfort: {indices.get('8', {}).get('category', '-')}")
    
    # 社会化观测
    social = w.get('social_obs', {})
    print(f"  Social Obs Status: {social.get('status', '-')}")
