from subprocess import call


num_of_islands = ["5"]
migration_ratio = ["1"]

models = [
    "convection"
]

numbers = [
    50, 100, 150, 200, 250, 300, 350, 400, 450, 500
]

students = [
    "132225",
    "132214",
    "132219",
    "132195",
    "125342",
    "132209",
    "132207",
    "132221",
    "127173",
    "132349",
    "132348",
    "132197",
    "132319",
    "132215",
    "127329",
    "132280",
    "126151",
    "132192"
]

for model in models:
    for student in students:
        for islandNum in num_of_islands:
            for ratio in migration_ratio:
                for n in numbers:
                    call(["python", "algorithm.py", "input/in"+student+"_"+str(n)+".txt", islandNum,
                          ratio, str(n), model])
