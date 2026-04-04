import requests
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

api_key = '9aa7a6306d7bb369e673afc85ea67dfd'
cities = ['仁寿', '成都']

for city in cities:
    url = f'http://apis.juhe.cn/simpleWeather/query?city={city}&key={api_key}'
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        print(f'\n=== {city} ===')
        print(f'Status: {data.get("error_code")} - {data.get("reason")}')

        if data.get('result'):
            r = data['result']
            real = r.get('realtime', {})
            print(f'Temperature: {real.get("temperature")} C')
            print(f'Humidity: {real.get("humidity")}%')
            print(f'Weather: {real.get("info")}')
            print(f'Wind: {real.get("direct")} {real.get("power")}')
            print(f'AQI: {real.get("aqi")}')

            # Future forecast
            future = r.get('future', {})
            if future:
                print(f'\nFuture forecast:')
                for k, v in future.items():
                    if isinstance(v, dict):
                        print(f'  {v.get("date", k)}: {v.get("weather")} {v.get("temperature")}')
        else:
            print(f'Response: {json.dumps(data, ensure_ascii=False)[:500]}')

    except Exception as e:
        print(f'{city} Error: {e}')
