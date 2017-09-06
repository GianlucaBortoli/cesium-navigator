#!/usr/bin/python
# Web Tracing Framework exports CSV files
from os import path
import csv


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
