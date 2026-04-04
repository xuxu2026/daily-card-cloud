"""
主入口脚本
每天早上9:30由定时任务调用
执行流程：获取数据 → 生成图片 → 推送到企业微信
"""

import sys
import traceback
import datetime
import hashlib
import os
from pathlib import Path

# 确保脚本所在目录在 Python 路径中
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from data_fetcher import fetch_all_data
from card_generator import generate_image, generate_images, get_holiday_styles, get_style_for_date
from wecom_pusher import send_image_to_wecom, send_text_to_wecom
from config import OUTPUT_IMAGE_PATH

# 上次推送图片的MD5记录（用于去重）
LAST_SENT_MD5_FILE = Path(__file__).parent / ".last_sent_md5"


def get_image_md5(path: str) -> str:
    """计算图片MD5"""
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def is_duplicate_send(image_path: str) -> bool:
    """检查图片是否与上次推送的完全相同（MD5去重）"""
    if not LAST_SENT_MD5_FILE.exists():
        return False
    if not os.path.exists(image_path):
        return False
    current_md5 = get_image_md5(image_path)
    last_md5 = LAST_SENT_MD5_FILE.read_text().strip()
    return current_md5 == last_md5


def mark_sent(image_path: str) -> None:
    """记录本次推送的图片MD5"""
    md5 = get_image_md5(image_path)
    LAST_SENT_MD5_FILE.write_text(md5)


# 进程锁文件（防止并发运行）
LOCK_FILE = Path(__file__).parent / ".running.lock"


def acquire_lock():
    """获取进程锁，防止脚本并发执行"""
    lock_file = open(LOCK_FILE, "w")
    try:
        import msvcrt
        msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        lock_file.write(str(os.getpid()))
        lock_file.flush()
        return lock_file
    except IOError:
        print("[✗] 脚本已在运行中，退出")
        lock_file.close()
        sys.exit(0)


def release_lock(lock_file):
    """释放进程锁"""
    try:
        import msvcrt
        msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
        lock_file.close()
        LOCK_FILE.unlink(missing_ok=True)
    except Exception:
        pass


def main():
    lock_fd = acquire_lock()  # 获取进程锁
    try:
        print(f"\n{'='*50}")
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行日签推送任务")
        print('='*50)

        # Step 1: 获取数据
        print("\n[1/3] 正在获取天气、限号等数据...")
        data = fetch_all_data()
        print(f"  ✓ 数据获取完成 - {data['date']} {data['weekday']}")

        # Step 2: 生成图片
        today = datetime.date.today()
        holiday_styles = get_holiday_styles(today)
        
        if holiday_styles and len(holiday_styles) > 1:
            # 节日期间：生成两张卡片供选择
            print(f"\n[2/3] 节日期间，生成 {len(holiday_styles)} 种主题供选择...")
            
            # 构建多张图片的输出路径
            base_path = Path(OUTPUT_IMAGE_PATH)
            stem = base_path.stem
            suffix = base_path.suffix
            parent = base_path.parent
            
            output_paths = []
            for i, style in enumerate(holiday_styles):
                style_name = style.get('name_en', f'H{i+1}')
                output_paths.append(parent / f"{stem}_{style_name}{suffix}")
            
            # 批量生成
            success = generate_images(data, output_paths, holiday_styles)
            if not success:
                raise Exception("图片生成失败，请检查日志")
            
            # 打印生成的主题名称
            style_names = [s.get('name', s.get('name_en', '?')) for s in holiday_styles]
            print(f"  ✓ 图片生成完成: {' / '.join(style_names)}")
            
            # Step 3: 推送到企业微信
            print(f"\n[3/3] 正在推送到企业微信（{len(output_paths)}张）...")
            
            # 先发送提示文字
            holiday_name = holiday_styles[0].get('name', '节日')
            tip_text = f"🎉 今日{holiday_name}，请选择喜欢的版本："
            send_text_to_wecom(tip_text)
            
            # 发送所有图片
            pushed_count = 0
            for i, path in enumerate(output_paths):
                if is_duplicate_send(str(path)):
                    print(f"  ⊙ {style_name} 与上次相同，跳过")
                    continue
                style_name = holiday_styles[i].get('name', f'版本{i+1}')
                print(f"  发送 {style_name}...", end=" ", flush=True)
                if send_image_to_wecom(str(path)):
                    mark_sent(str(path))
                    pushed_count += 1
                    print("✓")
                else:
                    print("✗")
            
            if pushed_count == len(output_paths):
                print("  ✓ 全部推送成功！")
            else:
                print(f"  ⚠ 推送完成（{pushed_count}/{len(output_paths)}）")
        
        else:
            # 非节日：生成单张卡片（保持原有逻辑）
            print(f"\n[2/3] 正在生成日签图片...")
            success = generate_image(data, OUTPUT_IMAGE_PATH)
            if not success:
                raise Exception("图片生成失败，请检查日志")
            print(f"  ✓ 图片生成完成: {OUTPUT_IMAGE_PATH}")

            # Step 3: 推送到企业微信
            print(f"\n[3/3] 正在推送到企业微信...")
            if is_duplicate_send(OUTPUT_IMAGE_PATH):
                print("  ⊙ 图片与上次相同，跳过推送")
            else:
                pushed = send_image_to_wecom(OUTPUT_IMAGE_PATH)
                if pushed:
                    mark_sent(OUTPUT_IMAGE_PATH)
                    print("  ✓ 推送成功！")
                else:
                    print("  ✗ 推送失败（请检查Webhook配置）")

        print(f"\n[✓] 任务完成！")

    except Exception as e:
        error_msg = f"[!] 日签推送任务出错：{str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        # 尝试发送错误通知
        try:
            send_text_to_wecom(f"⚠️ 每日日签推送失败\n时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n错误：{str(e)}")
        except Exception:
            pass
        sys.exit(1)
    finally:
        release_lock(lock_fd)


if __name__ == "__main__":
    main()
