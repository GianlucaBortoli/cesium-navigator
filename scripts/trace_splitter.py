#!/usr/bin/python
from os import path
from matplotlib import pyplot as plt
import csv
import argparse
import sys


def main(args):
    if (not args.splitCsv and not args.showChart):
        print 'No option selected. Use the -h flag to see a help message'
        sys.exit(1)
    # select webgl function to track
    WEBGL_FUNCTION = 'WebGLRenderingContext#'
    if (not args.function or not len(args.function)):
        WEBGL_FUNCTION += 'bindBuffer'
    else:
        WEBGL_FUNCTION += args.function
    print 'Looking for "{}"'.format(WEBGL_FUNCTION)
    # get csv file path
    filePath = path.abspath(args.file)
    if (args.splitCsv):
        split_csv(filePath, WEBGL_FUNCTION)
    if (args.showChart):
        show_chart(filePath, WEBGL_FUNCTION)


def show_chart(file, functionName):
    print 'Reading from "{}"\n'.format(file)
    with open(file, 'rb') as csvfilein:
        reader = csv.reader(csvfilein)
        next(reader)  # skip header
        firstRound = True
        lastTime = None
        arrivalTimes = []  # the X axes
        elapsedTimes = []  # the Y axes
        # extract elapsed time between bindBuffer calls
        for row in reader:
            startTime = float(row[0])
            function = row[1]

            if function == functionName:
                if firstRound:
                    lastTime = float(startTime)
                    firstRound = False
                    continue
                else:
                    assert lastTime is not None
                    elapsedTime = startTime - lastTime
                    lastTime = startTime
                    elapsedTimes.append(elapsedTime)
                    arrivalTimes.append(startTime)
        # show bar chart
        assert len(arrivalTimes) == len(elapsedTimes)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('bingBuffer elapsed times')
        ax.set_xlabel('time from application startup (ms)')
        ax.set_ylabel('time from previous call (ms)')
        ax.bar(arrivalTimes, elapsedTimes)
        plt.show()


def split_csv(file, functionName):
    print 'Reading from "{}"\n'.format(file)
    with open(file, 'rb') as csvfilein:
        reader = csv.reader(csvfilein)
        next(reader)  # skip header
        csvChunks = []
        count = 0
        firstRound = True

        for row in reader:
            csvChunks.append(row)  # save row for later write on file
            function = row[1]
            if function == functionName:
                if firstRound:
                    firstRound = False
                    continue  # include 1st bindBuffer in 1st chunk
                outFile = '{}-{}.csv'.format(path.splitext(file)[0], count)
                outFolder = path.dirname(file)
                create_csv(path.join(outFolder, outFile), csvChunks[:-1])
                csvChunks = csvChunks[-1:]
                count += 1
        # salve also the last chunks until EOF
        outFile = '{}-{}.csv'.format(path.splitext(file)[0], count)
        outFolder = path.dirname(file)
        create_csv(path.join(outFolder, outFile), csvChunks)


def create_csv(file, rows):
    print 'Writing to "{}"'.format(file)
    with open(file, 'wb') as csvfileout:
        writer = csv.writer(csvfileout)
        for r in rows:
            writer.writerow(r)
    print 'Done'


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
        '--function', help='The name of the WebGL function call to track')
    main(parser.parse_args())
