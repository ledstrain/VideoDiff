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
            frametext = "{frame}/{totalframes}".format(frame=frameinfo['frame'], totalframes=frameinfo['totalframes'])
            fontScale = min(width, height) * 0.0017
            yPos = int(height / 20)
            cv2.putText(frame, frametext, (0, yPos), cv2.FONT_HERSHEY_SIMPLEX, fontScale, [255, 255, 255], 3, cv2.FILLED);

        return frame

    def generate_frames(self, output=None, frameinfo=None):
        for i in range(0, self.sequence):
            if frameinfo:
                self.frames.append(self.generate_random_frame(self.height, self.width, {'frame': i, 'totalframes': self.sequence}))
            else:
                self.frames.append(self.generate_random_frame(self.height, self.width))
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
    parser.add_argument(
            "--frameinfo",
            action="store_true",
            default=False,
            help="Whether to overlay frame number markings on output",
    )

    args = parser.parse_args()
    fg = FrameGenerator(args.frames, args.width, args.height, args.seed)
    fg.generate_frames(args.output, args.frameinfo)
    if args.mode == 'display':
        fg.display_as_video()

if __name__ == '__main__':
    main()
