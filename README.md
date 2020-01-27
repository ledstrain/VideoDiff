VideoDiff
=========

A program to attempt to test a video source for temporal dithering and other visual artifacts

# License

GPLv2 (see LICENSE)

# Warning

Documentation is incomplete and more work needs to be done

```
usage: main.py [-h] [--fill-value FILL_VALUE] [--dither-method {r,g,b,m}]
               [--display | --output OUTPUT] [--cap CAP | --file FILE]

Compare frames from a video or capture device

optional arguments:
  -h, --help            show this help message and exit
  --fill-value FILL_VALUE
                        Used with mask method, fill value for detected image
                        changes.
  --dither-method {r,g,b,m}, -x {r,g,b,m}
                        Dither detection method
  --display, -d
  --output OUTPUT, -o OUTPUT
                        Output file, must be .avi format
  --cap CAP             Index value of cv2.VideoCapture device
  --file FILE           Path to AVI file to use instead of a video device
```

# Requirements

- Python >= 3.4
- NumPy
- OpenCV with Python bindings
- ffmpeg (need to test how library linking works)

# Tested platforms
Windows x86_64

Linux x86_64 (Gentoo)

# Keybindings

`r`: Switch to the red channel

`g`: Switch to the green channel

`b`: Switch to the blue channel

`m`: Switch to mask mode

`q`: Quit
