
# fixes incorrect bit depth metadata present in some compressed png images
# waifu2x will prune the alpha layer in these cases; cloning and fixing the input solves the issue
def main(ffmpeg_dir):
    def ffmpeg_alpha_conversion(ffmpeg_dir, i, o):
        return [ffmpeg_dir, '-i', i, '-pix_fmt', 'rgba', o]

    def ffmpeg_fix(input_dir,
                    output_dir, ffmpeg_dir, branch=''):

        for obj in os.scandir(input_dir + branch):
            newbranch = branch + SEP + obj.name
            if obj.is_dir():
                os.makedirs(output_dir + newbranch, exist_ok=True)
                ffmpeg_fix(branch=newbranch, input_dir=input_dir, output_dir=output_dir, ffmpeg_dir=ffmpeg_dir)
            elif obj.is_file():
                subprocess.run(
                    ffmpeg_alpha_conversion(
                        ffmpeg_dir, input_dir + newbranch, output_dir + newbranch
                        )
                    )


if __name__ == '__main__':
    main()