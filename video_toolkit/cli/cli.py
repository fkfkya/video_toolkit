# video_toolkit/cli/cli.py

import argparse
from video_toolkit.core import config

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
        default="output",
        help="Path to the output directory (default: ./output)."
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
        default=config.DEFAULT_FRAME_INTERVAL,
        help=f"Extract every N-th frame (default: {config.DEFAULT_FRAME_INTERVAL})"
    )

    parser.add_argument(
        "--crf",
        type=int,
        default=config.DEFAULT_CRF,
        help=f"CRF value for compression (default: {config.DEFAULT_CRF})"
    )

    parser.add_argument(
        "--preset",
        type=str,
        default=config.DEFAULT_PRESET,
        choices=["ultrafast", "superfast", "medium", "slow", "veryslow"],
        help=f"FFmpeg preset (default: {config.DEFAULT_PRESET})"
    )

    return parser.parse_args()
