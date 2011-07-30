#!/usr/bin/env python

import os
import subprocess

from optparse import OptionParser


def _get_files(path):
    files = []

    try:
        dirlist = os.listdir(path)
    except OSError:
        raise Exception("path %s is not a directory" % path)

    for item in dirlist:
        file = os.path.join(path, item)
        if os.path.isdir(file):
            files = files + _get_files(file)
        elif os.path.isfile(file):
            files.append(file)
    return files


def _encode_video(preset, input_file, output_file):
    if preset == "web":
        # --optimize (optimize for web)
        opt_list = ["HandBrakeCLI",
                    "--optimize",
                    "--encoder x264",
                    "-b 1000",
                    "--width 480",
                    "--height 270",
                    "--crop 0:0:0:0",
                    "--x264opts ref=2:bframes=2:subme=6:mixed-refs=0:weightb=0:8x8dct=0:trellis=0"]
    else:
        opt_list = ["HandBrakeCLI",
                    "--encoder x264",
                    "--quality 0.6",
                    '--deinterlace="1:-1:-1"',
                    "--width 1920",
                    "--height 1080",
                    "--crop 0:0:0:0",
                    "--x264opts ref=2:bframes=2:subme=6:mixed-refs=0:weightb=0:8x8dct=0:trellis=0"]
    opt_list.append("-i %s" % input_file)
    opt_list.append("-o %s" % output_file)
    subprocess.call(" ".join(opt_list), shell=True)


def main():
    parser = OptionParser(usage="usage: %prog source_folder destination_folder")
    parser.add_option("-p", "--preset", default="hq",
                      help="choose between hq and web [default: %default]")
    parser.add_option("-r", action="store_true", dest="replace",
                      help="overwrite output file, if it exists")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        return parser.print_help()

    source_dir = args[0]
    destination_dir = args[1]

    files = _get_files(source_dir)

    try:
        # recursively make directories up until the folder_name
        os.makedirs(destination_dir)
    except OSError:
        # directory already exists
        pass

    for file in files:
        path, filename = os.path.split(file)
        destination_filename = os.path.join(destination_dir, filename)

        if (filename[-4:] == ".MP4" and (
            not os.path.isfile(destination_filename) or options.replace)):
            _encode_video(options.preset, file, destination_filename)
            print "encoded: %s" % destination_filename


if __name__ == "__main__":
    main()
