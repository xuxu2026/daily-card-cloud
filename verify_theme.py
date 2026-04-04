#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""验证主题轮换和美文库"""
import datetime
from styles_72 import get_style_for_date, is_holiday, REGULAR_STYLES, HOLIDAY_STYLES
from content_fetcher import BEAUTY_TEXTS, SKINCARE_TIPS, _is_holiday as content_is_holiday

print('=' * 60)
print('【1. 主题轮换验证】')
print('=' * 60)

today = datetime.date.today()
print(f'今天是: {today}')
print(f'是否节日: {is_holiday(today)}')

# 计算今天是第几天
day_of_year = (today - datetime.date(today.year, 1, 1)).days + 1
print(f'今天是今年的第 {day_of_year} 天')
print(f'常规主题数量: {len(REGULAR_STYLES)}')
print(f'节日主题数量: {len(HOLIDAY_STYLES)}')
print()

# 主题索引
idx = (day_of_year - 1) % len(REGULAR_STYLES)
print(f'当前主题索引: {idx} (S{idx+1:02d})')
current_style = get_style_for_date()
print(f'主题名称: {current_style.get("name", "N/A")}')
print(f'主题primary: {current_style.get("primary", "N/A")}')
print()

print('=' * 60)
print('【2. 未来30天主题预览】')
print('=' * 60)
for i in range(30):
    future_date = today + datetime.timedelta(days=i)
    style = get_style_for_date(future_date)
    is_h = is_holiday(future_date)
    day_of_y = (future_date - datetime.date(future_date.year, 1, 1)).days + 1
    idx_f = (day_of_y - 1) % len(REGULAR_STYLES)
    print(f'{future_date} 第{day_of_y}天 S{idx_f+1:02d} {"[节日]" if is_h else ""}')
print()

print('=' * 60)
print('【3. 美文库统计】')
print('=' * 60)
total_beauty = 0
for key, texts in BEAUTY_TEXTS.items():
    print(f'{key}: {len(texts)} 条')
    total_beauty += len(texts)
print(f'美文总计: {total_beauty} 条')
print()

print('=' * 60)
print('【4. 护肤贴士库统计】')
print('=' * 60)
total_skincare = 0
for key, tips in SKINCARE_TIPS.items():
    print(f'{key}: {len(tips)} 条')
    total_skincare += len(tips)
print(f'护肤贴士总计: {total_skincare} 条')
print()

print('=' * 60)
print('【5. 节日检测】')
print('=' * 60)
print(f'content_fetcher节日检测: {content_is_holiday()}')
print(f'styles_72节日检测: {is_holiday()}')
print()

print('[完成] 验证完毕！')
