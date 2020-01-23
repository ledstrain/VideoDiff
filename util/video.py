import cv2


class VideoDiff:
    def __init__(self, source):
        self.colortoindex = {
            "b": 0,
            "g": 1,
            "r": 2,
        }

        self.cap = cv2.VideoCapture(source)
        self.state = 'g'

    def __del__(self):
        # When everything done, release the capture
        cv2.destroyAllWindows()
        self.cap.release()

    @staticmethod
    def getKeyBind(key):
        if cv2.waitKey(1) and 0xFF == ord(key):
            return key

    def show(self):
        windowname = 'diff {}'.format(self.state)
        for vimage in self.__render():
            cv2.imshow(windowname, vimage)

            # quit when 'q' is pressed on the image window
            if self.getKeyBind('q'):
                break
            if self.getKeyBind('r'):
                self.state = 'r'
            if self.getKeyBind('g'):
                self.state = 'g'
            if self.getKeyBind('b'):
                self.state = 'b'

    def save(self, path):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(path, fourcc, fps, (width, height))

        print(path, fps, width, height)
        for vimage in self.__render():
            framewritten = out.write(vimage)
        out.release()

    def __render(self):
        prevcolor = False
        while self.cap.isOpened():
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            if ret is True:
                # Save the previous frame
                if prevcolor is not False:
                    prevcolor = color

                # Zero out all color indexes not specified
                # instead of extracting just the index
                colorindex = self.colortoindex[self.state]
                for index in self.colortoindex.values():
                    if index != colorindex:
                        frame[:, :, index] = 0

                color = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

                # First run, save color as prevcolor and skip
                # Then compare the two
                if prevcolor is not False:
                    image = color - prevcolor
                else:
                    prevcolor = color
                    continue

                yield image

            else:
                # Once video has no more frames
                break
