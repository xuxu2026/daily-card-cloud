import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# 尝试 MSN 天气 API
# 仁寿 经纬度
lat_renshou = "30.01818884765625"
lon_renshou = "104.158935546875"

# 成都
lat_chengdu = "30.5728"
lon_chengdu = "104.0668"

# 尝试 Bing 天气 API
api_urls = [
    # MSN Weather API
    f'https://www.msn.com/weather/forecast/renshou,china?ocid=winp2fptaskbarhover&heldtime=1&FORM=0009',
    f'https://www.msn.com/weather/forecast/chengdu,china?ocid=winp2fptaskbarhover&heldtime=1&FORM=0009',

    # Microsoft Weather (新版)
    f'https://api.msn.com/weather/zh-cn/renshou?apiKey=test&format=json',
]

for url in api_urls[:2]:
    print(f'\n=== Testing: {url[:60]}... ===')
    try:
        resp = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        print(f'Status: {resp.status_code}')
        print(f'Final URL: {resp.url[:80]}')
        print(f'Content-Type: {resp.headers.get("Content-Type", "N/A")}')

        if 'json' in resp.headers.get('Content-Type', ''):
            data = resp.json()
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
        else:
            # 尝试从 HTML 中提取数据
            import re
            temps = re.findall(r'(\d+)[°℃]', resp.text[:5000])
            print(f'温度: {temps[:5]}')
    except Exception as e:
        print(f'Error: {e}')

print('\n\n结论: MSN Weather 主要靠 JavaScript 动态加载，爬虫方案不稳定')
print('建议: 继续使用和风 API 或申请 OpenWeatherMap API Key')
