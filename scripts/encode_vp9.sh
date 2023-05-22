# one pass encoding based on CRF
ffmpeg -framerate 30 -pattern_type glob -i '*.tiff' -vcodec libvpx-vp9 -pix_fmt rgb24 -color_range 2 -row-mt 1 -crf 32 out-vp9-full.webm

# two pass encoding based on target bitrate
ffmpeg -framerate 30 -i %d.tiff -c:v libvpx-vp9 -b:v 5M -pass 1 -row-mt 1 -an -f null /dev/null && \
ffmpeg -framerate 30 -i %d.tiff -c:v libvpx-vp9 -b:v 5M -pass 2 -row-mt 1 -c:a libopus output.webm
