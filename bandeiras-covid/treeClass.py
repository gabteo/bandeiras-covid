import math
from partitionCriteria import partitionCriteria
from leafNode import leafNode
from decisionNode import decisionNode

class treeClass:
    def __init__(self, trainingDataset, nodeDepth, maxDepth):
        self.treeNode = self.newTree(trainingDataset, maxDepth, nodeDepth)


    def getEntropy(self, data):
        # fonte: livro pagina 614
        labelOccurrences = self.numberOfLabelOccurrences(data)
        entropy = 0.0
        for label in labelOccurrences:
            labelProb = float(labelOccurrences[label])/float(len(data))
            entropy -= labelProb*math.log2(labelProb)
        return entropy


    def getGini(self, data):
         
        labelOccurrences = self.numberOfLabelOccurrences(data)

        # gini(node) = somatório para todas as labels de prob[label ocorrer]*(prob[lab NÃO cor])
        # = somatório para todas as labels de prob[label ocorrer]*(1-prob[lab ocor])
        # isso é igual a somatorio de (prob[ocorrer]-prob^2[ocorrer])
        # = 
        giniImpurity = 1
        for lbl in labelOccurrences:
            prob_of_lbl = labelOccurrences[lbl] / float(len(data))
            giniImpurity -= prob_of_lbl**2
        """ giniImpurity = 0
        for label in labelOccurrences:
            labelProb = float(labelOccurrences[label])/float(len(data))
            giniImpurity += labelProb*(1-labelProb) """
        return giniImpurity


    def getInformationGain(self, subsetA, subsetB, uncertainty, uncertaintyType = "gini"):
        # como no livro, página 615: o ganho de info é
        # incerteza[gini ou entropia] - resto
        # resto é prob[subsetA]*incerteza[subsetA]-prob[subsetB]*incerteza[subsetB]
        # (final da pág 614)
        
        probA = float(len(subsetA))/(len(subsetA)+len(subsetB))
        probB = 1 - probA

        if uncertaintyType == "gini":
            resto = probA*self.getGini(subsetA) + (1 - probA)*self.getGini(subsetB)
        elif uncertaintyType == "entropy":
            resto = probA*self.getEntropy(subsetA) + probB*self.getEntropy(subsetB)

        informationGain = uncertainty - resto
        return informationGain



    def getBestCut(self, data, uncertaintyType = "gini"):
        """ if uncertaintyType == "gini":
            uncertainty = self.getGini(data)
        elif uncertaintyType == "entropy":
            uncertainty = self.getEntropy(data) """

        uncertainty = self.getGini(data)
        bestGain = 0
        bestCriteria = None
        numberOfVariables = len(data[0])-1

        # qual variável usa? Percorre todas!
        for varIndex in range(numberOfVariables):  # -1 pq a ultima col é label
            # onde divide a variável? Percorre tudo, ordena, divide na média dos 
            # valores dois a dois e testa o ganho de info;
            # seria interessante evitar a repetição de valores
            sampleValues = list(set([row[varIndex] for row in data]))  # "gambiarra" pra não repetir valores e ordenar: fazer list
            #sampleValues.sort()
            valuesMeanList = []
            for i in range(1, len(sampleValues)):
                mean = (sampleValues[i-1]+sampleValues[i])/2.0
                valuesMeanList.append(mean)
            #valuesMeanList
            for dataValue in valuesMeanList:
                # instanciar "pergunta"
                criteria = partitionCriteria(varIndex, dataValue)

                # dividir dados
                trueRows, falseRows = self.divideData(data, criteria)  # retorna tupla

                # caso que não separa?
                if (len(trueRows) == 0) or (len(falseRows) == 0):
                    continue
                                
                # getInfoGain com a particao
                partitionGain = self.getInformationGain(trueRows, falseRows, uncertainty, uncertaintyType)

                if partitionGain >= bestGain:
                    bestGain, bestCriteria = partitionGain, criteria
                  

        #tem que retornar o ganho e a pergunta que divide
        return bestGain, bestCriteria

    def divideData(self, data, criteria):

        isSatisfied = []
        isNotSatisfied = []

        for dataRow in data:
            if criteria.isSatisfied(dataRow):   # é satisfeita quando o valor é >= que o criterio
                isSatisfied.append(dataRow)
                #print("sim")
            else:
                isNotSatisfied.append(dataRow)
                #print("nao")
        
        return isSatisfied, isNotSatisfied

    def printTree(self, node, tab=0):
        
        if isinstance(node, leafNode):
            print(" "*tab + "Bandeira ", node.leafData)
            return
        # imprime o critério
        print(" "*tab + str(node.criteria))
        
        # imprime subarvore direita
        print(" "*tab + ">>>Sim:")
        self.printTree(node.satisfied, tab+2)
        # imprime subarvore esquerda
        print(" "*tab + ">>>Nao:")
        self.printTree(node.notSatisfied, tab+2)


    

    def numberOfLabelOccurrences(self, data):
        # um dicionário (nao permite itens duplicados)
        # para armazenar as labels e quantas vezes ocorrem
        numberOfOccurrences = {}
        for row in data:
            rowLabel = row[-1]  # label na última coluna
            if rowLabel not in numberOfOccurrences:
                numberOfOccurrences[rowLabel] = 0
            numberOfOccurrences[rowLabel] += 1
        # retorna o dicionario com a contagem de ocorrencias de cada label
        return numberOfOccurrences

    def newTree(self, trainingDataset, maxDepth = 5, nodeDepth = -1):
        #if len(trainingDataset) == 0:
        #    print("Não existem dados para treinar a árvore!")
        nodeDepth += 1
        infoGain, divisionCriteria = self.getBestCut(trainingDataset, uncertaintyType="gini")
        # infoGain = bestCut[0]
        # divisionCriteria = bestCut[1]

        # caso base
        if (infoGain == 0) or (nodeDepth == maxDepth):
            return leafNode(trainingDataset)

        # agora executa a divisão
        trueData, falseData = self.divideData(trainingDataset, divisionCriteria)
        #satisfiedData = dividedData[0]
        #notSatisfiedData = dividedData[1]

        # constroi subarvore direita/verdadeira
        trueSubtree = treeClass(trainingDataset = trueData, nodeDepth=nodeDepth, maxDepth=maxDepth)
        trueNode = trueSubtree.treeNode
        # constroi subarvore esquerda/falsa
        falseSubtree = treeClass(trainingDataset = falseData, nodeDepth=nodeDepth, maxDepth=maxDepth)
        falseNode = falseSubtree.treeNode

        return decisionNode(divisionCriteria, trueNode, falseNode, nodeDepth)