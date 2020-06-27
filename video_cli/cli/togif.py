import argparse
import os.path as osp
import pprint

import imageio
import imgviz
import numpy as np
import tqdm


def togif(
    in_file,
    fps=None,
    retime=1,
    start=0,
    duration=None,
    resize=None,
    blank_end=None,
):

    out_file = osp.splitext(in_file)[0] + ".gif"

    reader = imageio.get_reader(in_file)
    meta = reader.get_meta_data()
    fps_src = meta["fps"]

    width, height = None, None
    if resize:
        width, height = meta["size"]
        width = int(round(resize * width))
        height = int(round(resize * height))

    if fps is None:
        fps = fps_src

    writer = imageio.get_writer(out_file, fps=fps * retime)

    scale = 1.0 * fps / fps_src

    j = -1
    for i in tqdm.trange(reader.count_frames()):
        elapsed_time = i * 1.0 / meta["fps"]
        if elapsed_time < start:
            continue

        frame = reader.get_data(i)
        if width is not None and height is not None:
            frame = imgviz.resize(
                frame, height=height, width=width, interpolation="linear"
            )

        j_detail = i * scale
        if int(round(j_detail)) != j:
            writer.append_data(frame)
            j = int(round(j_detail))

        if duration and (elapsed_time - start) >= duration:
            break

    if blank_end is not None:
        writer.append_data(np.full_like(frame, blank_end))

    reader.close()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("in_files", nargs="+", help="input video")
    parser.add_argument("--fps", type=float, default=1, help="fps")
    parser.add_argument("--retime", type=float, default=1, help="retime")
    parser.add_argument("--start", type=float, default=0, help="start")
    parser.add_argument("--duration", type=float, help="duration")
    parser.add_argument("--resize", type=float, default=1, help="resize")
    parser.add_argument("--blank-end", type=int, help="blank end")
    args = parser.parse_args()

    pprint.pprint(args.__dict__)

    for in_file in args.in_files:
        togif(
            in_file=in_file,
            fps=args.fps,
            retime=args.retime,
            start=args.start,
            duration=args.duration,
            resize=args.resize,
            blank_end=args.blank_end,
        )
