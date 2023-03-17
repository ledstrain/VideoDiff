import argparse
import numpy as np
import cv2

class FrameGenerator:
    def __init__(self, sequence, width, height, seed):
        self.sequence = sequence
        self.width = width
        self.height = height
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.frames = []

    def generate_random_frame(self, height, width, frameinfo=None):
        frame = self.rng.integers(256, size=(height, width, 3), dtype=np.uint8)
        if frameinfo:
            cv2.putText(frame, "{frame}/{totalframes}".format(frame=frameinfo['frame'], totalframes=frameinfo['totalframes']), (0, 20), cv2.FONT_HERSHEY_COMPLEX, 0.8*height, [255, 255, 255], 1, cv2.LINE_AA);
        return frame

    def generate_frames(self, output=None):
        for i in range(0, self.sequence):
            self.frames.append(self.generate_random_frame(self.height, self.width, {'frame': i, 'totalframes': self.sequence}))
            if output:
                output_file = "{output_path}/{frame}.tiff".format(output_path=output, frame=i)
                if cv2.haveImageWriter(output_file):
                    cv2.imwrite(output_file, self.frames[i], None) 
            print("Generated frame {i}".format(i=i))

    def display_as_video(self):
        for frame in self.frames:
            cv2.namedWindow("Display", flags=cv2.WINDOW_GUI_NORMAL + cv2.WINDOW_AUTOSIZE)
            cv2.imshow("Display", frame)
            cv2.waitKey(16)

def main():
    parser = argparse.ArgumentParser(
        description="Generate frames of random noise and display or save to .TIFF",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
            "--seed",
            "-s",
            type=int,
            default=12345,
            help="Seed to use for generating random frames",
    )
    parser.add_argument(
            "--output",
            "-o",
            type=str,
            default="randomnoise",
            help="Directory to save output frames",
    )
    parser.add_argument(
            "--frames",
            type=int,
            default=120,
            help="Number of frames to generate",
    )
    parser.add_argument(
            "--width",
            type=int,
            default=640,
            help="Width of generated frames",
    )
    parser.add_argument(
            "--height",
            type=int,
            default=480,
            help="Height of generated frames",
    )
    parser.add_argument(
            "--mode",
            choices=("output", "display"),
            default="output",
            help="Mode of operation",
    )


    args = parser.parse_args()
    fg = FrameGenerator(args.frames, args.width, args.height, args.seed)
    fg.generate_frames(args.output)
    if args.mode == 'display':
        fg.display_as_video()

if __name__ == '__main__':
    main()
