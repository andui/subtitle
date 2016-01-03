import os
from datetime import datetime
import re
import pysrt

# parse time string to datetime object with given format, eg. timeStr =
# '16:31:32.123'
def str2Dt(timeStr):
    return datetime.strptime(timeStr, '%H:%M:%S,%f')

# parse datetime object to time string with given format


def dt2Str(dateTime):
    return dateTime.strftime('%H:%M:%S,%f')[:-3]


def shift(part, delta, factor):
    part.shift(hours=delta.hour * factor)
    part.shift(minutes=delta.minute * factor)
    part.shift(seconds=delta.second * factor)
    part.shift(milliseconds=delta.microsecond / 1000 * factor)

def main(srtFile, cutFile, folder):
    dest =srtFile[:-4] + "_cut.srt"
    # read from the cut file to get a list of [start, end]
    start = []
    end = []

    lines = [line.rstrip('\n') for line in open(folder+cutFile)]
    pattern = re.compile("^(\d+\.)")
    lineNum = 0
    for line in lines:
        lineNum += 1
        strs = line.split()
        # get the diff
        if lineNum == 2:
            factor = 1 if strs[1] == '+' else -1
            diff = str2Dt(strs[2])
        elif pattern.match(line):
            # need to adjust this with the offset?
            start.append(str2Dt(strs[1]))
            end.append(str2Dt(strs[2]))

    # now read the srt file and out put the cutSrt
    subs = pysrt.open(folder+srtFile)
    res = subs

    for i in range(len(start)):
        # print i
        part = subs.slice(
            starts_after={'hours': start[i].hour, 'minutes': start[i].minute, 'seconds': start[
                i].second, 'milliseconds': start[i].microsecond / 1000},
            ends_before={'hours': end[i].hour, 'minutes': end[i].minute, 'seconds': end[i].second, 'milliseconds': end[i].microsecond / 1000})

        if i == 0:
            delta = start[i]
            shift(part, delta, -1)
            res = part
        else:
            delta += start[i] - end[i - 1]
            shift(part, delta, -1)
            res.extend(part)

    # adjust according to the diff between original video and srt
    shift(res, diff, factor)

    # #remove srtFile and cutFile
    # os.remove(folder + srtFile)
    # os.remove(folder + cutFile)
    res.save(folder + dest, encoding='utf-8')
    return dest
