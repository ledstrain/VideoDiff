import numpy as np
import argparse
import cv2
state = 'b'

parser = argparse.ArgumentParser(description="Compare frames from a video or capture device")
group = parser.add_mutually_exclusive_group()
group.add_argument("--cap", type=int, help="Index value of cv2.VideoCapture device")
group.add_argument("--file", type=str, help="Path to AVI file to use instead of a video device")


args = parser.parse_args()

if args.cap:
    cap = cv2.VideoCapture(args.cap)
if args.file:
    cap = cv2.VideoCapture(args.file)


def getKeyBind(key):
    if cv2.waitKey(1) & 0xFF == ord(key):
        return key

while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Save the previous frame
    try:
        old_img = img
        pb, pg, pr, _ = cv2.split(old_img)    
    except NameError:
       pass

    img = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
    b, g, r, _ = cv2.split(img)
   
   # Display the resulting frame
    try:
        cv2.imshow('diff {}'.format(state), eval("{} - p{}".format(state, state)))
    except NameError:
        pass
        
    # quit when 'q' is pressed on the image window
    if getKeyBind('q'):
        break
    if getKeyBind('r'):
        state = 'r'
    if getKeyBind('g'):
        state = 'g'
    if getKeyBind('b'):
        state = 'b'

# When everything done, release the capture
cv2.destroyAllWindows()
cap.release()
