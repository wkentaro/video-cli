import argparse
import pprint

import imageio


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("filename", help="filename")
    parser.add_argument("--key", help="key")
    args = parser.parse_args()

    reader = imageio.get_reader(args.filename)
    meta_data = reader.get_meta_data()

    if args.key is None:
        pprint.pprint(meta_data)
    else:
        print(meta_data[args.key])


if __name__ == "__main__":
    main()
