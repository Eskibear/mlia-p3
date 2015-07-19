import matplotlib.pyplot as plt

DECISION_NODE = dict(boxstyle="sawtooth,pad=0.6", fc="0.8")
LEAF_NODE = dict(boxstyle="round4,pad=0.6", fc="0.8")
ARROW_ARGS = dict(arrowstyle="<-", shrinkA=20, shrinkB=20, connectionstyle="arc3")

# First draw a node of <nodeType> in position <centerPt> with content of <nodeTxt> in the box
# Then draw a line from position <parentPt> to position <centerPt> 
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    print('plotNode:{}, {}, {}'.format(centerPt, parentPt, nodeTxt))
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', \
            xytext=centerPt, textcoords='axes fraction', va="center", ha="center", \
            bbox=nodeType, arrowprops=ARROW_ARGS)

# Plot content of <txtString> between position <centerPt> and position <parentPt>
def plotMidText(cntrPt, parentPt, txtString):
    xmid = (parentPt[0] - cntrPt[0])/2.0 + cntrPt[0]
    ymid = (parentPt[1] - cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xmid, ymid, txtString)

# Return number of leafNodes for width calculation
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if(type(secondDict[key]).__name__ == 'dict'):
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

# Return number of layers for depth calculation
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        maxDepth = thisDepth if thisDepth > maxDepth else maxDepth
    return maxDepth

# Recursive procedure to calculate position of subtrees and plot them
def plotTree(myTree, parentPt, nodeTxt):
    print('plotTree:{}, {}'.format(parentPt, nodeTxt))
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]   # content of <myTree> root
    # <cntrPt>: position of <myTree> root
    cntrPt = (plotTree.xOff + (1.0 + numLeafs)/2.0/plotTree.totalW,  plotTree.yOff) 
    plotNode(firstStr, cntrPt, parentPt, DECISION_NODE)
    plotMidText(cntrPt, parentPt, nodeTxt) 
    secondDict = myTree[firstStr]   # set of subtrees 
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD     # update <yOff> for next layer
    for key in secondDict.keys():
    # For each of subtrees, <cntrPt> is the parent position
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW    # update <xOff> on plotting a leaf
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, LEAF_NODE)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD     # restore <yOff> for backtrace

# Entry for creation a plot from a decision tree
# Including initialization of global variables, e.g. <xOff>, <yOff>
# <xOff>: 
#   postion before next plot zone in x-axis, initial value is -1/2W, step is 1/W when leafNode plot
# <yOff>:
#   next plot zone postion in y-axis, initial value is , step is -1/D when depth increases
def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW;
    plotTree.yOff = 1.0;
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()


# test
def retrieveTree(i):
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
            {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
            ]
    return listOfTrees[i]

def createPlotTest():
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    createPlot.ax1 = plt.subplot(111, frameon=False)
    plotNode(U'DECISION_NODE', (0.5, 0.1), (0.1, 0.5), DECISION_NODE)
    plotNode(U'LEAF_NODE', (0.8, 0.1), (0.3, 0.5), LEAF_NODE)
    plt.show()
