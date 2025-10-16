####################
# Helper Functions #
####################

def letterFollows(graph,vertex,letter):
    bucket = set()
    for adjVertex in graph[vertex]:
        bucket.add(adjVertex[0])
    if letter in bucket:
        return True
    else: 
        return False    

def vertexFollows(graph,vertex,letter):
    bucket = set()
    for preVertex in graph:
        if vertex in graph[preVertex]:
            bucket.add(preVertex[1])
    if letter in bucket:
        return True
    else: 
        return False

# generate all paths of a given length in a graph
def pathGen(graph,length):
    # initialize two empty sets, the one that stores the most up-to-date paths and the work place
    allPaths = []
    pathsInProgress = []

    # fill allPaths with length 1 paths
    for vertex in graph:
        allPaths.append(vertex)

    # repeat length-1 times since we already have length 1
    for k in range(length-1):
        # clear the work space
        pathsInProgress.clear()
        # extend each path using the adjacencies of the last vertex
        for path in allPaths:
            for adjVertex in graph[path[-2:]]:
                pathsInProgress.append(path+adjVertex)

        # update allPaths
        allPaths = pathsInProgress[:]

    return allPaths

# INPUTS
# graph = the graph
# errPath = path from the original graph with an error
# errPosition = position of the error
# deletion = 1 or 0 depending on whether the error was a deletion or not
# OUTPUT
# the number of bases after the error required to determine that an error occured
# ASSUMPTION
# At least one vertex preceeding vertex that contains error
def errorDetect(graph,errPath,errPosition,deletion):

    # initialize ell0 and ell1 to track error detection in both options for splits
    ell0 = 999
    ell1 = 999

    # number of letters before and after the position of the error
    preStrandLength = errPosition
    pstStrandLength = len(errPath) - errPosition - 1

    #########################
    # First we'll check the splitting that puts a full vertex in front of the error position
    # check whether each vertex before the error exists
    for b in range(preStrandLength//2):
        if errPath[b*2+preStrandLength%2:b*2+preStrandLength%2+2] not in graph and ell0 > 0:
            ell0 = 0
            break
    # after successfully verifying each vertex, make sure they do actually follow each other
    # exclude case 0 -> 12 -> errPosition
    if errPosition > 3 and ell0 > 0:
        for b in range(preStrandLength//2-1):
            if errPath[b*2+preStrandLength%2+2:b*2+preStrandLength%2+4] not in graph[errPath[b*2+preStrandLength%2:b*2+preStrandLength%2+2]]:
                ell0 = 0
                break
    # if odd, we'll have a leftover letter remaining at the beginning that we can also check
    if preStrandLength%2 and ell0 > 0:
        if not vertexFollows(graph,errPath[1:3],errPath[0]):
            ell0 = 0
    # check if error follows
    if ell0 > 0:
        if not letterFollows(graph,errPath[errPosition-2:errPosition],errPath[errPosition]):
            ell0 = 0

    # now check using letters after the error
    for a in range(1,pstStrandLength+1):
        # a even
        if not a%2 and ell0 > a:
            if not letterFollows(graph,errPath[errPosition+a-2:errPosition+a],errPath[errPosition+a]):
                ell0 = a
        # a odd
        elif a%2 and ell0 > a:
            if errPath[errPosition+a-1:errPosition+a+1] not in graph:
                ell0 = a
            elif errPath[errPosition+a-1:errPosition+a+1] not in graph[errPath[errPosition+a-3:errPosition+a-1]]:
                ell0 = a

    #########################
    # Then we'll check the other splitting, where the error is the second letter of a vertex
    # check whether each vertex before error exists
    for b in range((preStrandLength+1)//2):
        if errPath[b*2+(preStrandLength+1)%2:b*2+(preStrandLength+1)%2+2] not in graph and ell1 > 0:
            ell1 = 0
            break
    # after successfully verifying each vertex, make sure they do actually follow each other
    # exclude case 01 -> 2
    if errPosition > 2 and ell1 > 0:
        for b in range((preStrandLength-1)//2):
            if errPath[b*2+(preStrandLength+1)%2+2:b*2+(preStrandLength+1)%2+4] not in graph[errPath[b*2+(preStrandLength+1)%2:b*2+(preStrandLength+1)%2+2]]:
                ell1 = 0
                break
    # if even, we'll have a leftover letter remaining at the beginning that we can also check
    if not preStrandLength%2 and ell1 > 0:
        if not vertexFollows(graph,errPath[1:3],errPath[0]):
            ell1 = 0
    
    # now check using letters after the error
    for a in range(1,pstStrandLength+1):
        # a even
        if not a%2 and ell1 > a:
            if errPath[errPosition+a-1:errPosition+a+1] not in graph:
                ell1 = a
            elif errPath[errPosition+a-1:errPosition+a+1] not in graph[errPath[errPosition+a-3:errPosition+a-1]]:
                ell1 = a
        # a odd
        elif a%2 and ell1 > a:
            if not letterFollows(graph,errPath[errPosition+a-2:errPosition+a],errPath[errPosition+a]):
                ell1 = a

    return max(ell0,ell1) + deletion


# graph = {"AC":{"CT","GG"},"CT":{"TG","AA"},"TG":{"GA","CC"},"GA":{"AC","TT"},"CC":{"AC","GA"},"TT":{"AC","CT"},"GG":{"CT","TG"},"AA":{"GA","TG"}}
# alphabet = ['A','C','G','T']

# befNum = 2
# aftNum = 2
# pathLength = befNum + aftNum + 1

subCounter = {999:0}
delCounter = {999:0}
insCounter = {999:0}
for i in range(aftNum*2+2):
    subCounter[i] = 0
    delCounter[i] = 0
    insCounter[i] = 0

paths = pathGen(graph,pathLength)

# sub errors
for path in paths:
    for letter in alphabet:
        # first position
        if letter != path[befNum*2]:
            pathWithError = path[:befNum*2] + letter + path[befNum*2+1:]
            j = errorDetect(graph,pathWithError,befNum*2,0)
            subCounter[j] += 1
        # second position
        if letter != path[befNum*2+1]:
            pathWithError = path[:befNum*2+1] + letter + path[befNum*2+2:]
            k = errorDetect(graph,pathWithError,befNum*2+1,0)
            subCounter[k] += 1

print("Substitution Errors")
subTotalList = []
for item in subCounter:
    subTotalList.append(subCounter[item])
subTotal = sum(subTotalList)
for item in subCounter:
    print(str(item) + ' - ' + str(subCounter[item]/subTotal))
print('')

# ins errors
for path in paths:
    for letter in alphabet:
        # first position
        pathWithError = path[:befNum*2] + letter + path[befNum*2:]
        j = errorDetect(graph,pathWithError,befNum*2,0)
        insCounter[j] += 1
        # second position
        pathWithError = path[:befNum*2+1] + letter + path[befNum*2+1:]
        k = errorDetect(graph,pathWithError,befNum*2+1,0)
        insCounter[k] += 1

print("Insertion Errors")
insTotalList = []
for item in insCounter:
    insTotalList.append(insCounter[item])
insTotal = sum(insTotalList)
for item in insCounter:
    print(str(item) + ' - ' + str(insCounter[item]/insTotal))
print('')

# del errors 
for path in paths:
    # first position
    pathWithError = path[:befNum*2] + path[befNum*2+1:]
    j = errorDetect(graph,pathWithError,befNum*2,1)
    delCounter[j] += 1
    # second position
    pathWithError = path[:befNum*2+1] + path[befNum*2+2:]
    k = errorDetect(graph,pathWithError,befNum*2+1,1)
    delCounter[k] += 1

print("Deletion Errors")
delTotalList = []
for item in delCounter:
    delTotalList.append(delCounter[item])
delTotal = sum(delTotalList)
for item in delCounter:
    print(str(item) + ' - ' + str(delCounter[item]/delTotal))
print('')
