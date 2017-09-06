#!/usr/bin/python
from os import path
from lib import wtf
from lib import display
import argparse
import sys


def main(args):
    if (not args.splitCsv and
            not args.showChart and
            not args.groupChart):
        print 'No option selected. Use the -h flag to see a help message'
        sys.exit(1)
    # select webgl function to track (WTF only)
    WEBGL_FUNCTION = 'WebGLRenderingContext#'
    if (not args.function or not len(args.function)):
        WEBGL_FUNCTION += 'bindBuffer'
    else:
        WEBGL_FUNCTION += args.function
    if (args.splitCsv or args.showChart):
        print 'Looking for "{}"'.format(args.function)
    # get csv file path
    filePath = path.abspath(args.file)
    # check file exixts
    if (not path.isfile(filePath)):
        print 'File {} not found'.format(filePath)
        return
    if (args.splitCsv):
        wtf.split_csv(filePath, WEBGL_FUNCTION)
    if (args.showChart):
        display.show_chart(filePath, WEBGL_FUNCTION)
    if (args.groupChart):
        display.display_stacked_bars_groups(filePath, WEBGL_FUNCTION)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process CSV file from exported from WTF traces.')
    parser.add_argument(
        'file', help='The path to the CSV containing the exported WTF trace')
    parser.add_argument(
        '--splitCsv', action='store_true',
        help='Split input CSV looking for bindBuffer')
    parser.add_argument(
        '--showChart', action='store_true',
        help='Show the bindBuffer elapsed time chart')
    parser.add_argument(
        '--groupChart', action='store_true',
        help='Show the stacked bar chart for different groups')
    parser.add_argument(
        '--function', help='The name of the WebGL function call to track')
    main(parser.parse_args())
