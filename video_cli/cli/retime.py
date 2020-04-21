import argparse
import os.path as osp

import imageio
import tqdm

from ..utils import get_macro_block_size


def retime(in_file, retime, inplace=False):
    stem, ext = osp.splitext(in_file)
    out_file = stem + "_retime{:.3g}".format(retime) + ext

    reader = imageio.get_reader(in_file)
    meta_data = reader.get_meta_data()
    fps = meta_data["fps"]

    macro_block_size = get_macro_block_size(meta_data["size"])

    writer = imageio.get_writer(
        out_file, fps=fps * retime, macro_block_size=macro_block_size
    )
    for data in tqdm.tqdm(reader, total=reader.count_frames()):
        writer.append_data(data)

    reader.close()
    writer.close()

    if inplace:
        raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("in_files", nargs="+", help="input files")
    parser.add_argument(
        "--retime", "-x", type=float, default=1, help="retime factor"
    )
    parser.add_argument(
        "--inplace", "-i", action="store_true", help="operate in-place"
    )
    args = parser.parse_args()

    for in_file in args.in_files:
        retime(in_file=in_file, retime=args.retime, inplace=args.inplace)
