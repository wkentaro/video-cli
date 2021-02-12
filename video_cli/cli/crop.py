import argparse
import os.path as osp
import pprint

import cv2
import imageio
import tqdm

from ..utils import get_macro_block_size


def selectROI(img):
    height, width = img.shape[:2]

    max_height = 500
    max_width = 1000
    scale = min(max_height / height, max_width / width)

    img = cv2.resize(img, None, None, fx=scale, fy=scale)
    roi = cv2.selectROI(img[:, :, ::-1])

    x1, y1, w, h = roi
    x2 = x1 + w
    y2 = y1 + h

    y1 = int(round(y1 / scale))
    x1 = int(round(x1 / scale))
    y2 = int(round(y2 / scale))
    x2 = int(round(x2 / scale))

    return y1, x1, y2, x2


def crop(in_file):
    stem, ext = osp.splitext(in_file)
    out_file = stem + "_crop" + ext

    reader = imageio.get_reader(in_file)
    meta = reader.get_meta_data()
    fps = meta["fps"]

    y1, x1, y2, x2 = selectROI(reader.get_data(0))

    width = x2 - x1
    height = y2 - y1

    if height % 2 != 0:
        height -= 1
        y2 -= 1
    if width % 2 != 0:
        width -= 1
        x2 -= 1

    macro_block_size = get_macro_block_size((height, width))

    writer = imageio.get_writer(
        out_file,
        fps=fps,
        macro_block_size=macro_block_size,
        ffmpeg_log_level="error",
    )

    for i in tqdm.trange(reader.count_frames(), desc=out_file):
        frame = reader.get_data(i)
        frame = frame[y1:y2, x1:x2]
        writer.append_data(frame)

    reader.close()
    writer.close()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("in_file", help="input video")
    args = parser.parse_args()

    pprint.pprint(args.__dict__)

    crop(in_file=args.in_file)
