from video_toolkit.cli.cli import parse_arguments
from video_toolkit.core import compressor, extractor, config
from video_toolkit.utils import file_utils
from video_toolkit.utils import frames_to_video
import os

def make_compressed_name(input_path: str, output_dir: str) -> str:
    base = os.path.basename(input_path)
    name, ext = os.path.splitext(base)
    return os.path.join(output_dir, f"{name}_compressed{ext}")


def main():
    args = parse_arguments()

    input_path = args.input
    output_dir = args.output
    n = args.n
    crf = args.crf
    preset = args.preset

    file_utils.ensure_directory(output_dir)

    if args.compress:
        compressed_path = make_compressed_name(input_path, output_dir)
        print(f"[INFO] Compressing video to: {compressed_path}")
        compressor.compress_video(input_path, compressed_path)

        if args.ratio:
            from video_toolkit.utils import calculate_compression_ratio
            calculate_compression_ratio(input_path, compressed_path)

    else:
        compressed_path = input_path  # не сжимаем — работаем с оригиналом

    if args.extract:
        frames_dir = os.path.join(output_dir, config.FRAMES_FOLDERNAME)
        print(f"[INFO] Extracting every {n}-th frame to: {frames_dir}")
        extractor.extract_every_nth_frame(compressed_path, frames_dir, n)
    if args.assemble:
        assembled_path = os.path.join(output_dir, "assembled.mp4")
        frames_to_video(os.path.join(output_dir, config.FRAMES_FOLDERNAME),
                        assembled_path,
                        fps=args.fps)


if __name__ == "__main__":
    main()
