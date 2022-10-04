#!/usr/bin/env python3

import argparse
from sys import argv, exit
from util.video import SimpleDither
from util.image import ImageDiff

def main():

    parser = argparse.ArgumentParser(
        description="Compare frames from a video or capture device")

    parser.add_argument(
            "--fill-value",
            type=int,
            help="Used with mask method, fill value for detected image changes.",
            )
    parser.add_argument(
            "--dither-method",
            "-x",
            default="g",
            choices=("r", "g", "b", "m", "n"),
            help="Dither detection method",
            )
    parser.add_argument(
            "--mode",
            "-m",
            default="dithering",
            choices=("dithering", "image"),
            help="Method of operation: dithering means differentiating frames sequentially from a video source, and image compares two arbitrary frames",
            )
    parser.add_argument(
            "--display",
            "-d",
            action='store_true',
            default=False,
            )
    parser.add_argument(
            "--output",
            "-o",
            type=str,
            help="Output file, must be .avi format",
            )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
            "--cap",
            type=int,
            help="Index value of cv2.VideoCapture device",
            )
    group.add_argument(
            "--file",
            type=str,
            nargs="*",
            help="Path to AVI file to use instead of a video device",
            )

    if len(argv) < 2:
        parser.print_usage()
        exit(1)

    args = parser.parse_args()

    filelen = len(args.file)
    mode = args.mode
    print(f"Number of file arguments: {filelen}, Mode {mode}")

    if args.mode == "dithering":
        if len(args.file) > 1:
            print("Only one file is allowed")
            exit(1)
        file = args.file[0]
        source = args.cap if args.cap is not None else file
        video = SimpleDither(
            source,
            fill_value=args.fill_value,
            state=args.dither_method,
        )

        video.process(display=args.display, output_path=args.output)

    if args.mode == 'image':
        if len(args.file) != 2:
            print("Need two files for image differentiation mode")
            exit(1)
        image = ImageDiff(
                args.file,
                fill_value=args.fill_value,
                state=args.dither_method,
        )
        image.process(display=args.display)


if __name__ == '__main__':
    main()
