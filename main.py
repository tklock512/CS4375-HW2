from os import lseek
import sys



#class that connects the name of a variable, the column it belongs to for the data and its probability given its class
class variable:
    def __init__(self, name, column):
        self.name = name
        self.column = column
        self.negative0 = 0 #number of  0 given class is 0, changes to probability once completed
        self.negative1 = 0 #number of  1 given class is 0, changes to probability once completed
        self.positive0 = 0 #number of  0 given class is 1, changes to probability once completed
        self.positive1 = 0 #number of  1 given class is 1, changes to probability once completed

#start of main
if len(sys.argv) != 3:
    print("Error: requires exactly two arguments: first the training data, the second the test data")
    sys.exit(1) 

numColumns = 0
columns = []
trainDataArray = []
class0 = 0
class1 = 0

with open(sys.argv[1], 'r') as trainData:
    extractTrainData = trainData.readlines()
    classes = extractTrainData[0].split()
    for x in classes[:-1]:
        v = variable(x, numColumns)
        columns.append(v)
        numColumns+=1 
    for indvLine in extractTrainData[1:]:
        splitLine = indvLine.split()
        intArray = [int(numString) for numString in splitLine]
        trainDataArray.append(intArray)

#get probabilities for each variable
for d in trainDataArray:
    cls = d[-1]
    if cls == 0:
        class0+=1
    if cls == 1:
        class1+=1
    for v in columns:
        varNum = d[v.column]
        if cls == 0:
            if varNum == 0:
                v.negative0+=1
            if varNum == 1:
                v.negative1+=1
        if cls == 1:
            if varNum == 0:
                v.positive0+=1
            if varNum == 1:
                v.positive1+=1

for v in columns:
    v.negative0 = v.negative0/class0
    v.negative1 = v.negative1/class0
    v.positive0 = v.positive0/class1
    v.positive1 = v.positive1/class1

prob0 = class0/len(trainDataArray)
prob1 = class1/len(trainDataArray)
#print tree
print("P(class=0)=" + str(round(prob0, 2)), end=" ")
for v in columns:
    print("P(" + v.name + "=0|0)=" + str(round(v.negative0,2)), end = " ")
    print("P(" + v.name + "=1|0)=" + str(round(v.negative1,2)), end = " ")

print()

print("P(class=1)=" + str(round(prob1, 2)), end=" ")
for v in columns:
    print("P(" + v.name + "=0|1)=" + str(round(v.positive0,2)), end = " ")
    print("P(" + v.name + "=1|1)=" + str(round(v.positive1,2)), end = " ")

print()
print()

#test against training data
trainCorrect = 0

for d in trainDataArray:
    chance0 = prob0
    chance1 = prob1
    correct = d[-1]
    for v in columns:
        varNum = d[v.column]
        if varNum == 0:
            chance0 = chance0*v.negative0
            chance1 = chance1*v.positive0
        if varNum == 1:
            chance0 = chance0*v.negative1
            chance1 = chance1*v.positive1
    if chance0 > chance1:
        if correct == 0:
            trainCorrect+=1
    else:
        if correct == 1:
            trainCorrect+=1



print("Accuracy on training set(" + str(len(trainDataArray)) + " instances) " + str(round(100*trainCorrect/len(trainDataArray), 2)) + "%")

#test against testing data
numTestColumns = 0
testColumns = []
testDataArray = []


with open(sys.argv[2], 'r') as testData:
    extractTestData = testData.readlines()
    testClasses = extractTestData[0].split()
    if len(testClasses) != len(classes):
        print("Error: Test file has a different number of columns as the Train file")
        sys.exit(2)
    for y in testClasses[:-1]:
        v = variable(y, numTestColumns)
        testColumns.append(v)
        numTestColumns+=1
    for indvLine in  extractTestData[1:]:
        spltLine = indvLine.split()
        intrray = [int(numString) for numString in spltLine]
        testDataArray.append(intrray)

testCorrect = 0
for d in testDataArray:
    chance0 = prob0
    chance1 = prob1
    correct = d[-1]
    for v in columns:
        varNum = d[v.column]
        if varNum == 0:
            chance0 = chance0*v.negative0
            chance1 = chance1*v.positive0
        if varNum == 1:
            chance0 = chance0*v.negative1
            chance1 = chance1*v.positive1
    if chance0 > chance1:
        if correct == 0:
            testCorrect+=1
    else:
        if correct == 1:
            testCorrect+=1

print("Accuracy on testing set(" + str(len(testDataArray)) + " instances) " + str(round(100*testCorrect/len(testDataArray), 2)) + "%")