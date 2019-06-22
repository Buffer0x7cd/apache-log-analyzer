from dateutil.parser import parse
from datetime import datetime
import sys
from collections import defaultdict
from typing import Dict, List
import argparse

CODE_START = 500
CODE_END = 600

def strToDate(timestampString: str) -> datetime:
    timestamp = parse(timestampString[:11] + " " + timestampString[12:])
    return timestamp
 
def processString(line: str)-> datetime:
    line =  line.split(" ")
    timestampString =  line[3] + " " + line[4]
    timestampString  = timestampString[1:-1]
    return strToDate(timestampString)



def findPosition(file, startTime: datetime)->int:
    ''' Find the starting offset in a file by comparing timestamps using binary'''
    file.seek(0, 2)
    size = file.tell()
    if size <= 0:
        return 0
    low, high, mid = 0, size - 1, 1
    while low < high:
        mid = (low + high) >> 1
        if mid > 0:
            file.seek(mid - 1)
            file.readline()
            midf = file.tell()
        else:
            midf = 0
            file.seek(midf)
        line = file.readline()

        if not line or startTime <= processString(line):
            high = mid
        else:
            low = mid + 1
    if mid == low:
        return midf
    if low <= 0:
        return 0
    file.seek(low - 1)
    file.readline()
    return file.tell()


def main(startTime: str, endTime: str, fileList: List):
    startTime = strToDate(startTime)
    endTime = strToDate(endTime)
    totalResponse = 0
    responseBuffer = defaultdict(int)
    for fileName in fileList:
        with open(fileName, 'r') as file:
            fileOffset = findPosition(file, startTime)
            file.seek(fileOffset)
            for line in file:
                if endTime  > processString(line):
                    totalResponse += 1
                    line = line.split(" ")
                    ip = line[0]
                    currentResponse = line[8]
                    if int(currentResponse) in range(CODE_START, CODE_END):
                        responseBuffer[ip] += 1
                else:
                    break
    print("Between time {} and time {}".format(startTime, endTime))
    printStatstics(responseBuffer, totalResponse)


def printStatstics(responseBuffer: Dict, totalResponse: int):
    if not responseBuffer.keys():
        print(" No 5xx errors were found")
    else:
        for ip in responseBuffer.keys():
            errors = responseBuffer[ip]/totalResponse * 100
            print("{} got {:0.4f}% 5XX errors".format(ip,errors))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process logs file based on given timestamps")
    parser.add_argument("starttime", help="The starting timestamp to be used for filtering logs", metavar="startTime")
    parser.add_argument("endtime", help="The ending timestamp to be used for filtering logs", metavar="endTime")
    parser.add_argument("files", nargs="+", help="list of  files contaning the log data")
    args = parser.parse_args()
    startTime = args.starttime
    endTime = args.endtime
    fileList = args.files
    main(startTime, endTime, fileList)