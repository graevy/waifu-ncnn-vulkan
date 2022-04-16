# waifu-ncnn-vulkan
preserve directories when upscaling with https://github.com/nihui/waifu2x-ncnn-vulkan in windows

alpha preservation requires ffmpeg

usage inherits flags from ncnn-vulkan e.g. ```upscale.py -s 4``` upscales 4x instead of 2x
input/output dirs are handled interactively, and currently persist between sessions
