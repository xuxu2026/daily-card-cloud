"""
小红书 Cookie 获取工具
运行此脚本后，在浏览器中登录小红书
登录成功后按回车，Cookie 会自动保存到 config.py
"""

import time
import sys
import json

try:
    from playwright.sync_api import sync_playwright as p
except ImportError:
    print("正在安装 playwright...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "-q"])
    from playwright.sync_api import sync_playwright as p

def get_xhs_cookie():
    print("=" * 50)
    print("小红书 Cookie 获取工具")
    print("=" * 50)
    print()
    print("即将打开浏览器，请：")
    print("1. 手动登录你的小红书账号")
    print("2. 登录成功后回到这个窗口")
    print("3. 按回车键继续")
    print()
    input("按回车键打开浏览器...")

    with p.launch(channel='msedge', headless=False, slow_mo=100) as browser:
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        )
        page = context.new_page()

        # 访问小红书
        print("正在打开小红书...")
        page.goto('https://www.xiaohongshu.com', timeout=30000)
        page.wait_for_load_state('domcontentloaded')

        print()
        print("✅ 浏览器已打开")
        print("请在浏览器中完成登录...")
        print()

        # 等待用户按回车
        input("登录成功后，按回车键继续...")

        # 获取 Cookie
        cookies = context.cookies()
        xhs_cookie = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

        print()
        print("=" * 50)
        print("获取到 Cookie！")
        print("=" * 50)
        print()
        print(f"Cookie 长度: {len(xhs_cookie)} 字符")
        print()

        # 显示部分 Cookie（验证用）
        if xhs_cookie:
            print("Cookie 预览（前200字符）:")
            print(xhs_cookie[:200] + "...")
            print()

        # 保存到文件
        with open('xhs_cookie_temp.txt', 'w', encoding='utf-8') as f:
            f.write(xhs_cookie)

        print(f"✅ Cookie 已保存到 xhs_cookie_temp.txt")
        print()
        print("请把 xhs_cookie_temp.txt 文件的内容发给我，我来帮你配置！")

        browser.close()

if __name__ == "__main__":
    try:
        get_xhs_cookie()
    except Exception as e:
        print(f"出错了: {e}")
        input("\n按回车退出...")
