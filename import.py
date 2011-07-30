#!/usr/bin/env python

import datetime
import os
import shutil

from optparse import OptionParser


def main():
    parser = OptionParser(usage="usage: %prog source_folder destination_folder")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        return parser.print_help()

    source_dir = args[0]
    destination_dir = args[1]

    file_list = os.listdir(source_dir)
    for file_name in file_list:
        if ".MP4" not in file_name:
            continue

        source_file_path = os.path.join(source_dir, file_name)
        time_modified = os.path.getmtime(source_file_path)
        datetime_modified = datetime.datetime.fromtimestamp(time_modified)

        folder_name = datetime_modified.strftime("%Y-%m-%d")
        folder_path = os.path.join(destination_dir, folder_name)

        try:
            # recursively make directories up until the folder_name
            os.makedirs(folder_path)
        except OSError:
            # directory already exists
            pass

        destination_file_path = os.path.join(folder_path, file_name)

        # copy file to destination while preserving its meta data
        shutil.copy2(source_file_path, destination_file_path)
        print "added: %s" % destination_file_path


if __name__ == "__main__":
    main()
