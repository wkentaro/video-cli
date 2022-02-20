import argparse
import pprint

import imageio
import imgviz
import numpy as np
import tqdm

from .. import utils


def tile(in_files, out, resize=1, shape=None, duration="max"):
    fps = None
    n_frames = None
    readers = []
    for in_file in in_files:
        reader = imageio.get_reader(in_file)
        readers.append(reader)

        if fps is None:
            fps = reader.get_meta_data()["fps"]

        if n_frames is None:
            n_frames = reader.count_frames()
        else:
            if duration == "min":
                n_frames = min(n_frames, reader.count_frames())
            else:
                n_frames = max(n_frames, reader.count_frames())

    writer = None
    images_blank = None
    pbar = tqdm.tqdm(desc=out, total=n_frames)
    for i in range(n_frames):
        images = []
        finished = []
        for j, reader in enumerate(readers):
            try:
                img = reader.get_data(i)
                if resize != 1:
                    height = int(round(img.shape[0] * resize))
                    img = imgviz.resize(img, height=height)
                finished.append(False)
            except IndexError:
                img = images_blank[j]
                finished.append(True)
            images.append(img)
        if all(finished):
            break
        if images_blank is None:
            images_blank = [np.zeros_like(img) for img in images]
        img = imgviz.tile(images, shape=shape, border=(255, 255, 255))
        img = utils.resize_to_even(img)
        if writer is None:
            writer = imageio.get_writer(
                out,
                fps=fps,
                macro_block_size=utils.get_macro_block_size(img.shape[:2]),
                ffmpeg_log_level="error",
            )
        writer.append_data(img)
        pbar.update()
    pbar.close()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("in_files", nargs="+", help="video files")
    parser.add_argument("--out", "-o", required=True, help="out file")
    parser.add_argument("--resize", type=float, default=1, help="resize")
    parser.add_argument("--shape", help="row x col (e.g., 2x3)")
    parser.add_argument("--duration", default="max", choices=["max", "min"])
    args = parser.parse_args()

    pprint.pprint(args.__dict__)

    if args.shape is not None:
        args.shape = [int(x) for x in args.shape.split("x")]

    tile(
        in_files=args.in_files,
        out=args.out,
        resize=args.resize,
        shape=args.shape,
        duration=args.duration,
    )
