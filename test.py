def getFirstFreeMachine(currentTimes):
    minTime = min(currentTimes)
    return currentTimes.index(minTime)


def generateSolution(n, numberOfMachines, inputFileName):

    numberOfTasks, tasks = utils.readInputFile(inputFileName)

    tasks = sortByR(tasks)

    while len(tasks) != 0:

        machine = getFirstFreeMachine(currentTimes)

        solution[machine].append(task.number)

        tasks.remove(task)

        currentTimes[machine] = max(currentTimes[machine], task.r) + task.p

    return solution


def eval(list_of_tasks):

    currentTimes = []
    solution = []
    for _ in range(4):
        currentTimes.append(0)
        solution.append([])

    for task_number in list_of_tasks:
        machine = getFirstFreeMachine(currentTimes)
        solution[machine].append(task_number)

        currentTimes[machine] = max(currentTimes[machine], task.r) + task.p

    return max(currentTimes)
