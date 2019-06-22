from dateutil.parser import parse
from datetime import datetime
import sys
from collections import defaultdict
from typing import Dict


RESPONSE_CODE = ["301", "302", "303", "304", "305"]

def strToDate(timestampString: str) -> datetime:
    timestamp = parse(timestampString[:11] + " " + timestampString[12:])
    return timestamp
 
def processString(line: str)-> datetime:
    line =  line.split(" ")
    timestampString =  line[3] + " " + line[4]
    timestampString  = timestampString[1:-1]
    return strToDate(timestampString)



def findPosition(file, startTime: datetime):
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


def main(startTime: str, endTime: str):
    with open('logs', 'r') as file:
        startTime = strToDate(startTime)
        endTime = strToDate(endTime)
        fileOffset = findPosition(file, startTime)
        file.seek(fileOffset)
        responseBuffer = defaultdict(int)
        totalResponse = 0
        for line in file:
            if endTime  > processString(line):
                totalResponse += 1
                line = line.split(" ")
                ip = line[0]
                currentResponse = line[8]
                if currentResponse in RESPONSE_CODE:
                    responseBuffer[ip] += 1
            else:
                break
        printStatstics(responseBuffer, totalResponse, startTime, endTime)

def printStatstics(responseBuffer: Dict, totalResponse: int, startTime: datetime, endTime: datetime):
    for ip in responseBuffer.keys():
        errors = responseBuffer[ip]/totalResponse * 100
        print("Between time {} and time {}".format(startTime, endTime))
        print("{} got {:0.4f}% 3XX errors".format(ip,errors))

if __name__ == "__main__":
    startTime = sys.argv[1]
    endTime = sys.argv[2]
    main(startTime, endTime)