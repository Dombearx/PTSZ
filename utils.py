def makelogFile(lines, outputName):
    file = open(outputName, "w")
    for line in lines:
        for value in line:
            file.write(str(value) + "\t")
        file.write("\n")
    file.close()


class result:

    def __init__(self, logbooks, hallOfFamers, time):
        self.logbooks = logbooks
        self.hallOfFamers = hallOfFamers
        self.time = time

    def getLogbooks(self):
        return self.logbooks

    def getHallOfFamers(self):
        return self.hallOfFamers

    def getTime(self):
        return self.time
