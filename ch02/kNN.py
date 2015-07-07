#!/usr/bin/python3

from numpy import *
import operator

def createDataset():
    group = array( [[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]] )
    labels = [ 'A', 'A', 'B', 'B' ]
    return group, labels

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        # classCount[voteIlabel] += 1 if key exist, else set to 0
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted( classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount

def file2matrix(filename):
    # count lines
    with open(filename) as fr:
        for i, l in enumerate(fr):
            pass
        numberOfLines = i+1;
    returnMat = zeros( (numberOfLines, 3) )
    classLabelVector = []
    with open(filename) as fr:
        for i in range(numberOfLines):
            line = fr.readline().strip()
            listFromLine = line.split('\t');
            returnMat[i, :] = listFromLine[0:3]
            # here int() used, so only dataSet2 works due to converted labels
            classLabelVector.append(int(listFromLine[-1]))
    return returnMat, classLabelVector


        
