'''
Id:          "$Id$"
Copyright:   Copyright (c) 2015 Bank of America Merrill Lynch, All Rights Reserved
Description:
Test:
'''

'''
Created on Oct 14, 2010
@author: Peter Harrington
'''
import matplotlib.pyplot as plt


class plotDecisionTree(object):

    def __init__(self):
        #self.intree = inTree
        self.ax1 = None
        self.totalW = 0
        self.totalD = 0
        self.xOff = 0
        self.decisionNode = dict(boxstyle="sawtooth", fc="0.8")
        self.leafNode = dict(boxstyle="round4", fc="0.8")
        self.arrow_args = dict(arrowstyle="<-")

    #if you do get a dictonary you know it's a tree, and the first element will be another dict
    def createPlot(self, inTree):
        fig = plt.figure(1, facecolor='white')
        fig.clf()
        axprops = dict(xticks=[], yticks=[])
        self.ax1 = plt.subplot(111, frameon=False, **axprops)    #no ticks
        #self.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
        self.totalW = float(self.getNumLeafs(inTree))
        self.totalD = float(self.getTreeDepth(inTree))
        self.xOff = -0.5/self.totalW;
        self.yOff = 1.0;
        self.plotTree(inTree, (0.5,1.0), '')
        plt.show()


    def plotTree(self, myTree, parentPt, nodeTxt):#if the first key tells you what feat was split on
        numLeafs = self.getNumLeafs(myTree)  #this determines the x width of this tree
        depth = self.getTreeDepth(myTree)
        firstStr = myTree.keys()[0]     #the text label for this node should be this
        cntrPt = (self.xOff + (1.0 + float(numLeafs))/2.0/self.totalW, self.yOff)
        self.plotMidText(cntrPt, parentPt, nodeTxt)
        self.plotNode(firstStr, cntrPt, parentPt, self.decisionNode)
        secondDict = myTree[firstStr]
        self.yOff = self.yOff - 1.0/self.totalD
        for key in secondDict.keys():
            if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
                self.plotTree(secondDict[key],cntrPt,str(key))        #recursion
            else:   #it's a leaf node print the leaf node
                self.xOff = self.xOff + 1.0/self.totalW
                self.plotNode(secondDict[key], (self.xOff, self.yOff), cntrPt, self.leafNode)
                self.plotMidText((self.xOff, self.yOff), cntrPt, str(key))
        self.yOff = self.yOff + 1.0/self.totalD


    def plotNode(self, nodeTxt, centerPt, parentPt, nodeType):
        self.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',
                 xytext=centerPt, textcoords='axes fraction',
                 va="center", ha="center", bbox=nodeType, arrowprops=self.arrow_args )

    def plotMidText(self, cntrPt, parentPt, txtString):
        xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
        yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
        self.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)


    def getNumLeafs(self, myTree):
        numLeafs = 0
        firstStr = myTree.keys()[0]
        secondDict = myTree[firstStr]
        for key in secondDict.keys():
            if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
                numLeafs += self.getNumLeafs(secondDict[key])
            else:   numLeafs +=1
        return numLeafs

    def getTreeDepth(self, myTree):
        maxDepth = 0
        firstStr = myTree.keys()[0]
        secondDict = myTree[firstStr]
        for key in secondDict.keys():
            if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
                thisDepth = 1 + self.getTreeDepth(secondDict[key])
            else:   thisDepth = 1
            if thisDepth > maxDepth: maxDepth = thisDepth
        return maxDepth


#def createPlot():
#    fig = plt.figure(1, facecolor='white')
#    fig.clf()
#    createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
#    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
#    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
#    plt.show()

def retrieveTree(i):
    listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                  ]
    return listOfTrees[i]


def main():
    mytree = retrieveTree(0)
    test = plotDecisionTree()
    test.createPlot(mytree)
