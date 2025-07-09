from .core import compressor, extractor, config
from .utils import file_utils

import os
from .core import compressor, extractor, config
from .utils import file_utils, frames_to_video


def compress_and_extract(
    input_path: str,
    output_dir: str = "output",
    compress: bool = True,
    extract: bool = True,
    n: int = config.DEFAULT_FRAME_INTERVAL,
    crf: int = config.DEFAULT_CRF,
    preset: str = config.DEFAULT_PRESET
):
    """
    Универсальная функция для сжатия и/или извлечения кадров из видео.
    """
    file_utils.ensure_directory(output_dir)

    if compress:
        compressed_path = os.path.join(output_dir, config.COMPRESSED_FILENAME)
        print(f"[LIB] Compressing video to: {compressed_path}")
        compressor.compress_video(input_path, compressed_path, crf=crf, preset=preset)
    else:
        compressed_path = input_path

    if extract:
        frames_dir = os.path.join(output_dir, config.FRAMES_FOLDERNAME)
        print(f"[LIB] Extracting every {n}-th frame to: {frames_dir}")
        extractor.extract_every_nth_frame(compressed_path, frames_dir, n)
