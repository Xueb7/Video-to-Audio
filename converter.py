#!/usr/bin/env python3
"""
MP4 转 MP3 转换器
使用方法：
  python converter.py input.mp4
  或者拖拽 MP4 文件到此脚本
"""

import subprocess
import sys
import os
from pathlib import Path

def convert_mp4_to_mp3(input_file):
    """将 MP4 文件转换为 MP3"""

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"❌ 错误：文件不存在 - {input_file}")
        return False

    # 检查是否是 MP4 文件
    if not input_file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm')):
        print(f"⚠️  警告：文件格式可能不支持 - {input_file}")

    # 生成输出文件名
    input_path = Path(input_file)
    output_file = input_path.stem + '.mp3'

    # 如果输出文件已存在，添加编号
    if os.path.exists(output_file):
        counter = 1
        while os.path.exists(f"{input_path.stem}_{counter}.mp3"):
            counter += 1
        output_file = f"{input_path.stem}_{counter}.mp3"

    print(f"📥 输入文件：{input_file}")
    print(f"📤 输出文件：{output_file}")
    print(f"⏳ 正在转换，请稍候...\n")

    try:
        # 调用 FFmpeg 转换
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vn',                    # 不处理视频
            '-acodec', 'libmp3lame',  # 使用 MP3 编码
            '-q:a', '2',              # 质量等级 (0-9, 0最好)
            '-y',                      # 覆盖输出文件
            output_file
        ]

        # 运行转换
        subprocess.run(cmd, check=True)

        # 获取输出文件大小
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB

        print(f"\n✅ 转换成功！")
        print(f"📊 输出文件大小：{file_size:.1f} MB")
        print(f"📁 文件位置：{os.path.abspath(output_file)}")

        return True

    except FileNotFoundError:
        print("❌ 错误：找不到 FFmpeg")
        print("请先安装 FFmpeg：")
        print("  Windows: choco install ffmpeg")
        print("  或访问 https://ffmpeg.org/download.html")
        return False

    except subprocess.CalledProcessError as e:
        print(f"❌ 转换失败：{e}")
        return False

    except Exception as e:
        print(f"❌ 错误：{e}")
        return False


def main():
    """主函数"""

    print("=" * 50)
    print("   MP4 转 MP3 转换器")
    print("=" * 50)
    print()

    # 获取输入文件
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        print("用法：")
        print("  1. 将 MP4 文件拖拽到此脚本")
        print("  2. 或在命令行运行：python converter.py 文件名.mp4")
        print()
        input_file = input("请输入文件路径：").strip().strip('"').strip("'")

    if not input_file:
        print("❌ 没有指定文件")
        return

    # 执行转换
    success = convert_mp4_to_mp3(input_file)

    # 提示用户
    if success:
        print("\n按 Enter 键关闭此窗口...")
        input()
    else:
        print("\n按 Enter 键关闭此窗口...")
        input()


if __name__ == '__main__':
    main()
