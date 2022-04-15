import os
import subprocess
import PIL.Image


# PROGRAM_DIR = r"C:\Users\p\Downloads\waifu2x-ncnn-vulkan-20210521-windows\waifu2x-ncnn-vulkan.exe"
# INPUT_DIR = r"C:\Users\p\Documents\p design\STS BG\beta arts\Beta Art"
# OUTPUT_DIR = r"C:\Users\p\Documents\p design\STS BG\beta arts\upscales\waifu"
PROGRAM_DIR = r"C:\Users\a\Documents\code\waifu-ncnn-vulkan\waifu2x-ncnn-vulkan-20210521-windows\waifu2x-ncnn-vulkan.exe"
INPUT_DIR = r"C:\Users\a\Documents\code\waifu-ncnn-vulkan\input"
OUTPUT_DIR = r"C:\Users\a\Documents\code\waifu-ncnn-vulkan\output"

# path separator
SEP = os.sep


def build_cmd(input, output, *opts: str):
    return [PROGRAM_DIR, '-i', input, '-o', output] + [elem for elem in opts]

# def main():
#     # the supplied root from os.walk is problematic. it represents the input dir's root,
#     # to preserve the directory tree, we care about the structure after root
#     # if input is /home/guido/Downloads and output is /etc/new_program,
#     # for /home/guido/Downloads/blue/red/green.png, we care about /blue/red/green.png
#     # to remove /home/guido/Downloads/, remove the first 3, len(input.split(SEP)),
#     # preserving the rest of the dir structure to SEP.join with
#     splitlen = len(INPUT_DIR.split(SEP))
#     for root, dirs, files in os.walk(INPUT_DIR):
#         for d in dirs:
#             newroot = root + SEP + d
#             outroot = OUTPUT_DIR + SEP + SEP.join(newroot.split(SEP)[splitlen:])
#             os.makedirs(outroot, exist_ok=True)
#             # x = build_cmd(newroot,outroot)
#             subprocess.run(build_cmd(newroot, outroot))

#         for f in files:
#             newroot = root + SEP
#             outroot = OUTPUT_DIR + SEP + SEP.join(newroot.split(SEP)[splitlen])
#             os.makedirs(outroot, exist_ok=True)
#             with PIL.Image.open(outroot + f) as img:
#                 if img.mode == "L" or img.mode == "P":
#                     # Converts to 32 bit and overwrites the original image
#                     img.convert("RGBA").save(outroot + f)

def main(*opts):
    def recur(branch=''):
        for obj in os.scandir(INPUT_DIR + branch):
            newbranch = branch + SEP + obj.name
            # untested for symlinks
            if obj.is_dir():
                os.makedirs(OUTPUT_DIR + newbranch, exist_ok=True)
                recur(branch=newbranch)
            elif obj.is_file():
                subprocess.run(
                    build_cmd(
                        INPUT_DIR + newbranch, OUTPUT_DIR + newbranch, *opts
                        )
                    )
    recur()


if __name__ == '__main__':
    main()