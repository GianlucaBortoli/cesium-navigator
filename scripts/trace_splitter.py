#!/usr/bin/python
from os import path
import csv
import argparse
import sys


BINDBUFFER = 'WebGLRenderingContext#bindBuffer'


def main(args):
    if (not args.splitCsv and not args.showChart):
        print 'No option selected. Use the -h flag to see a help message'
        sys.exit(1)
    if (args.splitCsv):
        split_csv(path.abspath(args.file))
    if (args.showChart):
        show_chart()


def show_chart():
    # TODO: implement me
    pass


def split_csv(file):
    print 'Reading from "{}"\n'.format(file)
    with open(file, 'rb') as csvfilein:
        reader = csv.reader(csvfilein)
        next(reader)  # skip header
        csvChunks = []
        count = 0

        for row in reader:
            csvChunks.append(row)  # save row for later write on file
            startTime = row[0]
            function = row[1]
            if function == BINDBUFFER:
                outFile = '{}-{}.csv'.format(path.splitext(file)[0], count)
                outFolder = path.dirname(file)
                create_csv(path.join(outFolder, outFile), csvChunks[:-1])
                count += 1
                print startTime


def create_csv(file, rows):
    print 'Writing to "{}"'.format(file)
    with open(file, 'wb') as csvfileout:
        writer = csv.writer(csvfileout)
        for r in rows:
            writer.writerow(r)
    print 'Done'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process CSV file from WTF traces.')
    parser.add_argument(
        'file', help='The path to the CSV containing the WTF trace.')
    parser.add_argument(
        '--splitCsv', action='store_true',
        help='Split input CSV looking for bindBuffer.')
    parser.add_argument(
        '--showChart', action='store_true',
        help='Show the bindBuffer elapsed time chart.')
    main(parser.parse_args())
