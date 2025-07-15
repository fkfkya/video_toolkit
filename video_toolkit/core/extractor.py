import os
import subprocess

def extract_every_nth_frame(video_path: str, output_folder: str, n: int):
    """
    Извлекает каждый n-й кадр из видео и сохраняет его как изображение.

    :param video_path: Путь к видеофайлу
    :param output_folder: Папка для сохранения кадров
    :param n: Интервал кадров (каждый n-й)

    Реализация через ffmpeg: значительно быстрее, чем покадровое чтение через OpenCV.
    """

    if n < 1:
        raise ValueError("n должно быть >= 1")

    os.makedirs(output_folder, exist_ok=True)

    pattern = os.path.join(output_folder, "frame_%05d.jpg")
    vf = f"select='not(mod(n\\,{n}))'"

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", video_path,
        "-vf", vf,
        "-vsync", "vfr",    # корректная нумерация при пропуске кадров
        "-start_number", "0",
        pattern,
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Cannot extract frames with ffmpeg: {e}") from e

    saved_count = sum(
        1 for f in os.listdir(output_folder)
        if f.startswith("frame_") and f.endswith(".jpg")
    )

    print(f"[SUCCESS] Extracted {saved_count} frames to {output_folder}")
