import os
import subprocess
import argparse


# path separator
SEP = os.sep
WAIFU_DIR_NAME = "waifu2x-ncnn-vulkan-20210521-windows" + SEP + "waifu2x-ncnn-vulkan.exe"

# i should've been using this a year ago
def parse():
    parser = argparse.ArgumentParser(description="Preserve directory trees when upscaling images with waifu2x")
    parser.add_argument("-i", "--input-dir", help="directory containing input images/dirs", required=True)
    parser.add_argument("-o", "--output-dir", help="directory to generate output images into", required=True)
    parser.add_argument("-w", "--waifu-loc", help="override default waifu2x executable location")
    parser.add_argument("-f", "--ffmpeg-fix",
        help="provide ffmpeg location to fix bad image bit depth metadata for alpha channel preservation")
    return parser.parse_args()


def build_cmd(args):
    v = vars(args)
    if "w" in v:
        cmd = v["w"]
    else:
        cmd = [WAIFU_DIR_NAME]
    if "f" in v:
        import ffmpeg_fix

    cmd = ["waifu2x-ncnn-vulkan-20210521-windows/waifu2x-ncnn-vulkan.exe", "-i", args.i, "-o", args.o]

def main(*opts):
    # this recursive function does the upscaling with build_cmd
    def recur(branch='', input_dir=cfg['INPUT_DIR'], output_dir=cfg['OUTPUT_DIR']):
        for obj in os.scandir(input_dir + branch):
            newbranch = branch + SEP + obj.name
            # TODO? untested for symlinks
            if obj.is_dir():
                os.makedirs(output_dir + newbranch, exist_ok=True)
                recur(branch=newbranch, input_dir=input_dir, output_dir=output_dir)
            elif obj.is_file():
                subprocess.run(
                    build_cmd(
                        input_dir + newbranch, output_dir + newbranch, *opts
                        )
                    )


if __name__ == '__main__':
    # get_cfg()
    main()
