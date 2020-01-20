ImageComparator
===============

A program to attempt to test a video source for temporal dithering and other visual artifacts

# License

NDA. Will probably be changed to GPL for public release

# Requirements

- Python3
- OpenCV with Python bindings
- ffmpeg (need to test how library linking works)

# Tested platforms
x86_64 Windows 7
x86_64 Linux (early prototype version)

# Keybindings

`r`: Switch to the red channel
`g`: Switch to the green channel
`b`: Switch to the blue channel
`q`: Quit

# Known issues
Problem: On Windows, sometimes capture input won't display anything
Solution: Need to investigate. Restarting a few times usually fixes it

Problem: Sometimes keyboard input doesn't go through
Solution: Look into moving input to another thread

Problem: Video speed isn't constant
Solution: This isn't meant to be a constant time media player, but more investigation work is needed
