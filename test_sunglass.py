# -*- coding: utf-8 -*-
from data_fetcher import fetch_all_data

data = fetch_all_data()
for w in data['weather_list']:
    idx = w.get('indices', {})
    print(f"{w['city']}:")
    print(f"  Sunglass: {idx.get('12', {}).get('category', '-')}")
    print(f"  Sport: {idx.get('1', {}).get('category', '-')}")
    print(f"  CarWash: {idx.get('2', {}).get('category', '-')}")
