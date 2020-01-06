import numpy as np
import cv2
from sys import argv
cap = cv2.VideoCapture(argv[1])
state = 'b'

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
