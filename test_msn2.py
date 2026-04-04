import requests
import re
import json

# 仁寿
url_renshou = 'https://www.msn.cn/zh-cn/weather/forecast/in-%E5%9B%9B%E5%B7%9D%E7%9C%89%E5%B1%B1%E5%B8%82'
# 成都
url_chengdu = 'https://www.msn.cn/zh-cn/weather/forecast/in-%E6%88%90%E9%83%BD'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def parse_msn_weather(url, city_name):
    print(f'\n=== {city_name} ===')
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        text = resp.text

        # 查找 __INITIAL_STATE__ 或类似的数据
        state_match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', text, re.DOTALL)
        if state_match:
            print('找到 __INITIAL_STATE__')
            data = json.loads(state_match.group(1))
            print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
            return

        # 尝试查找 weatherData
        weather_match = re.search(r'"weatherData"\s*:\s*(\{[^}]+\})', text)
        if weather_match:
            print('找到 weatherData')
            print(weather_match.group(1)[:500])

        # 查找 script 标签中的 JSON
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', text, re.DOTALL)
        for script in scripts:
            if 'weather' in script.lower() and len(script) > 100:
                print(f'\n找到天气相关脚本 ({len(script)} chars):')
                # 提取关键数据
                temp_match = re.search(r'"temperature"\s*:\s*"?(\d+)"?', script)
                desc_match = re.search(r'"description"\s*:\s*"([^"]+)"', script)
                if temp_match:
                    print(f'温度: {temp_match.group(1)}°C')
                if desc_match:
                    print(f'描述: {desc_match.group(1)}')
                break

    except Exception as e:
        print(f'Error: {e}')

parse_msn_weather(url_renshou, '仁寿县')
parse_msn_weather(url_chengdu, '成都')
