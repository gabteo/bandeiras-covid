from treeClass import treeClass
#import forestClass
import generateDataSamples
import csv
from leafNode import leafNode
import random
import matplotlib.pyplot as plt


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


def classifyRow(testRow, node):
    if isinstance(node, leafNode):
        return node.leafData
    
    if node.criteria.isSatisfied(testRow):
        return classifyRow(testRow, node.satisfied)
    else:
        return classifyRow(testRow, node.notSatisfied)

def printLeaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs


###################################
######  INICIO DA EXECUCAO  #######
###################################
if __name__ == '__main__':

    

    #sizeByFlagTrain = [50, 100, 500, 1000, 5000]
    sizeByFlagTrain = [1500]
    sizeByFlagTest = [3000]
    generateDataSamples.newTestData(sizeByFlagTest[0])


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

    #random.shuffle(samples)
    #   for sample in samples:
    #        print(samples[sample], "\n")
    testingDataset = samples

    indexYellow = 0
    indexOrange = 1
    indexRed = 2

    printTests = False
    printTreesBool = True
    depthExec = 5

    
    for y in range(len([0])):
        generateDataSamples.newTrainData(sizeByFlagTrain[y])

        ######  ABRE DADOS DE TREINO  #######    
        trainingFile = open("rawTrainingData.csv", "r")
        #headerFile = open("decision-trees\\bandeirasHeader.csv", "r")
        with trainingFile as csv_file:
            csv.excel.skipinitialspace = True
            csv_reader = csv.reader(csv_file, delimiter=",", quoting = csv.QUOTE_NONE, quotechar="\"", dialect='excel')

            rows = [[float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), row[9]] for row in csv_reader if row]
            samples = []
            for row in rows:
                #samples.append([row[0], row[1][0], row[2]])
                samples.append(row)
            #print(samples)

            #print(samples[0][1][0])
        trainingDataset = samples
        #dataHeader = []

        rightGuessByDepth = []

        for z in range(depthExec):

            ######  CONSTRUCAO DA ÁRVORE  #######      
            trainingTree = treeClass(trainingDataset, maxDepth=z, nodeDepth=-1)

            ######  IMPRESSÃO DA ÁRVORE  #######
            if printTreesBool:
                printTree(trainingTree.treeNode)
            #trainingTree.printTree(trainingTree.treeNode)
            #print_tree(trainingTree.treeNode)

            ######  TESTE DA ÁRVORE ######
            acertos = 0
            testSize = 0


            #print(len(testingDataset), testingDataset)
            for testRow in testingDataset:
                #print(type(row[-1]), row[-1])
                testSize+=1

                classeOriginal = ""
                if testRow[-1] == "1":
                    classeOriginal = "amarela (1)"
                elif testRow[-1] == "2":
                    classeOriginal = "laranja (2)"
                elif testRow[-1] == "3":
                    classeOriginal = "vermelha (3)"
                    
                originalFlagValue = int(testRow[-1])

                previsao = classifyRow(testRow, trainingTree.treeNode)    

                quantidade = [0, 0, 0]
                """ quantidadeAmarela = 0
                quantidadeLaranja = 0
                quantidadeVermelha = 0 """

                if '1' in previsao:
                    quantidade[indexYellow] = previsao['1']
                if '2' in previsao:
                    quantidade[indexOrange] = previsao['2']
                if '3' in previsao:
                    quantidade[indexRed] = previsao['3']

                prob = [0, 0, 0]
                somaOcorrencias = sum(quantidade)
                prob[indexYellow] = quantidade[indexYellow]*100/somaOcorrencias
                prob[indexOrange] = quantidade[indexOrange]*100/somaOcorrencias
                prob[indexRed] = quantidade[indexRed]*100/somaOcorrencias


                wrongFlags = [1, 2, 3]
                wrongFlags.remove(originalFlagValue)

                rightFlag = originalFlagValue-1

                if (prob[rightFlag] > prob[wrongFlags[0]-1]) and (prob[rightFlag] > prob[wrongFlags[1]-1]):
                    acertos += 1

                #print(previsao, type(previsao))
                if printTests:
                    print("")
                    print(prob[indexYellow], "% amarela, ", prob[indexOrange], "% laranja, ", prob[indexRed], "% vermelha.")
                    print("Previu: %s, era: %s" % (printLeaf(previsao), classeOriginal))

            successRate = round((float(acertos)*100/float(testSize)), 2)
            rightGuessByDepth.append(successRate)
                    
            print("\n\nTaxa total de acertos da arvore: " + str(successRate) + "%")

        plt.close()
        #fig = plt.figure(figsize=(10, 10))
        xInt = range(0, depthExec+1)
        xData = []
        for i in range(depthExec):
            xData.append(i)
        plt.xticks(xInt)
        plt.yticks(range(0, 100, 5))
        plt.title('Acerto vs profundidade (' + str(sizeByFlagTrain[y]) + " amostras de treino)")
        plt.xlabel('Profundidade')
        plt.ylabel('Acerto [%]')
        plt.plot(xData,rightGuessByDepth)
        plt.ylim([0, 100])
        plt.xlim([0, 15])
        plt.grid()
        #plt.clf()
        plt.savefig("plots\\acertoVsDp-"+str(sizeByFlagTrain[y]) + " de treino.jpg")
        plt.show()