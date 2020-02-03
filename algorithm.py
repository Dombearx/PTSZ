# RAW ALGORITHM
from deap import creator, base, tools, algorithms, benchmarks
import migration as mig
import time
import utils
import numpy
import pickle
import sys
import random
import benchmarks_conf as bc
import os

# Przetwarzanie parametrów
# argv[0] to nazwa programu - tak jest domyślnie
# NAZWA BENCHMARKA - argv[1]
# LICZBA WYSP - argv[2]
# MNOŻNIK MIGRACJI - argv[3]
# MAX LICZBA WYWOŁAŃ BEZ POPRAWY - argv[4]
# MODEL - argv[5]

if(len(sys.argv) != 6):
    print("Wrong number of arguments!")
    print("Usage:", sys.argv[0],
          "fileName NUM_OF_ISLANDS MIGRATIONS_RATIO number_of_tasks MODEL")
    sys.exit()


# nazwa pliku z danymi
fileName = sys.argv[1]

# Początkowa liczba wysp
NUM_OF_ISLANDS = int(sys.argv[2])

# Mnożnik migracji
MIGRATION_RATIO = float(sys.argv[3])

# liczba zadan w przykladzie
number_of_tasks = int(sys.argv[4])

# model
MODEL = sys.argv[5]

# max
max_iterations_wo_improvement = 10000


POPULATION_SIZE = 50
ISLAND_POPULATION_SIZE = int(POPULATION_SIZE / NUM_OF_ISLANDS)
FREQ = int(MIGRATION_RATIO * POPULATION_SIZE)
CXPB, MUTPB = 0.1, 1


toolbox = bc.getPTSZToolBox(fileName)


toolbox.register("map", map)


# Migrate method
if(MODEL == "convection"):
    toolbox.register("migrate", mig.migSel, numOfIslands=NUM_OF_ISLANDS)

if(MODEL == "island"):
    toolbox.register("migrate", mig.migIslandsRandom,
                     numOfIslands=NUM_OF_ISLANDS)

# Statistics
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)


# Zapisuje n najlepszych osobników (tutaj n = 1)
hallOfFame = tools.HallOfFame(1)

# ngen = FREQ oznacza ile wykonań algorytmu się wykona przy jednym uruchomieniu funkcji
toolbox.register("algorithm", algorithms.eaSimple, toolbox=toolbox,
                 stats=stats, cxpb=CXPB, mutpb=MUTPB, ngen=FREQ, verbose=False, halloffame=hallOfFame)

logbooks = []

bestIndividuals = []

iterations_wo_improvement = 0

# Początkowa populacja
islands = [toolbox.population(n=ISLAND_POPULATION_SIZE)
           for i in range(NUM_OF_ISLANDS)]

if(NUM_OF_ISLANDS > 1):
    toolbox.migrate(islands)

for island in islands:
    hallOfFame.update(island)


first = True
previous_fitness = None
maxTime = 10 * number_of_tasks
iterations_wo_improvement = 0

print("Running:", fileName)
print("Islands number:", NUM_OF_ISLANDS)
print("Migration every", FREQ, "steps")
print("Max time [ms]:", maxTime)
print("Model:", MODEL)
print("----------START---------")
start_time = time.time()
while((time.time() - start_time) * 1000 < maxTime and iterations_wo_improvement <= max_iterations_wo_improvement / FREQ):

    results = toolbox.map(toolbox.algorithm, islands)

    islands = [island for island, logbook in results]

    if previous_fitness == None:
        previous_fitness = hallOfFame[0].fitness.values[0]
    else:
        if previous_fitness > hallOfFame[0].fitness.values[0]:
            iterations_wo_improvement = 0
        else:
            iterations_wo_improvement += 1

    print("Hall of fame:", hallOfFame[0], hallOfFame[0].fitness)

    if(NUM_OF_ISLANDS > 1):
        toolbox.migrate(islands)


print("----------END---------")
print("Hall of fame:", hallOfFame[0], hallOfFame[0].fitness)
print("Total time:", (time.time() - start_time) * 1000)

# Save results
utils.makeTxt(hallOfFame[0].fitness.values, hallOfFame[0],
              "out/out" + fileName[8:], fileName)
print("\n")
