import os
from natsort import natsorted
import subprocess
import shutil
import tempfile

def calculate_compression_ratio(original_path: str, compressed_path: str):
    original_size = os.path.getsize(original_path)
    compressed_size = os.path.getsize(compressed_path)

    if compressed_size == 0:
        print("[WARN] Сжатый файл пуст")
        return 0, 100

    ratio = original_size / compressed_size
    reduction = (1 - compressed_size / original_size) * 100

    print(f"[INFO] Исходный размер: {original_size / 1024 / 1024:.2f} MB")
    print(f"[INFO] Сжатый размер: {compressed_size / 1024 / 1024:.2f} MB")
    print(f"[INFO] Коэффициент сжатия: {ratio:.2f}")
    print(f"[INFO] Уменьшение: {reduction:.1f}%")

    return ratio, reduction

def frames_to_video(frames_dir: str, output_path: str, fps: int = 30) -> None:
    """
    Собирает .jpg/.png-кадры из папки в .mp4-видео.

    :param frames_dir: Папка, где лежат кадры.
    :param output_path: Итоговый .mp4-файл.
    :param fps: Кадров в секунду (по умолчанию 30).

    Реализация через ffmpeg: быстрее и надёжнее, чем OpenCV VideoWriter.
    Используется H.264 (libx264), совместимый пиксельный формат yuv420p и faststart.
    """

    if not os.path.isdir(frames_dir):
        raise ValueError(f"Frames directory not found: {frames_dir}")

    image_files = [
        f for f in os.listdir(frames_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    if not image_files:
        raise ValueError(f"No .jpg/.png files found in {frames_dir}")

    # «Человеческая» сортировка: frame_1, …, frame_10
    image_files = natsorted(image_files)
    abs_files = [os.path.join(frames_dir, f) for f in image_files]

    # Создаем временную последовательность с ровной нумерацией, чтобы ffmpeg читал строго в нужном порядке
    temp_dir = tempfile.mkdtemp(prefix=".ffmpeg_seq_", dir=frames_dir)
    try:
        for idx, src in enumerate(abs_files):
            # сохраняем исходное расширение (jpg/png)
            ext = os.path.splitext(src)[1].lower()
            dst = os.path.join(temp_dir, f"seq_{idx:05d}{ext}")
            try:
                os.symlink(src, dst)
            except (AttributeError, NotImplementedError, OSError):
                shutil.copy2(src, dst)  # копируем, если symlink недоступен

        '''
        Запускаем ffmpeg по шаблону 
        
        -framerate задает входной fps,
        -r фиксирует выходной fps, libx264 + yuv420p для совместимости,
        +faststart для мгновенного старта MP4 в плеерах.
        '''

        has_jpg = any(p.lower().endswith((".jpg", ".jpeg")) for p in os.listdir(temp_dir))
        has_png = any(p.lower().endswith(".png") for p in os.listdir(temp_dir))

        # Если кадры смешанные (jpg и png), ffmpeg одного вызова с шаблоном не поймет
        if has_jpg and has_png:
            unified_dir = os.path.join(temp_dir, "_jpg")
            os.makedirs(unified_dir, exist_ok=True)
            # перекодируем все png в jpg, а jpg просто копируем
            for name in natsorted(os.listdir(temp_dir)):
                if not name.startswith("seq_"):
                    continue
                src_path = os.path.join(temp_dir, name)
                if name.lower().endswith(".png"):
                    dst_path = os.path.join(unified_dir, os.path.splitext(name)[0] + ".jpg")
                    cmd = [
                        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-i", src_path, dst_path
                    ]
                    subprocess.run(cmd, check=True)
                elif name.lower().endswith((".jpg", ".jpeg")):
                    dst_path = os.path.join(unified_dir, os.path.splitext(name)[0] + ".jpg")
                    try:
                        os.symlink(src_path, dst_path)
                    except Exception:
                        shutil.copy2(src_path, dst_path)
            temp_dir_for_ffmpeg = unified_dir
            pattern = os.path.join(temp_dir_for_ffmpeg, "seq_%05d.jpg")
        else:
            temp_dir_for_ffmpeg = temp_dir
            # выбираем расширение по найденным файлам
            ext = ".jpg" if has_jpg else ".png"
            pattern = os.path.join(temp_dir_for_ffmpeg, f"seq_%05d{ext}")

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(fps),
            "-i", pattern,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-r", str(fps),
            "-movflags", "+faststart",
            output_path,
        ]
        subprocess.run(cmd, check=True)

        print(f"[INFO] video saved → {output_path}")
    finally:
        # Чистим временную последовательность
        shutil.rmtree(temp_dir, ignore_errors=True)
