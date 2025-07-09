import cv2
import os

def extract_every_nth_frame(video_path: str, output_folder: str, n: int):
    """
    Извлекает каждый n-й кадр из видео и сохраняет его как изображение.

    :param video_path: Путь к видеофайлу
    :param output_folder: Папка для сохранения кадров
    :param n: Интервал кадров (каждый n-й)
    """
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")

    frame_index = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % n == 0:
            filename = os.path.join(output_folder, f"frame_{saved_count:05}.jpg")
            cv2.imwrite(filename, frame)
            saved_count += 1

        frame_index += 1

    cap.release()
    print(f"[SUCCESS] Extracted {saved_count} frames to {output_folder}")
