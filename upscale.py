import os
import subprocess
import argparse


# path separator
SEP = os.sep

# i should've been using this a year ago
def parse():
    parser = argparse.ArgumentParser(description="Preserve directory trees when upscaling images with waifu2x")
    parser.add_argument("-i", "--input-dir", help="directory containing input images/dirs", required=True)
    parser.add_argument("-o", "--output-dir", help="directory to generate output images into", required=True)
    parser.add_argument("--ffmpeg-fix",
        help="use ffmpeg to fix bad image bit depth metadata for alpha channel preservation", action="store_true")
    return parser.parse_args()

# def get_cfg():
#     global cfg
#     try:
#         with open('cfg.json') as f:
#             cfg = json.load(f)
#     except FileNotFoundError:
#         cfg = {}
#         cfg['WAIFU']      = input("drag&drop (no quotes!) waifu2x-ncnn-vulkan executable: ")
#         cfg['INPUT_DIR']  = input("drag&drop (no quotes!) input folder: ")
#         cfg['OUTPUT_DIR'] = input("drag&drop (no quotes!) output folder: ")
#         cfg['FFMPEG']     = input("drag&drop (no quotes!) ffmpeg executable: ")
#         with open('cfg.json','w+') as f:
#             json.dump(cfg, f)


def build_cmd(input, output, args):
    return [cfg['WAIFU'], '-i', input, '-o', output] + [elem for elem in opts]

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
    get_cfg()
    main()
