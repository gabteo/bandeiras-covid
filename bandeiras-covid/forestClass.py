import treeClass
from generateDataSamples import generateDataSamples
from statistics import mode
from leafNode import leafNode
import csv
import matplotlib.pyplot as plt



class forestClass:
    def __init__(self, forestSize = 11, treesDepth = 6, trainGrouping = 0.4, trainSetSize = 150, printForestFlag = False) -> None:
        self.forest = []
        self.forestSize = forestSize
        self.treesDepth = treesDepth
        trainingDataList = getTrainList(trainGrouping, forestSize, trainSetSize)
        #obter dados de treinamento

        for i in range(forestSize):
            self.forest.append(treeClass.treeClass(trainingDataList[i], maxDepth = treesDepth, nodeDepth=-1))
            if printForestFlag:
                printTree(self.forest[i].treeNode)
                print("")

        #testar
        
           
    def forestTest(self, testData):
        testedRows = 0
        rightGuessedRows = 0

        indexYellow = 0
        indexOrange = 1
        indexRed = 2

        for testRow in testData:
            testedTrees = 0
            testedRows += 1

            classeOriginal = ""
            if testRow[-1] == "1":
                classeOriginal = "amarela (1)"
            elif testRow[-1] == "2":
                classeOriginal = "laranja (2)"
            elif testRow[-1] == "3":
                classeOriginal = "vermelha (3)"
                
            originalFlagValue = int(testRow[-1])
            if printForestGuesses:
                print("")
            #print(testRow, testRow[-1], originalFlagValue)
            guess = []
            for i in range(self.forestSize):
                previsao = classifyRow(testRow, self.forest[i].treeNode)

                #tipos = [type(k) for k in previsao.keys()]
                #print(tipos, previsao.keys())
                #print(previsao["1"], previsao["2"], previsao["3"])
                quantidade = [0, 0, 0]

                if 1 in previsao:
                    quantidade[indexYellow] = previsao[1]
                if 2 in previsao:
                    quantidade[indexOrange] = previsao[2]
                if 3 in previsao:
                    quantidade[indexRed] = previsao[3]
                testedTrees += 1
                #print(quantidade)

                guess.append(quantidade.index(max(quantidade))+1)   # add o cod da flag 1, 2, 3
            
            rowFinalGuess = mode(guess)
            if printForestGuesses:
                print("chutou " + str(guess) + ", portanto " + str(rowFinalGuess))
                print("era " + str(originalFlagValue))
            # certezaPalpite = ocorrencias(palpite)/palpitesDados
            # nao calculado por performance
            if rowFinalGuess == originalFlagValue:
                rightGuessedRows += 1

        print("\nQuantidade de dados testados: " + str(testedRows))
        overallSuccess = round((float(rightGuessedRows)*100/testedRows), 2)

        print("Overall success da floresta: " + str(overallSuccess)+"%")

        return overallSuccess



def getTrainList(trainGrouping, forestSize, trainSetSize = 300):
    generateData = generateDataSamples()
    yellow = generateData.getYellowData(trainGrouping, forestSize, trainSetSize)
    # yellow é uma lista, e
    # cada item de yellow é um conjunto para treinamento de uma tree
    orange = generateData.getOrangeData(trainGrouping, forestSize, trainSetSize)
    red = generateData.getRedData(trainGrouping, forestSize, trainSetSize)
    
    #print("conj de conj amarelo")
    #print(yellow)
    #for item in range(len(yellow)):
        #print(yellow[item]) # imprime cada conjunto de treinamento

    samples = []    # sera uma lista de treinamento, de 3 bandeiras cada
    # [[listra123T1], [lista123T2]....]

    for tree in range(forestSize):
        samplesTemp = []
        # add os elementos de uma sublista de yellow em uma sublista mista de samplesTemp
        for i in range(len(yellow[tree])):    # range(trainSetSize)?
            samplesTemp.append(yellow[tree][i])    
            samplesTemp.append(orange[tree][i])    #[i]?
            samplesTemp.append(red[tree][i])

        # finalmente, adiciona a sublista mista em samples
        samples.append(samplesTemp)

    # cada sublista de samples serve para treinar uma árvore
    #print(samples)  #ok ate aqui
    return samples
                
                


def classifyRow(testRow, node):
    if isinstance(node, leafNode):
        return node.leafData

    if node.criteria.isSatisfied(testRow):
        return classifyRow(testRow, node.satisfied)
    else:
        return classifyRow(testRow, node.notSatisfied)

def printTree(node, tab=0):
        
    if isinstance(node, leafNode):
        print("| "*(tab-1) + "Bandeira ", node.leafData)
        return
    # imprime o critério
    print("| "*(tab-1) + str(node.criteria))
    
    # imprime subarvore direita
    print("| "*(tab-1) + "|Sim ->")
    printTree(node.satisfied, tab+2)
    # imprime subarvore esquerda
    print("| "*(tab-1) + "|Nao ->")
    printTree(node.notSatisfied, tab+2)
    


######  ABRE DADOS DE TESTE  #######    
testingFile = open("rawTestingData.csv", "r")
    #headerFile = open("decision-trees\\bandeirasHeader.csv", "r")
with testingFile as csv_file:
    csv.excel.skipinitialspace = True
    csv_reader = csv.reader(csv_file, delimiter=",", quoting = csv.QUOTE_NONE, quotechar="\"", dialect='excel')

    rows = [[float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), row[9]] for row in csv_reader if row]
    samples = []
    for row in rows:
        #samples.append([row[0], row[1][0], row[2]])
        samples.append(row)
    #print(samples)
testSamples = samples
#random.shuffle(samples)

maxForestSize = 15
forestTreesDepth = 4
trainGrouping = 0.40
trainSetSize = 3000
printForestFlag = False
printForestGuesses = False
forestSuccess = [0]

for z in range(1, maxForestSize+1):
    floresta = forestClass(z, forestTreesDepth, trainGrouping, trainSetSize, printForestFlag)

    forestSuccess.append(floresta.forestTest(testSamples))


plt.close()
xInt = range(0, maxForestSize+1)
xData = []
for i in range(maxForestSize+1):
    xData.append(i)

plt.xticks(xInt)
plt.yticks(range(0, 100, 5))
plt.title("Acerto vs tam. da Floresta")
plt.xlabel('Tamanho da floresta')
plt.ylabel('Acerto [%]')
plt.plot(xData,forestSuccess)
plt.ylim([0, 100])
plt.xlim([0, 15])
plt.grid()
#plt.clf()
plt.savefig("forestPlots\\acertoVsSize_D"+ str(forestTreesDepth)+"_G"+ str(int(trainGrouping*100)) +".jpg")
plt.show()