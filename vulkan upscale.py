import os
import subprocess
import PIL


# PROGRAM_DIR = r"C:\Users\p\Downloads\waifu2x-ncnn-vulkan-20210521-windows\waifu2x-ncnn-vulkan.exe"
# INPUT_DIR = r"C:\Users\p\Documents\p design\STS BG\beta arts\Beta Art"
# OUTPUT_DIR = r"C:\Users\p\Documents\p design\STS BG\beta arts\upscales\waifu"



def build_cmd(input, output, *opts: str):
    return [PROGRAM_DIR, '-i', input, '-o', output, opts]

def main():
    splitlen = len(INPUT_DIR.split(os.sep))
    for root, dirs, files in os.walk(INPUT_DIR):
        for d in dirs:
            # the supplied root from os.walk is problematic. it represents the input dir's root.
            # to preserve the directory tree, we care about the structure after root
            # if input is /home/guido/Downloads and output is /etc/new_program,
            # for /home/guido/Downloads/blue/red/green.png, we care about /blue/red/green.png
            # to remove /home/guido/Downloads/, remove the first 3, len(input.split(os.sep)),
            # preserving the rest of the dir structure to os.sep.join with
            newroot = root + os.sep + dd
            outroot = OUTPUT_DIR + os.sep + os.sep.join(newroot.split(os.sep)[splitlen:])
            # print('newrddoot:', newroot, '\n', 'outroot:', outroot)
            os.makedirs(outroot)
            subprocess.run(build_cmd(newroot, outroot))
        
        for f in files:
            newroot = root + os.sep + f
            outroot = OUTPUT_DIR + os.sep + os.sep.join(newroot.split(os.sep)[splitlen:]) + os.sep
            img = PIL.Image.open(f)
            if img.mode == "L" or img.mode == "P":
                # Converts to 32 bit and overwrites the original image.
                # Use a different filename from the original if you want to preserve the original image
                img.convert("RGBA").save(f)


if __name__ == '__main__':
    main()