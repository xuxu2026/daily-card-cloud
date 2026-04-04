"""测试天气描述格式修改"""
from card_generator import build_html
from data_fetcher import fetch_all_data
from styles_72 import get_style_for_date

# 测试数据
data = fetch_all_data()
style = get_style_for_date()
html = build_html(data, style)

# 保存到临时文件
with open('output/preview_test.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('HTML已生成到 output/preview_test.html')
print('天气数据:')
for w in data['weather_list']:
    now = w.get('now', {})
    today_f = w.get('today', {})
    wind = f"{now.get('windDir', '')}{now.get('windScale', '')}"
    print(f"  {w['city']}: {now.get('text', '--')} -> {today_f.get('textDay', '--')} ({wind})")
    print(f"    temp: {now.get('temp', '--')} | humidity: {now.get('humidity', '--')}%")
