#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""高强度稳定性测试脚本"""
from data_fetcher import get_poetic_sentences, get_skincare_tip, get_all_weather, get_chengdu_restriction

def run_tests():
    print('=' * 60)
    print('【测试1】美文抓取')
    print('=' * 60)
    p1, p2 = get_poetic_sentences()
    print(f'poem1: {p1}')
    print(f'poem2: {p2}')
    print(f'是否相同: {p1 == p2}')
    print(f'poem1长度: {len(p1)} 字符')
    print(f'poem2长度: {len(p2)} 字符')
    # 判断显示逻辑
    if len(p1) >= 22:
        print(f'[预期] 长美文，显示1条')
    else:
        print(f'[预期] 短美文，显示2条')
    print()

    print('=' * 60)
    print('【测试2】护肤贴士')
    print('=' * 60)
    tip = get_skincare_tip()
    print(f'贴士: {tip}')
    print()

    print('=' * 60)
    print('【测试3】天气API')
    print('=' * 60)
    weather_list = get_all_weather()
    for w in weather_list:
        city = w.get('city', '')
        now = w.get('now', {})
        today = w.get('today', {})
        tomorrow = w.get('tomorrow', {})
        uv = w.get('uv', '')
        dress = w.get('dress', '')
        air = w.get('air', '')
        indices = w.get('indices', {})

        print(f'城市: {city}')
        print(f'  当前天气: {now.get("temp")}° {now.get("text")}')
        print(f'  今日预报: {today.get("textDay")} {today.get("tempMin")}-{today.get("tempMax")}°')
        print(f'  明日预报: {tomorrow.get("textDay")} {tomorrow.get("tempMin")}-{tomorrow.get("tempMax")}°')
        print()

        # 简化显示的文字
        if uv:
            uv_text = uv.split('（')[0] if '（' in uv else uv
            print(f'  [前端显示] 紫外线 {uv_text}')
        else:
            print(f'  [前端显示] 紫外线 --')

        if dress:
            if '长袖' in dress:
                dress_text = '穿衣 长袖'
            elif '外套' in dress:
                dress_text = '穿衣 外套'
            elif '短袖' in dress:
                dress_text = '穿衣 短袖'
            elif 'T恤' in dress:
                dress_text = '穿衣 T恤'
            else:
                dress_text = f'穿衣 {dress[:6]}'
            print(f'  [前端显示] {dress_text}')
        else:
            print(f'  [前端显示] 穿衣 --')

        # 空气指数
        if isinstance(air, str):
            try:
                aqi_val = int(air)
                if aqi_val <= 50:
                    aqi_text = f'空气 {air} 优'
                elif aqi_val <= 100:
                    aqi_text = f'空气 {air} 良'
                elif aqi_val <= 150:
                    aqi_text = f'空气 {air} 轻度污染'
                else:
                    aqi_text = f'空气 {air} 中度污染'
            except:
                aqi_text = f'空气 {air}'
        else:
            aqi_text = '空气 --'
        print(f'  [前端显示] {aqi_text}')
        print()

        # 生活指数
        print(f'  [生活指数]')
        print(f'    运动: {indices.get("1", {}).get("category", "")}')
        print(f'    洗车: {indices.get("2", {}).get("category", "")}')
        print(f'    太阳镜: {indices.get("12", {}).get("category", "")}')
        print(f'    过敏: {indices.get("7", {}).get("category", "")}')
        print(f'    舒适度: {indices.get("8", {}).get("category", "")}')
        print()

    print('=' * 60)
    print('【测试4】限号信息')
    print('=' * 60)
    restriction = get_chengdu_restriction()
    print(f'今日限号: {restriction.get("today_restriction", "")}')
    print(f'明日限号: {restriction.get("tomorrow_restriction", "")}')
    print()

    print('=' * 60)
    print('【测试5】后端数据检查')
    print('=' * 60)
    # 汇总数据
    data = {
        'date': '测试日期',
        'weekday': '测试',
        'weather_list': weather_list,
        'restriction': restriction,
        'skincare_tip': tip,
        'poem1': p1,
        'poem2': p2
    }

    # 检查数据完整性
    issues = []
    for w in data['weather_list']:
        if not w.get('now', {}).get('temp'):
            issues.append(f"{w.get('city')} 缺少温度数据")
        if not w.get('today', {}).get('textDay'):
            issues.append(f"{w.get('city')} 缺少今日预报")
        if not w.get('uv'):
            issues.append(f"{w.get('city')} 缺少紫外线数据")
        if not w.get('dress'):
            issues.append(f"{w.get('city')} 缺少穿衣数据")
        if not w.get('air'):
            issues.append(f"{w.get('city')} 缺少空气数据")

    if issues:
        print('[警告] 发现数据问题:')
        for issue in issues:
            print(f'  - {issue}')
    else:
        print('[通过] 所有后端数据完整')
    print()

    print('=' * 60)
    print('【测试6】连续运行3次，检查稳定性')
    print('=' * 60)
    for i in range(3):
        p1, p2 = get_poetic_sentences()
        print(f'第{i+1}次: poem1={p1[:30]}...')
    print()

    print('=' * 60)
    print('[测试完成]')
    print('=' * 60)

if __name__ == '__main__':
    run_tests()
