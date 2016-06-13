from os import walk
from collections import deque
import pickle
from random import shuffle

# Get a list of files to process from a directory
directoryName = "images"
recordList = []
for (directoryPath, directoryNames, fileNames)\
        in walk(directoryName):
    recordList.extend(fileNames)
    break
numberOfRecords = len(recordList)

sortableDeque = deque()
shuffle(recordList)

for element in recordList:
    singleElement = deque([''.join([directoryName, '/', element])])
    sortableDeque.append(singleElement)

emptyElement = deque()
sortableDeque.appendleft(emptyElement)

pickle.dump(sortableDeque, open("sortable.srt", "wb"))
