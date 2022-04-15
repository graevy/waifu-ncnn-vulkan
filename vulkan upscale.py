import os
import subprocess
import PIL.Image
import json

import cfg

# path separator
SEP = os.sep
cfg = {}

def get_cfg():
    global cfg
    try:
        with open('cfg.json') as f:
            cfg = json.load(f)
    except FileNotFoundError:
        cfg = {}
        cfg['WAIFU']      = input("drag&drop waifu2x-ncnn-vulkan executable: ")
        cfg['INPUT_DIR']  = input("drag&drop input folder: ")
        cfg['OUTPUT_DIR'] = input("drag&drop output folder: ")
        cfg['FFMPEG']     = input("drag&drop ffmpeg executable: ")
        with open('cfg.json','w+') as f:
            json.dump(cfg, f)


def build_cmd(input, output, *opts: str):
    return [cfg['WAIFU'], '-i', input, '-o', output] + [elem for elem in opts]

def ffmpeg_alpha_conversion(i, o):
    return [cfg['FFMPEG'], '-i', i, '-pix_fmt', 'rgba', o]

def main(*opts):    
    def recur(branch='', input_dir=cfg['INPUT_DIR'], output_dir=cfg['OUTPUT_DIR']):
        for obj in os.scandir(input_dir + branch):
            newbranch = branch + SEP + obj.name
            # untested for symlinks
            if obj.is_dir():
                os.makedirs(output_dir + newbranch, exist_ok=True)
                recur(branch=newbranch, input_dir=input_dir, output_dir=output_dir)
            elif obj.is_file():
                subprocess.run(
                    build_cmd(
                        input_dir + newbranch, output_dir + newbranch, *opts
                        )
                    )

    def ffmpeg_fix(branch='', input_dir=cfg['INPUT_DIR'],
                    output_dir=cfg['OUTPUT_DIR'] + SEP + 'ffmpeg'):

        for obj in os.scandir(input_dir + branch):
            newbranch = branch + SEP + obj.name
            if obj.is_dir():
                os.makedirs(output_dir + newbranch, exist_ok=True)
                ffmpeg_fix(branch=newbranch, input_dir=input_dir, output_dir=output_dir)
            elif obj.is_file():                
                subprocess.run(
                    ffmpeg_alpha_conversion(
                        input_dir + newbranch, output_dir + newbranch
                    )
                )

    ffmpeg_fix()
    recur(input_dir=cfg['INPUT_DIR'])


if __name__ == '__main__':
    get_cfg()
    main()