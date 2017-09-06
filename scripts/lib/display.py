#!/usr/bin/python
from matplotlib import pyplot as plt
from os import path
from wtf import (INIT, MODIFY, DRAW)
import json
import csv


BAR_WIDTH = 5
RED = '#ff0000'
BLUE = '#0066ff'
GREEN = '#00cc00'


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
    ax.bar(xlist, ylist, BAR_WIDTH)
    plt.show()


def display_stacked_bars_groups(file, functionName):
    with open(file, 'rb') as csvfilein:
        reader = csv.reader(csvfilein)
        next(reader)  # skip header
        firstRound = True
        lastTime = None

        initTimes = modifyTimes = drawTimes = 0

        for row in reader:
            startTime = float(row[0])
            function = row[1].split('#')[1]

            if firstRound:
                lastTime = float(startTime)
                firstRound = False
                continue
            else:
                assert lastTime is not None
                elapsedTime = startTime - lastTime
                lastTime = startTime
                if function in INIT:
                    initTimes += elapsedTime
                elif function in MODIFY:
                    modifyTimes += elapsedTime
                elif function in DRAW:
                    drawTimes += elapsedTime
                # Ignore any other function

        xInd = 0
        initBar = plt.bar(
            xInd, initTimes, BAR_WIDTH,
            color=RED,
        )
        modifyBar = plt.bar(
            xInd, modifyTimes, BAR_WIDTH,
            color=BLUE, bottom=initTimes
        )
        drawBar = plt.bar(
            xInd, drawTimes, BAR_WIDTH,
            color=GREEN, bottom=(initTimes + modifyTimes)
        )
        plt.legend(
            (initBar[0], modifyBar[0], drawBar[0]),
            ('Init', 'Modify', 'Draw')
        )
        plt.show()


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
