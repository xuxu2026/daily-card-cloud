"""用 Playwright 抓取 MSN Weather 动态页面"""
import sys
import io
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from playwright.sync_api import sync_playwright


def fetch_msn_weather(url, city_name):
    """从 MSN Weather 抓取天气数据"""
    result = {'city': city_name, 'source': 'MSN'}

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel='msedge', headless=True)
            page = browser.new_page(viewport={'width': 1280, 'height': 900})

            page.goto(url, wait_until='load', timeout=15000)
            page.wait_for_timeout(3000)

            text = page.inner_text('body')
            browser.close()

        # 提取所有温度
        temps = re.findall(r'(\d+)[°℃]', text)
        temps = [int(t) for t in temps if 0 < int(t) < 50]  # 过滤合理范围

        # 提取天气描述
        weather_kws = ['晴朗', '晴间多云', '多云', '阴', '阵雨', '小雨', '中雨', '大雨', '雷阵雨', '小雪', '中雪', '大雪', '雾', '霾', '大风']
        found = [kw for kw in weather_kws if kw in text[:3000]]

        # 找今天温度（通常在页面上半部分）
        if len(temps) >= 4:
            # 第一个温度通常是当前，后面是预报
            result['temp_now'] = temps[0]
            result['temp_low'] = min(temps[:4])
            result['temp_high'] = max(temps[:4])
            result['temps_week'] = temps
        elif len(temps) >= 2:
            result['temp_low'] = min(temps)
            result['temp_high'] = max(temps)

        result['conditions'] = found

    except Exception as e:
        result['error'] = str(e)

    return result


if __name__ == '__main__':
    urls = [
        ('https://www.msn.cn/zh-cn/weather/forecast/in-%E5%9B%9B%E5%B7%9D%E7%9C%89%E5%B1%B1%E5%B8%82', '仁寿'),
        ('https://www.msn.cn/zh-cn/weather/forecast/in-%E6%88%90%E9%83%BD', '成都'),
    ]

    print('='*50)
    print('MSN Weather 数据抓取测试')
    print('='*50)

    for url, city in urls:
        data = fetch_msn_weather(url, city)
        print(f'\n>>> {city} <<<')
        print(f'  当前温度: {data.get("temp_now", "N/A")} C')
        print(f'  今日区间: {data.get("temp_low", "N/A")} ~ {data.get("temp_high", "N/A")} C')
        print(f'  天气状况: {", ".join(data.get("conditions", ["未知"]))}')
        print(f'  一周温度: {data.get("temps_week", [])}')
        if 'error' in data:
            print(f'  错误: {data["error"]}')

    print('\n' + '='*50)
    print('[OK] 测试完成！数据可用于天气获取。')
