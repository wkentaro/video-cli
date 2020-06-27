import argparse
import glob
import os.path as osp
import pprint

import imageio
import tqdm

from .. import utils


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("out_file", help="out file")
    parser.add_argument(
        "-i",
        "--input-files",
        default="*.jpg",
        help="Input patterns like '*.jpg'",
    )
    parser.add_argument("--fps", type=int, default=10, help="fps")
    parser.add_argument(
        "--nframes", type=int, help="num frames (default: all)"
    )
    args = parser.parse_args()

    pprint.pprint(args.__dict__)

    args.input_files = glob.glob(args.input_files)

    # fix low fps for non-GIF videos
    n_times_write = 1
    if osp.splitext(args.out_file)[1] != ".gif" and args.fps < 10:
        n_times_write = 10 // args.fps
        args.fps = 10

    files = utils.natural_sort(args.input_files)
    if args.nframes:
        files = files[: args.nframes]

    writer = None
    for f in tqdm.tqdm(iterable=files, desc=args.out_file):
        frame = imageio.imread(f)
        frame = utils.resize_to_even(frame)

        if writer is None:
            writer = imageio.get_writer(
                args.out_file,
                fps=args.fps,
                macro_block_size=utils.get_macro_block_size(frame.shape[:2]),
                ffmpeg_log_level="error",
            )
        for _ in range(n_times_write):
            writer.append_data(frame)
