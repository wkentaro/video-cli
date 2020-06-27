import argparse
import os
import os.path as osp
import pprint

import imageio
import tqdm


def toimg(in_file, start=0, end=None, rate=1):
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

        if (i - i_offset) % rate == 0:
            data = reader.get_data(i)
            imageio.imsave(osp.join(stem, "{:08d}.jpg".format(i)), data)

        if end and elapsed_time >= end:
            break

    reader.close()


def main():
    def natural_number(val):
        val = int(val)
        if val < 1:
            raise ValueError("val must be natural number")
        return val

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("in_files", nargs="+", help="input video")
    parser.add_argument("--start", type=float, default=0, help="start")
    parser.add_argument("--duration", type=float, help="duration")
    parser.add_argument("--rate", type=natural_number, default=1, help="rate")
    args = parser.parse_args()

    pprint.pprint(args.__dict__)

    end = None
    if args.duration:
        end = args.start + args.duration

    for in_file in args.in_files:
        toimg(in_file=in_file, start=args.start, end=end, rate=args.rate)
