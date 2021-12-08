header = ["conf sem/sem anterior", "interSRAG dia/semana anterior", "Leito COVID dia/sem. anterior", "UTI COVID dia/sem. anterior", "conf/100k", "obitos/100k", "utiDisp", "Mediana Ocup UTI 7d", "mediana Ocup Enf 7d", "label"]

class partitionCriteria:
    def __init__(self, varIndex, value) -> None:
        self.varIndex = varIndex
        self.value = value

    def isSatisfied(self, dataRow):
        return dataRow[self.varIndex] >= self.value
        
        # é satisfeita quando o valor é >= que o criterio
        """ if dataRow[self.varIndex] >= self.value:
            return True
        else:
            return False """

    def __repr__(self):
        return "%s é >= %s?" % (header[self.varIndex], str(self.value))