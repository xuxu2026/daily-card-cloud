# 小红书内容采集器
# 使用小红书API搜索美文和护肤贴士

import requests
import json
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
        # 清理HTML标签
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


def search_xhs(keyword, limit=10):
    """搜索小红书"""
    try:
        resp = requests.post(
            "http://localhost:18060/mcp",
            json={
                "tool": "search_feeds",
                "params": {
                    "keyword": keyword,
                    "filters": {
                        "sort_by": "最多点赞",
                        "note_type": "图文",
                        "publish_time": "半年内"
                    }
                }
            },
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("feeds", [])[:limit]
    except Exception as e:
        print(f"    Search error: {e}")
    return []


def get_feed_detail(feed_id, xsec_token):
    """获取笔记详情"""
    try:
        resp = requests.post(
            "http://localhost:18060/mcp",
            json={
                "tool": "get_feed_detail",
                "params": {
                    "feed_id": feed_id,
                    "xsec_token": xsec_token,
                    "load_all_comments": False
                }
            },
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            return data
    except Exception as e:
        print(f"    Detail error: {e}")
    return None


def extract_text(feed):
    """从feed中提取文本"""
    texts = []

    # 从noteCard提取正文
    note_card = feed.get("noteCard", {})
    desc = note_card.get("desc", "")
    if desc:
        # 分割长文本为短句
        sentences = re.split(r'[。！？\n]', desc)
        for s in sentences:
            s = s.strip()
            if len(s) >= 15 and len(s) <= 100:
                texts.append(s)

    return texts


def main():
    print("=" * 50)
    print("Xiaohongshu Content Crawler")
    print("=" * 50)

    beauty_results = []
    skincare_results = []

    # 搜索关键词
    beauty_keywords = ["美文", "文案", "语录", "金句", "治愈", "温暖文案", "励志"]
    skincare_keywords = ["护肤", "保养", "护肤心得", "护肤技巧", "皮肤管理"]

    # 搜索美文
    print("\n[1] Searching beauty texts...")
    for kw in beauty_keywords:
        print(f"    Searching: {kw}...")
        feeds = search_xhs(kw, limit=10)
        for feed in feeds:
            texts = extract_text(feed)
            beauty_results.extend(texts)
            # 避免请求太快
            time.sleep(0.5)
        print(f"      -> Found {len(feeds)} feeds")

    # 搜索护肤
    print("\n[2] Searching skincare tips...")
    for kw in skincare_keywords:
        print(f"    Searching: {kw}...")
        feeds = search_xhs(kw, limit=10)
        for feed in feeds:
            texts = extract_text(feed)
            skincare_results.extend(texts)
            time.sleep(0.5)
        print(f"      -> Found {len(feeds)} feeds")

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

    # Show samples
    if total_beauty > 0:
        print("\nSample beauty texts:")
        samples = list(load_existing(BEAUTY_FILE))[-5:]
        for s in samples:
            print(f"  - {s[:50]}...")


if __name__ == "__main__":
    main()
