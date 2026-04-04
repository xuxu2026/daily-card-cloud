"""
小红书登录模块
通过 Playwright 模拟登录获取 Cookie
"""
import json
import os
from pathlib import Path

def get_cookie_file():
    """获取 Cookie 文件路径"""
    return os.path.join(os.path.dirname(__file__), "xhs_cookies.json")

def save_cookies(context):
    """保存 Cookie 到文件"""
    cookies = context.cookies()
    cookie_file = get_cookie_file()
    with open(cookie_file, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"Cookie 已保存到: {cookie_file}")
    return cookie_file

def load_cookies():
    """从文件加载 Cookie"""
    cookie_file = get_cookie_file()
    if os.path.exists(cookie_file):
        with open(cookie_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def login_and_get_cookies():
    """
    启动浏览器，手动登录小红书，然后自动保存 Cookie
    """
    from playwright.sync_api import sync_playwright
    
    cookies_file = get_cookie_file()
    
    # 检查是否已有有效 Cookie
    existing = load_cookies()
    if existing:
        print(f"已存在 Cookie 文件: {cookies_file}")
        print("如需重新登录，请先删除该文件")
        return existing
    
    print("正在启动浏览器...")
    print("请在打开的浏览器中登录小红书...")
    print("登录成功后，Cookie 将自动保存\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=False)
        page = browser.new_page()
        
        # 打开小红书登录页
        page.goto("https://www.xiaohongshu.com")
        
        # 等待用户手动登录
        input("登录完成后，按 Enter 继续...")
        
        # 保存 Cookie
        cookies = page.context.cookies()
        with open(cookies_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Cookie 已保存到: {cookies_file}")
        browser.close()
        
    return cookies

if __name__ == "__main__":
    cookies = login_and_get_cookies()
    print(f"\n获取到 {len(cookies)} 个 Cookie")
