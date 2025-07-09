# video_toolkit/utils/video_utils.py
import os
import cv2
from natsort import natsorted


def frames_to_video(frames_dir: str, output_path: str, fps: int = 30) -> None:
    """
    Собирает .jpg/.png-кадры из папки в .mp4-видео.

    :param frames_dir: Папка, где лежат кадры.
    :param output_path: Итоговый .mp4-файл.
    :param fps: Кадров в секунду (по умолчанию 30).
    """
    image_files = [
        f for f in os.listdir(frames_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    if not image_files:
        raise ValueError(f"No .jpg/.png files found in {frames_dir}")

    # «Человеческая» сортировка: frame_1, …, frame_10
    image_files = natsorted(image_files)

    first_frame = cv2.imread(os.path.join(frames_dir, image_files[0]))
    h, w, _ = first_frame.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")     # контейнер .mp4
    writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    for fname in image_files:
        frame = cv2.imread(os.path.join(frames_dir, fname))
        if frame is None:
            print(f"[WARN] skipped {fname}")
            continue
        writer.write(frame)

    writer.release()
    print(f"[INFO] video saved → {output_path}")
