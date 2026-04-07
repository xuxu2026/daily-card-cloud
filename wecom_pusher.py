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
    读取图片，如超过 2MB 则自动缩放压缩至 2MB 以内。
    优先用 PNG 优化压缩（compress_level=9），如仍超限则按比例缩小尺寸。
    返回最终的图片 bytes。
    """
    from PIL import Image

    with open(image_path, "rb") as f:
        raw = f.read()

    if len(raw) <= WECOM_IMAGE_MAX_BYTES:
        return raw  # 原图已在限制内，直接返回

    img = Image.open(image_path)
    w, h = img.size
    _log(f"[i] 原图 {w}x{h}px {len(raw)/1024:.0f}KB，超过2MB，开始压缩...")

    # 先尝试 PNG 最高压缩
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True, compress_level=9)
    data = buf.getvalue()
    if len(data) <= WECOM_IMAGE_MAX_BYTES:
        _log(f"[i] PNG优化压缩后 {len(data)/1024:.0f}KB，OK")
        return data

    # 仍超限：按比例缩小到 2x（1500x2200）
    scale = 0.667  # 3x → 2x
    new_w, new_h = int(w * scale), int(h * scale)
    img2 = img.resize((new_w, new_h), Image.LANCZOS)
    buf2 = io.BytesIO()
    img2.save(buf2, format="PNG", optimize=True, compress_level=9)
    data2 = buf2.getvalue()
    _log(f"[i] 缩放至 {new_w}x{new_h}px 后 {len(data2)/1024:.0f}KB")
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
