#!/usr/bin/env python3

import argparse

from util.video import VideoDiff


def main():

    parser = argparse.ArgumentParser(description="Compare frames from a video or capture device")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--cap", type=int, help="Index value of cv2.VideoCapture device")
    group.add_argument("--file", type=str, help="Path to AVI file to use instead of a video device")

    args = parser.parse_args()

    if args.cap:
        source = args.cap
    elif args.file:
        source = args.file


    video = VideoDiff(source)
    video.render()


if __name__ == '__main__':
    main()
