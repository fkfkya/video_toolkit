# video_toolkit/core/compressor.py

import subprocess
import os

def compress_video(input_path: str, output_path: str, crf: int = 28, preset: str = "veryslow"):
    """
    :param input_path: Путь к входному видео
    :param output_path: Путь к выходному сжатому видео
    :param crf: Коэффициент качества (чем выше — тем сильнее сжатие, разумный диапазон: 18–32)
    :param preset: Скорость сжатия (ultrafast, fast, medium, slow, veryslow)
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input video not found: {input_path}")

    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vcodec", "libx265",
        "-crf", str(crf),
        "-preset", preset,
        "-y",                      # Перезаписывать выходной файл без запроса
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"[SUCCESS] Video compressed and saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] ffmpeg compression failed: {e}")
