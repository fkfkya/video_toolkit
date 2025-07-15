import subprocess
import os

def compress_video(input_path: str, output_path: str, crf: int = 28, preset: str = "medium", codec: str = "h264"):
    """
    :param input_path: Путь к входному видео
    :param output_path: Путь к выходному сжатому видео
    :param crf: Коэффициент качества (чем выше — тем сильнее сжатие, разумный диапазон: 18–32)
    :param preset: Скорость сжатия (ultrafast, fast, medium, slow, veryslow)
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input video not found: {input_path}")

    vcodec = (
        "libx265" if codec.lower() in ("h265", "hevc")
        else "libx264" if codec.lower() in ("h264", "avc")
        else codec  # оставляем как есть, если явно передали валидный энкодер (например, h264_videotoolbox)
    )

    out_dir = os.path.dirname(output_path) or "."
    os.makedirs(out_dir, exist_ok=True)

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", input_path,
        "-c:v", vcodec, "-preset", preset, "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ]


    try:
        subprocess.run(cmd, check=True)
        print(f"[SUCCESS] Video compressed and saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] ffmpeg compression failed: {e}")
