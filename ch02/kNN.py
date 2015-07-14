#!/usr/bin/python3

from numpy import *
import operator
import os
import random

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
    return sortedClassCount[0][0]

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

def autoNorm(dataSet):              # m x n
    m = dataSet.shape[0]
    minVals = dataSet.min(0)        # 1 x n
    maxVals = dataSet.max(0)        # 1 x n
    ranges = maxVals - minVals      # 1 x n
    normDataset = zeros(dataSet.shape)      # m x n
    normDataset = dataSet - tile(minVals, (m,1))
    normDataset = normDataset / tile(ranges, (m,1))
    return normDataset, ranges, minVals

def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, : ], \
                normMat[numTestVecs:m, : ], \
                datingLabels[numTestVecs:m], \
                3)
        print('the classifier came back with: %d, the real answer is: %d ' \
                % (classifierResult, datingLabels[i]) )
        if(classifierResult != datingLabels[i]):
            errorCount += 1.0
    print('the total error rate is: %f ' % (errorCount/numTestVecs) )

def classifyPersion():
    k = 3 # param k for kNN
    resultList = ['not at all', 'in small dose', 'in large dose']
    ffMiles = float(input('frequent flier miles earned per year? '))
    percentTats = float(input('percentage of time playing video games? '))
    iceCream = float(input('liters of ice cream consumed per year? '))
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([percentTats, ffMiles, iceCream])
    classifierResult = classify0((inArr - minVals)/ranges, normMat, datingLabels, k)
    print('You will probably like this person: %s' % resultList[classifierResult - 1] )
            
def img2vector(filename):
    returnVect = zeros( (1, 1024) )
    with open(filename) as fr:
        for i in range(32):
            lineStr = fr.readline()
            for j in range(32):
                returnVect[0, 32*i+j] = int(lineStr[j])
    return returnVect

def handwritingClassTest():
    k = 3 # param k for kNN
    hwLabels = []
    trainingFileList = os.listdir('trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros( (m, 1024) )
    for i in range(m):
        # '<digit>_<sampleID>.txt'
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNum = int(fileStr.split('_')[0])
        hwLabels.append(classNum)
        trainingMat[i, : ] = img2vector('trainingDigits/%s' % fileNameStr)

    errorCount = 0.0
    testFileList = os.listdir('testDigits')
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNum = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, k)
        print("the classifier came back with: %d, the real answer is: %d" \
                % (classifierResult, classNum) )
        if (classifierResult != classNum):
            errorCount += 1.0
    print("the total number of errors is: %d" % errorCount)
    print("the total error rate is: %f" % (errorCount/mTest) )
        




        



