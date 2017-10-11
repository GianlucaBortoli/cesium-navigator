#!/usr/bin/python
# Google Chrome Event profiiler related functions
import json


def frame_computation_time(file):
    print 'Reading from "{}"'.format(file)
    chunks = []

    with open(file, 'rb') as jsonfile:
        data = json.load(jsonfile)
        for key, events in data.iteritems():
            frameCompTime = []

            for e in events:
                if type(e) is dict:
                    frameCompTime.append(e.get('tdur'))  # us
                    if 'snapshot' in e.get('args'):
                        filteredCompTime = filter(None, frameCompTime)
                        chunks.append(filteredCompTime)
                        frameCompTime = []
    print "{} frames detected".format(len(chunks))
    # sum computation time for each frame
    frameSums = []
    for c in chunks:
        frameSums.append(sum(c))
    assert len(chunks) == len(frameSums)
    # print per-frame computation time to stout
    for s in frameSums:
        print s
