import numpy as np
import random
from math import floor

class generateDataSamples():
    def __init__(self) -> None:
        self.yellowTrainingIndexes = []
        self.orangeTrainingIndexes = []
        self.redTrainingIndexes = []

        self.yellowTestingIndexes = []
        self.orangeTestingIndexes = []
        self.redTestingIndexes = []
        
        #self.trainingSizeByFlag = 200
        #self.testingSizeByFlag = 10

        self.trainingFlags = np.empty((1, 10), dtype=int, order='C')
        self.testingFlags = np.empty((1, 10), dtype=int, order='C')
        #print(self.trainingFlags)
        
        self.yellow = np.loadtxt("yellowData.csv", dtype=int, delimiter=';')
        self.orange = np.loadtxt("orangeData.csv", dtype=int, delimiter=';')
        self.red = np.loadtxt("redData.csv", dtype=int, delimiter=';')

        

    def singleTreeTrain(self, trainingSizeByFlag):
        self.generateFlagsSample(trainingSizeByFlag, "training")
        self.trainingData = self.getValuesFromFlags(self.trainingFlags)
        self.saveCSV(self.trainingData, "rawTrainingData.csv")

    def singleTreeTest(self, testingSizeByFlag):
        self.generateFlagsSample(testingSizeByFlag, "testing")
        self.testingData = self.getValuesFromFlags(self.testingFlags)
        self.saveCSV(self.testingData, "rawTestingData.csv")
        

    def generateFlagsSample(self, sizeByFlag = 125, sampleType = "training"):

        if sampleType == "training":
            self.trainingFlags = np.delete(self.trainingFlags, 0, axis=0)
            trainSetSize = sizeByFlag
            subsetAtual = []

            #amarela
            if sizeByFlag > self.yellow.shape[0]-1:
                for i in range(self.yellow.shape[0]-1):
                    self.yellowTrainingIndexes.append(i) 
                    self.trainingFlags = np.append(self.trainingFlags, [self.yellow[i]], axis=0)
            else:
                for i in range(sizeByFlag):      
                    #amarelo:
                    randIndex = random.randint(0, self.yellow.shape[0]-1)
                    while randIndex in self.yellowTrainingIndexes:
                        randIndex = random.randint(0, self.yellow.shape[0]-1)

                    
                    toAppend = self.yellow[randIndex]
                    self.yellowTrainingIndexes.append(randIndex) 
                    self.trainingFlags = np.append(self.trainingFlags, [toAppend], axis=0)

           
            """ yellowSetSize = self.yellow.shape[0]-1
            self.yellowTrainingIndexes = []
            
            for i in range(trainSetSize):      
                randIndex = random.randint(0, yellowSetSize)
                while randIndex in self.yellowTrainingIndexes:
                    randIndex = random.randint(0, yellowSetSize)
                self.yellowTrainingIndexes.append(randIndex)
                if len(self.yellowTrainingIndexes) == yellowSetSize:
                    self.yellowTrainingIndexes = []
                toAppend = np.ndarray.tolist(self.getValuesFromFlags(np.array([self.yellow[randIndex]]))[0])
                #dataList.append(toAppend)
                #self.yellowTrainingIndexes.append(randIndex) 
                subsetAtual.append(toAppend)
                self.trainingFlags = np.append(self.trainingFlags, [toAppend], axis=0) """
            




            #laranja
            if sizeByFlag > self.orange.shape[0]-1:
                for i in range(self.orange.shape[0]-1):
                    self.orangeTrainingIndexes.append(i) 
                    self.trainingFlags = np.append(self.trainingFlags, [self.orange[i]], axis=0)
            else:
                for i in range(sizeByFlag):      
                    #laranja:
                    randIndex = random.randint(0, self.orange.shape[0]-1)
                    while randIndex in self.orangeTrainingIndexes:
                        randIndex = random.randint(0, self.orange.shape[0]-1)

                    toAppend = self.orange[randIndex]
                    self.trainingFlags = np.append(self.trainingFlags, [toAppend], axis=0)
                    self.orangeTrainingIndexes.append(randIndex)


            #vermelho
            if sizeByFlag > self.red.shape[0]-1:
                for i in range(self.red.shape[0]-1):
                    self.redTrainingIndexes.append(i) 
                    self.trainingFlags = np.append(self.trainingFlags, [self.red[i]], axis=0)
            else:
                for i in range(sizeByFlag):      
                    #amarelo:
                    randIndex = random.randint(0, self.red.shape[0]-1)
                    while randIndex in self.redTrainingIndexes:
                        randIndex = random.randint(0, self.red.shape[0]-1)

                    toAppend = self.red[randIndex]
                    self.trainingFlags = np.append(self.trainingFlags, [toAppend], axis=0)
                    self.redTrainingIndexes.append(randIndex)

            #print(self.yellowTrainingIndexes)
            #print(self.orangeTrainingIndexes)
            #print(self.redTrainingIndexes)
            #print("treino:\n",self.trainingFlags)
            return self.trainingFlags

        elif sampleType == "testing":   # dados para teste
            self.testingFlags = np.delete(self.testingFlags, 0, axis=0)

            #testingSetSize = sizeByFlag
            subsetAtual = []

            #yellowSetSize = self.yellow.shape[0]-1
            self.yellowTestingIndexes = []
            
            """  for i in range(testingSetSize):      
                randIndex = random.randint(0, yellowSetSize)
                while randIndex in self.yellowTrainingIndexes:
                    randIndex = random.randint(0, yellowSetSize)
                self.yellowTrainingIndexes.append(randIndex)
                if len(self.yellowTrainingIndexes) == yellowSetSize:
                    self.yellowTrainingIndexes = []
                toAppend = np.ndarray.tolist(self.getValuesFromFlags(np.array([self.yellow[randIndex]]))[0])
                #dataList.append(toAppend)
                #self.yellowTrainingIndexes.append(randIndex) 
                subsetAtual.append(toAppend)
                self.testingFlags = np.append(self.testingFlags, [toAppend], axis=0)
            """
            
            for i in range(sizeByFlag):      
                #amarelo:
                randIndex = random.randint(0, self.yellow.shape[0]-1)
                while randIndex in (self.yellowTestingIndexes or self.yellowTrainingIndexes):
                    randIndex = random.randint(0, self.yellow.shape[0]-1)

                
                toAppend = self.yellow[randIndex]
                self.yellowTestingIndexes.append(randIndex) 
                self.testingFlags = np.append(self.testingFlags, [toAppend], axis=0)
            print("teste amarelo ok")
            
            
            for i in range(sizeByFlag):      
                #laranja:
                randIndex = random.randint(0, self.orange.shape[0]-1)
                while randIndex in (self.orangeTestingIndexes or self.orangeTrainingIndexes):
                    randIndex = random.randint(0, self.orange.shape[0]-1)

                toAppend = self.orange[randIndex]
                self.testingFlags = np.append(self.testingFlags, [toAppend], axis=0)
                self.orangeTestingIndexes.append(randIndex)


            for i in range(sizeByFlag):      
                #vermelho:
                randIndex = random.randint(0, self.red.shape[0]-1)
                """ while randIndex in (self.redTestingIndexes or self.redTrainingIndexes):
                    randIndex = random.randint(0, self.red.shape[0]-1) """

                toAppend = self.red[randIndex]
                self.testingFlags = np.append(self.testingFlags, [toAppend], axis=0)
                self.redTestingIndexes.append(randIndex)

            #print(self.yellowTestingIndexes)
            #print(self.orangeTestingIndexes)
            #print(self.redTestingIndexes)
            #print("teste:\n", self.testingFlags)
            return self.testingFlags


    def getYellowData(self, grouping = 1.0, subsets = 1, trainSetSize = 150):
        # trainSetSize é o tamanho de cada subconj de treino
        # subsets é a quantidade de subconj de treino = tamanho da floresta
        dataList = []

        #if grouping == 1.0:
        #    subsets = 1

        yellowSetSize = self.yellow.shape[0]-1
        
        #if trainSetSize > yellowSetSize:
        #    trainSetSize = yellowSetSize
        
        trainSetSize *= grouping
        trainSetSize = floor(trainSetSize)
        """ for i in range(yellowSetSize):
            self.yellowTrainingIndexes.append(i) 
            self.trainingFlags = np.append(self.trainingFlags, [self.yellow[i]], axis=0) """

        for element in range(subsets):            # pra cada subconj de treinamento
            self.yellowTrainingIndexes = []
            subsetAtual = []
            for i in range(trainSetSize):      
                randIndex = random.randint(0, yellowSetSize)
                while randIndex in self.yellowTrainingIndexes:
                    randIndex = random.randint(0, yellowSetSize)
                self.yellowTrainingIndexes.append(randIndex)
                if len(self.yellowTrainingIndexes) == yellowSetSize:
                    self.yellowTrainingIndexes = []
                toAppend = np.ndarray.tolist(self.getValuesFromFlags(np.array([self.yellow[randIndex]]))[0])
                #dataList.append(toAppend)
                #self.yellowTrainingIndexes.append(randIndex) 
                subsetAtual.append(toAppend)
                #self.trainingFlags = np.append(self.trainingFlags, [toAppend], axis=0)
            dataList.append(subsetAtual)
        """ 
        if subsets == 1:
            return [dataList[0]]
        else:
            return dataList """
        #cada item de datalist é um conjunto para treinamento de uma tree
        return dataList

    def getOrangeData(self, grouping = 1.0, subsets = 1, trainSetSize = 150):
        # trainSetSize é o tamanho de cada subconj de treino
        # subsets é a quantidade de subconj de treino = tamanho da floresta
        dataList = []

        #if grouping == 1.0:
        #    subsets = 1

        orangeSetSize = self.orange.shape[0]-1
        
        #if trainSetSize > orangeSetSize:
        #    trainSetSize = orangeSetSize
        
        trainSetSize *= grouping
        trainSetSize = floor(trainSetSize)

        for element in range(subsets):            # pra cada subconj de treinamento
            subsetAtual = []
            self.orangeTrainingIndexes = []
            for i in range(trainSetSize):      
                randIndex = random.randint(0, orangeSetSize)
                while randIndex in self.orangeTrainingIndexes:
                    randIndex = random.randint(0, orangeSetSize)
                if len(self.orangeTrainingIndexes) == orangeSetSize:
                    self.orangeTrainingIndexes = []
                toAppend = np.ndarray.tolist(self.getValuesFromFlags(np.array([self.orange[randIndex]]))[0])
                subsetAtual.append(toAppend)
            dataList.append(subsetAtual)
        return dataList

    def getRedData(self, grouping = 1.0, subsets = 1, trainSetSize = 150):
        # trainSetSize é o tamanho de cada subconj de treino
        # subsets é a quantidade de subconj de treino = tamanho da floresta
        dataList = []

        #if grouping == 1.0:
            #subsets = 1

        redSetSize = self.red.shape[0]-1
        
        #if trainSetSize > redSetSize:
        #    trainSetSize = redSetSize
        
        trainSetSize *= grouping
        trainSetSize = floor(trainSetSize)

        for element in range(subsets):            # pra cada subconj de treinamento
            subsetAtual = []
            self.redTrainingIndexes = []
            for i in range(trainSetSize):      
                randIndex = random.randint(0, redSetSize)
                while randIndex in self.redTrainingIndexes:
                    randIndex = random.randint(0, redSetSize)
                if len(self.redTrainingIndexes) == redSetSize:
                    self.redTrainingIndexes = []
                toAppend = np.ndarray.tolist(self.getValuesFromFlags(np.array([self.red[randIndex]]))[0])
                subsetAtual.append(toAppend)
            dataList.append(subsetAtual)
        return dataList




    def getValuesFromFlags(self, flagsData):
        values = np.empty((1, 10), dtype=int, order='C')
        values = np.delete(values, 0, axis=0)

        rowValues = np.empty(10, dtype=int, order='C')
        """ print(rowValues)
        rowValues[0] = 1
        print(rowValues[0])
        rowValues = np.delete(rowValues, 0, axis=0)
        print(rowValues[0]) """

        for r in range(flagsData.shape[0]): #pra cada linha
            
            # 4 primeiros atributos
            for i in range(4):
                #print(rowValues)
                if flagsData[r][i] == 1:
                    rowValues[i] = int(random.uniform(0.0, 1.0)*100)
                elif flagsData[r][i] == 2:
                    rowValues[i] = int(random.uniform(1.01, 2.0)*100)
                elif flagsData[r][i] == 3:
                    rowValues[i] = int(random.uniform(2.01, 3.0)*100)      # definir intervalo final

            # 5
            if flagsData[r][4] == 1:
                rowValues[4] = int(random.uniform(0.0, 5.0))
            elif flagsData[r][4] == 2:
                rowValues[4] = int(random.uniform(5.01, 15.0))
            elif flagsData[r][4] == 3:
                rowValues[4] = int(random.uniform(15.01, 250.0))      # definir intervalo final

            # 6
            if flagsData[r][5] == 1:
                rowValues[5] = int(random.uniform(0.0, 1.0)*100)
            elif flagsData[r][5] == 2:
                rowValues[5] = int(random.uniform(1.01, 2.5)*100)
            elif flagsData[r][5] == 3:
                rowValues[5] = int(random.uniform(2.5, 10.0)*100)      # definir intervalo final

            # 7
            if flagsData[r][6] == 1:
                rowValues[6] = int(random.randint(55, 150)*100)          # definir intervalo final
            elif flagsData[r][6] == 2:
                rowValues[6] = int(random.randint(28, 54)*100)
            elif flagsData[r][6] == 3:
                rowValues[6] = int(random.randint(0, 27)*100)      

            # 8 e 9
            for i in range(7, 9):
                if flagsData[r][i] == 1:
                    rowValues[i] = int(random.uniform(0.0, 0.90)*100)
                elif flagsData[r][i] == 2:
                    rowValues[i] = int(random.uniform(0.91, 0.95)*100)
                elif flagsData[r][i] == 3:
                    rowValues[i] = int(random.uniform(0.96, 1.0)*100)      # definir intervalo final

            if flagsData[r][9] == 1:
                rowValues[9] = 1          
            elif flagsData[r][9] == 2:
                rowValues[9] = 2
            elif flagsData[r][9] == 3:
                rowValues[9] = 3

            values = np.append(values, [rowValues], axis=0)
        #print(values)
        return values



    def saveCSV(self, data, fileName):
        print("Salvando " + fileName + "...")
        try:
            np.savetxt(fileName, data, delimiter=',', fmt='%d')
        except:
            print("erro ao salvar!")

    def getData(self):
        return [self.trainingData, self.testingData]



def newData(sizeByFlagTrain = 500, sizeByFlagTest = 3000):

    generataData = generateDataSamples()
    generataData.singleTreeTrain(sizeByFlagTrain)
    generataData.singleTreeTest(sizeByFlagTest)
    """    generataData.singleTreeTrain(500)
        generataData.singleTreeTest(3000) """
    """ generataData.singleTreeTrain(1500)
    generataData.singleTreeTest(5000) """

def newTrainData(sizeByFlagTrain = 500):

    generataData = generateDataSamples()
    generataData.singleTreeTrain(sizeByFlagTrain)

def newTestData(sizeByFlagTest = 3000):

    generataData = generateDataSamples()
    generataData.singleTreeTest(sizeByFlagTest)

newData(5000, 3000)