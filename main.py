from video_toolkit.cli.cli import parse_arguments
from video_toolkit.core import compressor, extractor
from video_toolkit.utils import file_utils
import os

def main():
    args = parse_arguments()

    input_path = args.input
    output_dir = args.output
    n = args.n

    # Ensure output directory exists
    file_utils.ensure_directory(output_dir)

    if args.compress:
        compressed_path = os.path.join(output_dir, "compressed.mp4")
        print(f"[INFO] Compressing video to: {compressed_path}")
        compressor.compress_video(input_path, compressed_path)
    else:
        compressed_path = input_path  # Use original if not compressing

    if args.extract:
        frames_dir = os.path.join(output_dir, "frames")
        print(f"[INFO] Extracting every {n}-th frame to: {frames_dir}")
        extractor.extract_every_nth_frame(compressed_path, frames_dir, n)

if __name__ == "__main__":
    main()
