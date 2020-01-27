#  benchmarks
from deap import creator, base, tools, algorithms, benchmarks
import migration as mig
import time
import utils
import numpy
import pickle
import sys
import random
import utils
import math
import copy

from itertools import repeat
try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequenc


def ptszMutate(individual):
    genotype = copy.copy(individual)
    a = random.randint(0, len(genotype) - 1)
    b = random.randint(0, len(genotype) - 1)
    individual[a] = genotype[b]
    individual[b] = genotype[a]
    return individual,


def ptszCrossover(individual1, individual2):
    genotype1 = individual1
    genotype2 = individual2

    priority1 = [0] * len(genotype1)
    priority2 = [0] * len(genotype2)

    priority = 1
    for g1, g2 in zip(genotype1, genotype2):
        priority1[g1 - 1] = priority
        priority2[g2 - 1] = priority
        priority += 1

    point = math.floor(len(priority1) / 2)

    priority1, priority2 = priority1[:point] + \
        priority2[point:], priority2[:point] + priority1[point:]

    for i in range(0, len(priority1)):
        priority1[i] = (i + 1, priority1[i])
        priority2[i] = (i + 1, priority2[i])

    priority1.sort(key=lambda x: x[1])
    priority2.sort(key=lambda x: x[1])

    result1 = [i[0] for i in priority1]
    result2 = [i[0] for i in priority2]

    for index, r1 in enumerate(result1):
        individual1[index] = r1
    for index, r2 in enumerate(result2):
        individual2[index] = r2

    return individual1, individual2


def sortByR(taskList):
    return sorted(taskList, key=lambda x: x.r, reverse=False)


def generateListSolution(tasks):

    t2 = copy.deepcopy(tasks)

    if random.randint(0, 1) < 1:
        random.shuffle(t2)
    t2 = sortByR(t2)

    nums = [task.number for task in t2]

    return nums


def registerStandard(attributes, creator, evalBenchmark, tasks):

    toolbox = base.Toolbox()

    #toolbox.register("attr_list", random.sample, range(attributes), attributes)
    toolbox.register("attr_list", generateListSolution, tasks)
    toolbox.register("individual", tools.initIterate, creator.Individual,
                     toolbox.attr_list)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evalBenchmark)
    toolbox.register("mate", ptszCrossover)
    toolbox.register("mutate", ptszMutate)

    toolbox.register("select", tools.selTournament, tournsize=3)

    return toolbox


def getPTSZToolBox(inputFileName):

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    numberOfTasks, tasks = utils.readInputFile(inputFileName)

    def getFirstFreeMachine(currentTimes):
        minTime = min(currentTimes)
        return currentTimes.index(minTime)

    def evalBenchmark(individual):
        return eval(individual)

    def eval(list_of_tasks_id):
        currentTimes = []
        solution = []
        for _ in range(4):
            currentTimes.append(0)
            solution.append([])

        tardines_sum = 0

        for task_id in list_of_tasks_id:
            machine = getFirstFreeMachine(currentTimes)
            solution[machine].append(task_id)

            currentTimes[machine] = max(
                currentTimes[machine], tasks[task_id - 1].r) + tasks[task_id - 1].p

            tardines_sum += max(0, currentTimes[machine] -
                                tasks[task_id - 1].d)

        return tardines_sum,

    toolbox = registerStandard(numberOfTasks, creator, evalBenchmark, tasks)

    return toolbox
