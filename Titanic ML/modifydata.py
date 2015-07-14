from IPython.core.debugger import Tracer
from sklearn import cluster
import pandas as pd
import IPython
import numpy as np

"""
VARIABLE DESCRIPTIONS:
survival        Survival
                (0 = No; 1 = Yes)
pclass          Passenger Class
                (1 = 1st; 2 = 2nd; 3 = 3rd)
name            Name
sex             Sex
age             Age
sibsp           Number of Siblings/Spouses Aboard
parch           Number of Parents/Children Aboard
ticket          Ticket Number
fare            Passenger Fare
cabin           Cabin
embarked        Port of Embarkation
                (C = Cherbourg; Q = Queenstown; S = Southampton)

SPECIAL NOTES:
Pclass is a proxy for socio-economic status (SES)
 1st ~ Upper; 2nd ~ Middle; 3rd ~ Lower

Age is in Years; Fractional if Age less than One (1)
 If the Age is Estimated, it is in the form xx.5

With respect to the family relation variables (i.e. sibsp and parch)
some relations were ignored.  The following are the definitions used
for sibsp and parch.

Sibling:  Brother, Sister, Stepbrother, or Stepsister of Passenger Aboard Titanic
Spouse:   Husband or Wife of Passenger Aboard Titanic (Mistresses and Fiances Ignored)
Parent:   Mother or Father of Passenger Aboard Titanic
Child:    Son, Daughter, Stepson, or Stepdaughter of Passenger Aboard Titanic

"""



'''
Version 1.0:

Data Clean: using linear regression,
            fill NaN with avg

Data Predict: using random forest

Result:  0.75598
'''



'''
Version 1.1

Data Clean:

Data Predict:

Reduce Dimension: PCA feature 8

Result: 0.74641 not imporved

'''


'''
Version 1.2

Data Clean:

Data Predict: replace random forest with SVM

Reduce Dimension: PCA feature 8

Result: Better! 0.77990

'''


def readandmodifytraindata(filename):
    originaldata = pd.read_csv(filename)

    if 'train' in filename:
        label = originaldata.Survived
    else:
        label = None

    ##############
    ## CLEAN DATA
    ##############

    #Turn all quality data into quantitative
    originaldata.Sex = [ 1 if x == 'male' else 0 for x in originaldata.Sex ]
    originaldata.Embarked = [1 if x == 'S' else 2 if x =='C' else 3 for x in originaldata.Embarked ]
    originaldata.Cabin = [ord(x[0]) - 65 if type(x) == str else x for x in originaldata.Cabin]

    # Forget name right now, age Cabin have some null, need to run regression to fill
    originaldata.Age = runregressiontofillnull('Age',
                                        ['Pclass','Parch','SibSp'],
                                        originaldata)
    originaldata.Cabin = runregressiontofillnull('Cabin',
                                           ['Fare','Parch','SibSp','Embarked'],
                                           originaldata)

    ##################################
    ## return clean dataset and label
    ##################################
    # import ipdb
    # ipdb.set_trace()
    return label, originaldata[
        ['Pclass','Sex','Age','SibSp','Parch','Fare','Cabin','Embarked']]




# Age, Cabin
def runregressiontofillnull(spccolumn, listparatorun, dataFrame):
    from sklearn import linear_model
    linModel = linear_model.LinearRegression(normalize = True)

    indexnotnull = dataFrame[spccolumn].index[dataFrame[spccolumn].notnull()]
    indexnull =  dataFrame[spccolumn].index[dataFrame[spccolumn].isnull()]

    # Good catch is that i find
    # There is null in the test train data
    # Which is not in the spccolumn here
    # So before we run our test, we need to make
    # Sure to replace this data (either call this function again or
    # replace with the mean)
    # Get around with it in this project
    traindata = checksubdataContainsNaN(listparatorun,indexnotnull,dataFrame)
    label = dataFrame[spccolumn][indexnotnull]



    # import ipdb
    # ipdb.set_trace()
    ##Run anaylsis
    linModel.fit(traindata,label)


    # As is the same to check for test train data
    testdata = checksubdataContainsNaN(listparatorun,indexnull,dataFrame)

    dataFrame[spccolumn][indexnull] = linModel.predict(testdata)


    return dataFrame[spccolumn]


def checksubdataContainsNaN(listparatorun,indexrow, dataFrame):

    modifydata = dataFrame[listparatorun].irow(indexrow)
    if any(pd.isnull(modifydata).any()) == True:
        for eachitem in listparatorun:
            dataFrame.loc[indexrow,eachitem] =\
            dataFrame.loc[indexrow,eachitem].fillna(np.mean(
            dataFrame.loc[indexrow,eachitem]
            ))
        modifydata = dataFrame.loc[indexrow,listparatorun]


    return modifydata



def writetoCVSpredict(filename, dataFrame):
    filename = filename + '.csv'
    with open(filename, 'w') as writer:
        writer.write('"PassengerId","Survived"\n')
        count = 891
        for p in dataFrame:
            count += 1
            writer.write(str(count) + ',"' + str(p) + '"\n')

    #Could also use dataframe.to_CSV


if __name__  == '__main__':
    print 'Get Train Data'
    wholeresult = readandmodifytraindata('train.csv')
    trainlabel = wholeresult[0]
    traindata = wholeresult[1] # Exclude the name, passagerID, and Survived as the labe

    print 'Get Test Data'
    testdata = readandmodifytraindata('test.csv')
    testdata = testdata[1]


    print 'Training....'
    from sklearn import ensemble
    from sklearn.svm import SVC
    from sklearn.decomposition import PCA
    pca = PCA(whiten=True)
    pca.fit(traindata)
    traindata = pca.transform(traindata)

    #randomforestmodel = ensemble.RandomForestClassifier()
    #randomforestmodel.fit(traindata, trainlabel)

    svcmodel = SVC()
    svcmodel.fit(traindata, trainlabel)

    print 'Predicting...'
    testdata = pca.transform(testdata)
    testpredictresult = svcmodel.predict(testdata)

    print 'Saving...'
    writetoCVSpredict('testresult_SVM',testpredictresult)

    print 'done'
    previous = pd.read_csv('testresult.csv')
    print 'Score is:', svcmodel.score(testdata,previous.Survived)