import argparse
import os.path as osp
import pprint

import imageio
import imgviz
import tqdm

from ..utils import get_macro_block_size


def resize(in_file, scale=1):
    stem, ext = osp.splitext(in_file)
    out_file = stem + "_resize{:.3g}".format(scale) + ext

    reader = imageio.get_reader(in_file)
    meta = reader.get_meta_data()
    fps = meta["fps"]

    width, height = None, None
    if scale:
        width, height = meta["size"]
        width = int(round(scale * width) // 2 * 2)
        height = int(round(scale * height) // 2 * 2)

    macro_block_size = get_macro_block_size((height, width))

    writer = imageio.get_writer(
        out_file,
        fps=fps,
        macro_block_size=macro_block_size,
        ffmpeg_log_level="error",
    )

    for i in tqdm.trange(reader.count_frames(), desc=out_file):
        frame = reader.get_data(i)
        if width is not None and height is not None:
            frame = imgviz.resize(
                frame, height=height, width=width, interpolation="linear"
            )
        writer.append_data(frame)

    reader.close()
    writer.close()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("in_files", nargs="+", help="input video")
    parser.add_argument("--scale", type=float, default=1, help="resize")
    args = parser.parse_args()

    pprint.pprint(args.__dict__)

    for in_file in args.in_files:
        resize(
            in_file=in_file,
            scale=args.scale,
        )
