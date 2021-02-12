import argparse
import os.path as osp
import pprint

import imageio
import tqdm

from .. import utils


def clip(in_file, start=0, end=None, inplace=False):
    stem, ext = osp.splitext(in_file)
    if end is None:
        out_file = stem + "_trim{:.3g}-end".format(start) + ext
    else:
        out_file = stem + "_trim{:.3g}-{:.3g}".format(start, end) + ext

    reader = imageio.get_reader(in_file)
    meta_data = reader.get_meta_data()

    writer = imageio.get_writer(
        out_file,
        fps=meta_data["fps"],
        macro_block_size=utils.get_macro_block_size(meta_data["size"]),
    )

    for i in tqdm.trange(reader.count_frames(), desc=out_file):
        elapsed_time = i * 1.0 / meta_data["fps"]
        if elapsed_time < start:
            continue

        data = reader.get_data(i)
        writer.append_data(data)

        if end and elapsed_time >= end:
            break

    reader.close()
    writer.close()

    if inplace:
        raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("in_files", nargs="+", help="input video")
    parser.add_argument("--start", type=float, default=0, help="start")
    parser.add_argument("--duration", type=float, help="duration")
    args = parser.parse_args()

    pprint.pprint(args.__dict__)

    end = None
    if args.duration:
        end = args.start + args.duration

    for in_file in args.in_files:
        clip(
            in_file=in_file,
            start=args.start,
            end=end,
        )
