import argparse
import glob
import os.path as osp

import imageio
import tqdm

from ..utils import get_macro_block_size
from ..utils import natural_sort


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("out_file")
    parser.add_argument(
        "-i",
        "--input-files",
        default="*.jpg",
        help="Input patterns like '*.jpg'",
    )
    parser.add_argument("--fps", type=int, default=10)
    args = parser.parse_args()

    args.input_files = glob.glob(args.input_files)

    # fix low fps for non-GIF videos
    n_times_write = 1
    if osp.splitext(args.out_file)[1] != ".gif" and args.fps < 10:
        n_times_write = 10 // args.fps
        args.fps = 10

    writer = None
    for f in tqdm.tqdm(natural_sort(args.input_files), ncols=80):
        frame = imageio.imread(f)

        if writer is None:
            writer = imageio.get_writer(
                args.out_file,
                fps=args.fps,
                macro_block_size=get_macro_block_size(frame.shape[:2]),
            )
        for _ in range(n_times_write):
            writer.append_data(frame)
