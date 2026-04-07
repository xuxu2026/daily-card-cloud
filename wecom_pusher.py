"""
企业微信机器人推送模块
支持发送图片消息（base64）到企业微信群机器人
企业微信限制：图片≤2MB
"""

import datetime
import hashlib
import io
import os
import requests
import base64
from config import WECOM_WEBHOOK_URL

# 企业微信图片大小上限（bytes）
WECOM_IMAGE_MAX_BYTES = 2 * 1024 * 1024  # 2MB

# 推送日志文件
PUSH_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".push_log.txt")


def _log(msg: str):
    """带时间戳的日志，同时输出和写文件"""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    line = f"[{ts}] {msg}"
    print(line)
    with open(PUSH_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _compress_image_for_wecom(image_path: str) -> bytes:
    """
    读取图片，在 2MB 限制内输出最清晰的图片。
    策略：优先用 JPEG 高质量（95），如超限则逐步降质量，最后才缩放尺寸。
    """
    from PIL import Image

    with open(image_path, "rb") as f:
        raw = f.read()

    if len(raw) <= WECOM_IMAGE_MAX_BYTES:
        return raw  # 原图已在限制内，直接返回

    img = Image.open(image_path)
    w, h = img.size
    _log(f"[i] 原图 {w}x{h}px {len(raw)/1024:.0f}KB，超过2MB，开始优化...")

    # 如果原图是 RGBA，先转 RGB（JPEG 不支持透明）
    if img.mode == "RGBA":
        # 把透明背景合成到白色上
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg

    # JPEG 质量迭代：从95往下找最优值
    for quality in [95, 90, 85, 80, 75, 70]:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        data = buf.getvalue()
        size_kb = len(data) / 1024
        if len(data) <= WECOM_IMAGE_MAX_BYTES:
            _log(f"[i] JPEG q={quality} {w}x{h}px {size_kb:.0f}KB，OK")
            return data

    # JPEG 质量70仍超限 → 缩放尺寸
    # 目标：缩到约 2x 像素数（1500x2200），仍用 JPEG q=85
    target_area = int(w * h * 0.44)  # 约 1/2.25 倍
    ratio = w / h
    target_h = int((target_area / ratio) ** 0.5)
    target_w = int(target_h * ratio)
    img2 = img.resize((target_w, target_h), Image.LANCZOS)
    buf2 = io.BytesIO()
    img2.save(buf2, format="JPEG", quality=85, optimize=True)
    data2 = buf2.getvalue()
    _log(f"[i] 缩放至 {target_w}x{target_h}px + JPEG q=85 → {len(data2)/1024:.0f}KB")
    return data2


def send_image_to_wecom(image_path: str) -> bool:
    """
    发送图片到企业微信机器人
    企业微信图片消息需要 base64 编码 + md5
    """
    if not os.path.exists(image_path):
        _log(f"[✗] 图片文件不存在: {image_path}")
        return False

    # 自动压缩（超过 2MB 则缩小）
    image_data = _compress_image_for_wecom(image_path)

    image_base64 = base64.b64encode(image_data).decode("utf-8")
    image_md5 = hashlib.md5(image_data).hexdigest()

    _log(f"[→] 开始推送图片: {os.path.basename(image_path)} | {len(image_data)/1024:.0f}KB | MD5: {image_md5}")

    payload = {
        "msgtype": "image",
        "image": {
            "base64": image_base64,
            "md5": image_md5,
        }
    }

    try:
        resp = requests.post(
            WECOM_WEBHOOK_URL,
            json=payload,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        result = resp.json()
        if result.get("errcode") == 0:
            _log(f"[✓] 图片推送成功！MD5: {image_md5}")
            return True
        else:
            _log(f"[✗] 推送失败：{result}")
            return False
    except Exception as e:
        _log(f"[✗] 推送异常: {e}")
        return False


def send_text_to_wecom(text: str) -> bool:
    """发送文本消息到企业微信机器人（用于错误通知）"""
    payload = {
        "msgtype": "text",
        "text": {"content": text}
    }
    try:
        resp = requests.post(WECOM_WEBHOOK_URL, json=payload, timeout=10)
        return resp.json().get("errcode") == 0
    except Exception as e:
        print(f"[✗] 文本推送异常: {e}")
        return False


if __name__ == "__main__":
    # 测试发送
    test_image = "C:/Users/30286/WorkBuddy/20260403180838/daily-card/output/daily_card.png"
    send_image_to_wecom(test_image)
