import sys
from dateutil.parser import parse
from collections import defaultdict

def dateFilter(startTime, endTime, currentTime):
    return currentTime >= startTime and currentTime < endTime

def convertStringToDate(timeString):
    timestring = timeString[:11]+ " "+ timeString[12:]
    res = parse(timestring)
    return res

def filter(line, startTime, endTime):
    response_code = line[8]
    error_code = ["300", "301", "302", "303", "304", "305"]
    startTime = convertStringToDate(startTime)
    endTime = convertStringToDate(endTime)
    currentTime = line[3]+" "+line[4]
    currentTime = convertStringToDate(currentTime[1:-1])
    return dateFilter(startTime, endTime, currentTime) and response_code in error_code

def main(startTime, endTime):
    recordBuffer = defaultdict(int)
    bufferLength = 0
    with open('logs', 'r') as file:
        for line in file:
            line = line.split(" ")
            IP = line[0]
            bufferLength += 1
            if filter(line, startTime, endTime):
                recordBuffer[IP] += 1
    
    for k in recordBuffer.keys():
        percentile = recordBuffer[k]/bufferLength * 100
        print("{} Has {} Percentage of 3XX Errors".format(k, percentile))

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) < 3:
        print("Enter ./command startTime endTime")
        exit(1)
    startTime = sys.argv[1]
    endTime = sys.argv[2]
    main(startTime, endTime)