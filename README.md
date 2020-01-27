VideoDiff
=========

A program to attempt to test a video source for temporal dithering and other visual artifacts

# License

GPLv2 (see LICENSE)

# Warning

Documentation is incomplete and more work needs to be done

# Requirements

- Python3
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

# Known issues
Problem: Video speed isn't constant

Solution: This isn't meant to be a constant time media player, but more investigation work is needed


Problem: On Windows `--output` doesn't work

Solution: Investigate possible OpenCV library issues. For now use a third party video capture tool such as [VirtualDub](https://www.videohelp.com/software/Virtualdub) with the [Lagarith Lossless codec](https://lags.leetcode.net/codec.html) (recommended)
