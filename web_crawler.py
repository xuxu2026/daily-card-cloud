# 全网内容采集器 v4.0
# 使用一言API + 今日诗词API

import requests
import time
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BEAUTY_FILE = os.path.join(BASE_DIR, "web_beauty.txt")
SKINCARE_FILE = os.path.join(BASE_DIR, "web_skincare.txt")


def load_existing(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()


def is_chinese(text):
    if not text:
        return False
    chinese_count = len(re.findall(r'[\u4e00-\u9fff]', text))
    return chinese_count / len(text) > 0.6


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
        # 过滤日文
        japanese_count = len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF]', item))
        if japanese_count > 3:
            continue
        new_items.append(item)

    new_items = list(set(new_items))

    if new_items:
        with open(filepath, "a", encoding="utf-8") as f:
            for item in new_items:
                f.write(item + "\n")
        return len(new_items)
    return 0


def fetch_hitokoto(categories, count=30):
    texts = []
    cat_names = {
        'd': '文学', 'e': '原创', 'i': '诗词',
        'f': '网络', 'g': '其他', 'h': '影视', 'k': '哲学'
    }

    for cat in categories:
        print(f"    Fetching {cat_names.get(cat, cat)}...")
        success = 0
        for _ in range(count):
            try:
                resp = requests.get(
                    f"https://v1.hitokoto.cn/?c={cat}&encode=json",
                    timeout=5
                )
                if resp.status_code == 200:
                    data = resp.json()
                    text = data.get("hitokoto", "")
                    if len(text) >= 15 and is_chinese(text):
                        texts.append(text)
                        success += 1
                time.sleep(0.15)
            except:
                pass
        print(f"      -> {success} texts")

    return texts


def fetch_jinrishici():
    texts = []
    print("    Fetching 今日诗词...")
    for _ in range(20):
        try:
            resp = requests.get("https://v1.jinrishici.com/sentence", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                content = data.get("data", {}).get("content", "")
                if len(content) >= 8 and is_chinese(content):
                    texts.append(content)
            time.sleep(0.2)
        except:
            pass
    print(f"      -> {len(texts)} texts")
    return texts


def fetch_skincare_tips():
    tips = []
    print("    Fetching skincare tips...")

    # 使用简书公开API
    keywords = ["护肤", "保湿", "防晒", "清洁", "抗衰", "美白"]
    for kw in keywords:
        try:
            resp = requests.get(
                f"https://www.jianshu.com/search?q={kw}&page=1",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=5
            )
            if resp.status_code == 200:
                matches = re.findall(r'[^。！？]{20,100}[。！？]', resp.text)
                for m in matches:
                    m = m.strip()
                    if len(m) >= 20 and is_chinese(m):
                        tips.append(m)
            time.sleep(0.3)
        except:
            pass

    print(f"      -> {len(tips)} tips")
    return tips


def main():
    print("=" * 50)
    print("Content Crawler v4.0")
    print("=" * 50)

    beauty_results = []
    skincare_results = []

    # 一言API - 文学、原创、诗词
    print("\n[1] Fetching Hitokoto API...")
    beauty_results.extend(fetch_hitokoto(['d', 'e', 'i'], count=50))
    beauty_results.extend(fetch_hitokoto(['f', 'g', 'h', 'k'], count=20))

    # 今日诗词
    print("\n[2] Fetching Jinrishici...")
    beauty_results.extend(fetch_jinrishici())

    # 护肤知识
    print("\n[3] Fetching skincare tips...")
    skincare_results.extend(fetch_skincare_tips())

    # 保存
    print("\n[4] Saving results...")

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
