#!/usr/bin/env python3

import argparse
from sys import argv, exit
from util.video import Dithering


def main():

    parser = argparse.ArgumentParser(
        description="Compare frames from a video or capture device")

    parser.add_argument(
            "--fill-value",
            type=int,
            help="Used with mask method, fill value for detected image changes.")
    parser.add_argument(
            "--dither-method",
            "-x",
            default="g",
            choices=("r", "g", "b", "m", "n"),
            help="Dither detection method")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
            "--display",
            "-d",
            action='store_true')
    group.add_argument(
            "--output",
            "-o",
            type=str,
            help="Output file, must be .avi format")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
            "--cap",
            type=int,
            help="Index value of cv2.VideoCapture device")
    group.add_argument(
            "--file",
            type=str,
            help="Path to AVI file to use instead of a video device")

    if len(argv) < 2:
        parser.print_usage()
        exit(1)

    args = parser.parse_args()

    source = args.cap if args.cap is not None else args.file

    video = Dithering(
        source,
        fill_value=args.fill_value,
        state=args.dither_method,
    )

    if args.display is True:
        video.show()
    if args.output:
        video.save(args.output)


if __name__ == '__main__':
    main()
