# Encode sequentually numbered (i.e 0.tiff, 1.tiff) into lossless 8-bit H264 file in MKV container
ffmpeg -r 30 -i %d.tiff -vcodec libx264rgb -qp 0 -pix_fmt rgb24 -color_range 2 out-h264-full.mkv
