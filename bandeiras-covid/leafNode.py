class leafNode:
    def __init__(self, data) -> None:
        self.leafData = self.numberOfLabelOccurrences(data) #para análise de treinamento
        self.isLeaf = True

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