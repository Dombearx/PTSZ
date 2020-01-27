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


class Task:
    def __init__(self, p, r, d, number):
        # czas przetwarzania
        self.p = int(p)
        # czas gotowosci
        self.r = int(r)
        # oczekiwany czas zakonczenia
        self.d = int(d)
        self.number = number


def checkInputFile(inputFileName):
    inputFile = open(inputFileName, "r")
    tasks = []

    for index, line in enumerate(inputFile):
        # ignore first line
        if(index != 0):
            p, r, d = line.split(" ")
            tasks.append(Task(p, r, d, index))

    inputFile.close()

    for task in tasks:
        if (task.r >= task.d):
            return False

        if (task.d - task.r < task.p):
            return False

        if(task.p <= 0):
            return False

    return True


def readInputFile(inputFileName):
    inputFile = open(inputFileName, "r")
    tasks = []

    for index, line in enumerate(inputFile):
        # ignore first line
        if(index != 0):
            p, r, d = line.strip().split(" ")
            tasks.append(Task(p, r, d, index))
        else:
            # First line
            numberOfTasks = line

    return int(numberOfTasks), tasks


def readSolutionFile(solutionFileName):
    solutionFile = open(solutionFileName, "r")

    lines = []

    for index, line in enumerate(solutionFile):
        if(index != 0):
            lines.append(line.split(" "))
        else:
            # First line
            sum = line

    return sum, lines


def calculateSum(inputFileName, solution):
    """calculate sum of delays

    Arguments:
        inputFileName {string} -- file with input data
        solution {list} -- list with tasks associated to machines
    """
    inputFile = open(inputFileName, "r")
    tasks = []

    for index, line in enumerate(inputFile):
        # ignore first line
        if(index != 0):
            p, r, d = line.split(" ")
            tasks.append(Task(p, r, d, index))

    inputFile.close()
    sum = 0
    currentTime = 0

    for line in solution:
        for taskNumber in line:
            currentTime = tasks[int(taskNumber) - 1].r if tasks[int(taskNumber) -
                                                                1].r > currentTime else currentTime
            currentTime += tasks[int(taskNumber) - 1].p
            sum += max(0, currentTime - tasks[int(taskNumber) - 1].d)
        currentTime = 0

    return sum


def calculateFittnesValue(tasks, solution):

    sum = 0
    currentTime = 0

    for line in solution:
        for taskNumber in line:
            currentTime = tasks[int(taskNumber) - 1].r if tasks[int(taskNumber) -
                                                                1].r > currentTime else currentTime
            currentTime += tasks[int(taskNumber) - 1].p
            sum += max(0, currentTime - tasks[int(taskNumber) - 1].d)
        currentTime = 0

    return sum


def makeTxt(sum, list_of_taskts_id, outputName, inputFileName):
    file = open(outputName, "w")

    solution = eval(list_of_taskts_id, inputFileName)

    file.write(str(sum[0]) + "\n")
    for line in solution:
        file.write(" ".join(map(str, line)))
        file.write("\n")
    file.close()


def getFirstFreeMachine(currentTimes):
    minTime = min(currentTimes)
    return currentTimes.index(minTime)


def eval(list_of_tasks_id, inputFileName):

    _, tasks = readInputFile(inputFileName)

    currentTimes = []
    solution = []
    for _ in range(4):
        currentTimes.append(0)
        solution.append([])

    for task_id in list_of_tasks_id:
        machine = getFirstFreeMachine(currentTimes)
        solution[machine].append(task_id)

        currentTimes[machine] = max(
            currentTimes[machine], tasks[task_id - 1].r) + tasks[task_id - 1].p

    return solution


def makeSimpleLogFile(lines, outputName):
    file = open(outputName, "w")
    for value in lines:
        file.write(str(value) + "\t")
    file.close()


def generateOutputFile(sum, solution, outputName):
    lines = []
    space = " "
    for line in solution:
        lines.append(space.join(map(str, line)))
    makeTxt(sum, lines, outputName)
