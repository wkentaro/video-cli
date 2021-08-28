import argparse
import os
import os.path as osp
import pprint

import imageio
import tqdm


def toimg(in_file, start=0, end=None, per=1):
    stem, ext = osp.splitext(in_file)
    if not osp.exists(stem):
        os.makedirs(stem)

    reader = imageio.get_reader(in_file)
    meta_data = reader.get_meta_data()

    i_offset = None
    for i in tqdm.trange(reader.count_frames()):
        elapsed_time = i * 1.0 / meta_data["fps"]
        if elapsed_time < start:
            continue
        if i_offset is None:
            i_offset = i

        if (i - i_offset) % per == 0:
            img = reader.get_data(i)
            img_file = osp.join(stem, "{:08d}.jpg".format(i))
            if not osp.exists(img_file):
                imageio.imsave(img_file, img)

        if end and elapsed_time >= end:
            break

    reader.close()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("in_files", nargs="+", help="input video file")
    parser.add_argument("--start", type=float, default=0, help="start [s]")
    parser.add_argument("--duration", type=float, help="duration [s]")
    parser.add_argument(
        "--per", "--rate", type=int, default=1, help="save per"
    )
    args = parser.parse_args()

    pprint.pprint(args.__dict__)

    end = None
    if args.duration:
        end = args.start + args.duration

    for in_file in args.in_files:
        toimg(in_file=in_file, start=args.start, end=end, per=args.per)
