import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Video Toolkit: compress video and extract every N-th frame."
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the input video file."
    )

    parser.add_argument(
        "--output", "-o",
        required=False,
        help="Path to the output directory (default: ./output/).",
        default="output"
    )

    parser.add_argument(
        "--compress",
        action="store_true",
        help="Enable video compression."
    )

    parser.add_argument(
        "--extract",
        action="store_true",
        help="Enable extraction of every N-th frame."
    )

    parser.add_argument(
        "--n",
        type=int,
        default=10,
        help="Extract every N-th frame (used only if --extract is set)."
    )

    return parser.parse_args()