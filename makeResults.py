import glob


def sortByN(taskList):
    return sorted(taskList, key=lambda x: x.n, reverse=False)


def parseName(text):
    user = text[7:7+6]
    n = text[7+6+1:-4]
    return user, n


txtfiles = []
for file in glob.glob("out/*.txt"):
    txtfiles.append(file)


class result:

    def __init__(self, user, n, result):
        self.user = user
        self.n = int(n)
        self.result = result


results = []

for txtfile in txtfiles:
    f = open(txtfile, "r")
    r = int(float(f.readline()[:-1]))
    user, n = parseName(txtfile)
    results.append(result(user, n, r))


while(True):
    user = input()
    found = []
    for result in results:
        if(result.user == user):
            found.append(result)
    found = sortByN(found)
    for f in found:
        print(f.result)
