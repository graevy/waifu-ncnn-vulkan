import os
import subprocess
import PIL.Image

import cfg


# path separator
SEP = os.sep

# TODO json persistence
def get_dirs():
    try:
        PROGRAM_DIR = cfg.PROGRAM_DIR
    except:
        PROGRAM_DIR = input("drag&drop waifu2x executable: ")
    try:
        INPUT_DIR = cfg.INPUT_DIR
    except:
        INPUT_DIR = input("drag&drop input folder")
    try:
        OUTPUT_DIR = cfg.OUTPUT_DIR
    except:
        OUTPUT_DIR = input("drag&drop output folder")


def build_cmd(input, output, *opts: str):
    return [cfg.PROGRAM_DIR, '-i', input, '-o', output] + [elem for elem in opts]

def main(*opts):
    def recur(branch=''):
        for obj in os.scandir(cfg.INPUT_DIR + branch):
            newbranch = branch + SEP + obj.name
            # untested for symlinks
            if obj.is_dir():
                os.makedirs(cfg.OUTPUT_DIR + newbranch, exist_ok=True)
                recur(branch=newbranch)
            elif obj.is_file():
                subprocess.run(
                    build_cmd(
                        cfg.INPUT_DIR + newbranch, cfg.OUTPUT_DIR + newbranch, *opts
                        )
                    )
    recur()


if __name__ == '__main__':
    main()