#!/usr/bin/python
from matplotlib import pyplot as plt
from os import path
from wtf import (
    INIT, MODIFY, DRAW, split_csv
)
import json
import csv

# Global constants
BAR_WIDTH = 5
RED = '#ff0000'  # init
BLUE = '#0066ff'  # modify
GREEN = '#00cc00'  # draw
GREY = '#adad85'  # other


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
    fig = plt.figure(figsize=(15, 5))
    ax = fig.add_subplot(111)
    ax.set_title('"{}" elapsed times'.format(functionName))
    ax.set_xlabel('Time from application startup (ms)')
    ax.set_ylabel('Time from previous call (ms)')
    ax.bar(xlist, ylist, BAR_WIDTH)
    plt.show()


def display_stacked_bars_groups(file, functionName):
    """
    Cumulative bar chart for the entire trace
    """
    with open(file, 'rb') as csvfilein:
        reader = csv.reader(csvfilein)
        next(reader)  # skip header
        firstRound = True
        lastTime = None

        initTime = modifyTime = drawTime = otherTime = 0

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
                    initTime += elapsedTime
                elif function in MODIFY:
                    modifyTime += elapsedTime
                elif function in DRAW:
                    drawTime += elapsedTime
                else:
                    otherTime += elapsedTime
        xInd = 0
        plt.bar(
            xInd, initTime, BAR_WIDTH,
            color=RED,
        )
        plt.bar(
            xInd, modifyTime, BAR_WIDTH,
            color=BLUE, bottom=initTime
        )
        plt.bar(
            xInd, drawTime, BAR_WIDTH,
            color=GREEN, bottom=(initTime + modifyTime)
        )
        plt.bar(
            xInd, otherTime, BAR_WIDTH,
            color=GREY, bottom=(initTime + modifyTime + drawTime)
        )
        plt.legend(
            ('Init', 'Modify', 'Draw', 'Other')
        )
        plt.ylabel('Cumulative time (ms)')
        plt.show()


def display_stacked_bars_groups_1(file, functionName):
    """
    Similar to display_from_csv, but different colors for each group
    """
    plt.figure(figsize=(15, 5))
    chunks = split_csv(file, functionName, ret=True)

    for chunk in chunks:
        firstRound = True
        lastTime = None
        initTime = modifyTime = drawTime = otherTime = 0

        for row in chunk:
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
                    initTime += elapsedTime
                elif function in MODIFY:
                    modifyTime += elapsedTime
                elif function in DRAW:
                    drawTime += elapsedTime
                else:
                    otherTime += elapsedTime
        # Draw each bar one by one
        plt.bar(
            startTime, initTime, BAR_WIDTH,
            color=RED
        )
        plt.bar(
            startTime, modifyTime, BAR_WIDTH,
            color=BLUE, bottom=initTime
        )
        plt.bar(
            startTime, drawTime, BAR_WIDTH, color=GREEN,
            bottom=(initTime + modifyTime)
        )
        plt.bar(
            startTime, otherTime, BAR_WIDTH, color=GREY,
            bottom=(initTime + modifyTime + drawTime)
        )
    plt.legend(
        ('Init', 'Modify', 'Draw', 'Other')
    )
    plt.xlabel('Time from application startup (ms)')
    plt.ylabel('Time from previous call (ms)')
    plt.title('Grouped "{}" elapsed times'.format(functionName.split('#')[1]))
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
