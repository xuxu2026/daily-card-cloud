# 小红书浏览器采集器
# 使用浏览器自动化访问小红书网页版

import subprocess
import time
import json
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BEAUTY_FILE = os.path.join(BASE_DIR, "web_beauty.txt")
SKINCARE_FILE = os.path.join(BASE_DIR, "web_skincare.txt")

SESSION = "xhs_crawl"


def run_cmd(cmd, timeout=60):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True,
            timeout=timeout, encoding='utf-8', errors='ignore'
        )
        return (result.stdout or '') + (result.stderr or '')
    except:
        return ""


def load_existing(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()


def is_chinese(text):
    if not text:
        return False
    chinese_count = len(re.findall(r'[\u4e00-\u9fff]', text))
    return chinese_count / len(text) > 0.5


def save_new(filepath, items):
    existing = load_existing(filepath)
    new_items = []
    for item in items:
        item = item.strip()
        if len(item) < 15 or len(item) > 200:
            continue
        if item in existing:
            continue
        if not is_chinese(item):
            continue
        item = re.sub(r'<[^>]+>|\[.*?\]|#\S+', '', item)
        item = item.strip()
        if len(item) >= 15:
            new_items.append(item)

    new_items = list(set(new_items))

    if new_items:
        with open(filepath, "a", encoding="utf-8") as f:
            for item in new_items:
                f.write(item + "\n")
        return len(new_items)
    return 0


def get_page_text(url, wait=5):
    """获取页面文本"""
    print(f"    Opening {url[:50]}...")
    run_cmd(f'uvx browser-use --session {SESSION} open "{url}"')
    time.sleep(wait)

    # 获取正文
    output = run_cmd(f'uvx browser-use --session {SESSION} eval "document.body.innerText"')
    return output


def extract_sentences(text):
    """提取有意义的句子"""
    if not text:
        return []

    sentences = []
    # 按标点分割
    parts = re.split(r'[。！？\n]', text)

    for part in parts:
        part = part.strip()
        # 过滤条件
        if len(part) < 15 or len(part) > 150:
            continue
        if not is_chinese(part):
            continue
        # 过滤无意义内容
        if re.match(r'^[\d\W_]+$', part):
            continue
        if part.count('，') + part.count('。') + part.count('、') < 2:
            continue
        sentences.append(part)

    return sentences


def main():
    print("=" * 50)
    print("Xiaohongshu Browser Crawler")
    print("=" * 50)

    beauty_results = []
    skincare_results = []

    # 小红书搜索页面
    keywords_beauty = ["美文", "文案", "语录", "金句", "治愈", "励志"]
    keywords_skincare = ["护肤", "保养", "护肤技巧", "皮肤管理"]

    print("\n[1] Searching beauty texts...")

    for kw in keywords_beauty:
        try:
            # 搜索URL
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={kw}&type=51"
            text = get_page_text(search_url, wait=5)
            sentences = extract_sentences(text)
            print(f"      -> {len(sentences)} sentences")
            beauty_results.extend(sentences)
            time.sleep(2)
        except Exception as e:
            print(f"      -> Error: {e}")

    print("\n[2] Searching skincare tips...")

    for kw in keywords_skincare:
        try:
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={kw}&type=51"
            text = get_page_text(search_url, wait=5)
            sentences = extract_sentences(text)
            print(f"      -> {len(sentences)} sentences")
            skincare_results.extend(sentences)
            time.sleep(2)
        except Exception as e:
            print(f"      -> Error: {e}")

    # 关闭浏览器
    run_cmd(f'uvx browser-use --session {SESSION} close')

    # 保存结果
    print("\n[3] Saving results...")

    new_beauty = save_new(BEAUTY_FILE, beauty_results)
    total_beauty = len(load_existing(BEAUTY_FILE))

    new_skincare = save_new(SKINCARE_FILE, skincare_results)
    total_skincare = len(load_existing(SKINCARE_FILE))

    print("\n" + "=" * 50)
    print("Crawling Complete!")
    print(f"  Beauty texts: +{new_beauty} (total: {total_beauty})")
    print(f"  Skincare tips: +{new_skincare} (total: {total_skincare})")
    print("=" * 50)

    if total_beauty > 0:
        print("\nSample beauty texts:")
        samples = list(load_existing(BEAUTY_FILE))[-5:]
        for s in samples:
            print(f"  - {s[:50]}...")


if __name__ == "__main__":
    main()
