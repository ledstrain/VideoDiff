#!/usr/bin/env python3

import argparse

from util.video import VideoDiff


def main():

    parser = argparse.ArgumentParser(
            description="Compare frames from a video or capture device")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--display", "-d", action='store_true')
    group.add_argument("--output", "-o", type=str, help="Output file, must be .avi format")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
            "--cap",
            type=int,
            help="Index value of cv2.VideoCapture device")
    group.add_argument(
            "--file",
            type=str,
            help="Path to AVI file to use instead of a video device")
    parser.add_argument(
            "--fill-value",
            type=int,
            help="Fill value for detected image changes")

    args = parser.parse_args()

    source = args.cap if args.cap else args.file

    video = VideoDiff(
        source,
        fill_value=args.fill_value,
    )

    if args.display is True:
        video.show()
    if args.output:
        video.save(args.output)


if __name__ == '__main__':
    main()
