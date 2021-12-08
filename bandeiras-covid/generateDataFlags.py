import csv
import numpy as np


class generateDataFlags():
    def __init__(self) -> None:
        self.rows = 3**9
        self.collums = 10

        self.yellowCount = 0
        self.orangeCount = 0
        self.redCount = 0

        #self.data = []        
        self.dataFlag = np.ones((self.rows, self.collums), dtype=int, order='C')    #ver arg like
        #print(self.data)
        self.fillMatrix()
        print(self.dataFlag)
        self.calcFlag()

        self.saveCSV(self.dataFlag, "entireDataset.csv")
        self.saveCSV(self.yellowFlag, "yellowData.csv")
        self.saveCSV(self.orangeFlag, "orangeData.csv")
        self.saveCSV(self.redFlag, "redData.csv")

        print("------------------------")
        print(self.yellowCount, "amarelas,", self.orangeCount, "laranjas e", self.redCount, "vermelhas.")

        print("\nbandeira amarela:", self.yellowCount)
        print(self.yellowFlag)

        print("\nbandeira laranja:", self.orangeCount)
        print(self.orangeFlag)

        print("\nbandeira vermelha:", self.redCount)
        print(self.redFlag)
        

    def fillMatrix(self):
        for l in range(1, self.rows):
            for c in range(self.collums-1):
                self.dataFlag[l][c] = self.dataFlag[l-1][c]
            c = self.collums - 2    # -1 por contar de zero, -1 por ignorar a ultima coluna 
            self.incrementLine(l, c)


    def incrementLine(self, l, c):
        if self.dataFlag[l][c] < 3:
            self.dataFlag[l][c] += 1
            return
        else:
            self.dataFlag[l][c] = 1
            c -= 1
            if c >= 0:
                self.incrementLine(l, c)
            else:
                return


    def calcFlag(self):
        for l in range(self.rows):
            row = self.dataFlag[l]
            #print(row)
            flagA = float(row[0]+row[1]+row[2]+row[3])*0.375
            flagB = float(row[4]+row[5])*1.75
            flagC = float(row[6]+2*row[7]+2*row[8])
            rowScore = (flagA+flagB+flagC)/10.0
            #print(rowScore)

            #seta a bandeira da linha e classifica em matrizes amarela, laranja e vermelha
            if rowScore < 2.0:
                rowFlag = 1                
                self.yellowCount +=1
            elif rowScore < 2.7:
                rowFlag = 2
                self.orangeCount += 1
            else:
                rowFlag = 3
                self.redCount += 1

            # até aqui, a última coluna tem lixo
            self.dataFlag[l][self.collums-1] = int(rowFlag)

            if rowFlag == 1:
                if self.yellowCount != 1:
                    self.yellowFlag = np.append(self.yellowFlag, [self.dataFlag[l]], axis=0)
                else:
                    self.yellowFlag = np.empty((1, 10), dtype=int, order='C')
                    for c in range(self.collums):
                        self.yellowFlag[0][c] = self.dataFlag[l][c]
            elif rowFlag == 2:
                if self.orangeCount != 1:
                    self.orangeFlag = np.append(self.orangeFlag, [self.dataFlag[l]], axis=0)
                else:
                    self.orangeFlag = np.empty((1, 10), dtype=int, order='C')
                    for c in range(self.collums):
                        self.orangeFlag[0][c] = self.dataFlag[l][c]
            else:
                if self.redCount != 1:
                    self.redFlag = np.append(self.redFlag, [self.dataFlag[l]], axis=0)
                else:
                    self.redFlag = np.empty((1, 10), dtype=int, order='C')
                    for c in range(self.collums):
                        self.redFlag[0][c] = self.dataFlag[l][c]
    
    def saveCSV(self, data, fileName):
        print("Salvando " + fileName + "...")

        try:
            np.savetxt(fileName, data, delimiter=';', fmt='%d')
        except:
            print("erro ao salvar!")


generateDataFlags()