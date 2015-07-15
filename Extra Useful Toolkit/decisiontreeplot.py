
import matplotlib.pyplot as plt

class plotdecisiontree(object):

    def __init__(self):
        self.decisionNode = dict(boxstyle = "sawtooth", fc = '0.8')
        self.leafNode = dict(boxstyle = "round4", fc = '0.8')
        self.arror_args = dict(arrowstyle= "<-")


    def plotNode(self, nodeText, centerPt, parentPt, nodeType):
        createPlot.ax1.annotate(nodeText, xy=parentPt, xycoords = 'axes fraction',
                                xytext= centerPt, textcoords= 'axes fraction',
                                va= 'center', ha='center', bbox=nodeType,
                                arrowprops=arrow_args)

    def createPlot(self, nodelist):
        fig = plt.figure(1,facecolor='white')
        fig.clf()
        createPlot.ax1 = plt.subplot(111, frameon=False)
        for item in nodelist:
            self.plotNode(item[0], item[1], item[2], decisionNode)
            self.plotNode(item[3], item[4], item[5], leafNode)
        plt.show()