#!/usr/bin/python
from os import path
from matplotlib import pyplot as plt
import csv
import argparse
import sys
import json


def main(args):
    if (not args.splitCsv and not args.showChart):
        print 'No option selected. Use the -h flag to see a help message'
        sys.exit(1)
    # select webgl function to track (WTF only)
    WEBGL_FUNCTION = 'WebGLRenderingContext#'
    if (not args.function or not len(args.function)):
        WEBGL_FUNCTION += 'bindBuffer'
    else:
        WEBGL_FUNCTION += args.function
    print 'Looking for "{}"'.format(args.function)
    # get csv file path
    filePath = path.abspath(args.file)
    # check file exixts
    if (not path.isfile(filePath)):
        print 'File {} not found'.format(filePath)
        return
    if (args.splitCsv):
        split_csv(filePath, WEBGL_FUNCTION)
    if (args.showChart):
        show_chart(filePath, WEBGL_FUNCTION)


def show_chart(file, functionName):
    print 'Reading from {}'.format(file)
    _, ext = path.splitext(file)
    if (ext == '.csv'):
        display_from_csv(file, functionName)
    elif (ext == '.json'):
        # remove 1st part of function name, use plain cli argument
        display_from_json(file, functionName.split('#')[1])
    else:
        print 'File extension not supported'
        return


def show_bar_chart(xlist, ylist, functionName):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('"{}" elapsed times'.format(functionName))
    ax.set_xlabel('time from application startup (ms)')
    ax.set_ylabel('time from previous call (ms)')
    ax.bar(xlist, ylist)
    plt.show()


def display_from_json(file, functionName):
    with open(file, 'rb') as jsonfilein:
        timestamps = []  # the X axes
        tdurations = []  # the Y axes
        data = json.load(jsonfilein)

        for key, events in data.iteritems():
            for e in events:
                if type(e) is dict:
                    name = e.get('name', '')
                    if (name == functionName):
                        # thread clock duration for the operation
                        tdurations.append(e.get('tdur', 0))
                        # tracing clock timestamp of the event
                        timestamps.append(e.get('ts', 0))
        assert len(timestamps) == len(tdurations)
        show_bar_chart(timestamps, tdurations, functionName)


def display_from_csv(file, functionName):
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
        assert len(arrivalTimes) == len(elapsedTimes)
        show_bar_chart(arrivalTimes, elapsedTimes, functionName.split('#')[1])


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
