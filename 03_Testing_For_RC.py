import math

####################
# Helper Functions #
####################

def revComp(codeword):
    alphabet = ['A','C','G','T']
    compabet = ['T','G','C','A']
    revCodeword = ''
    for letter in codeword:
        revCodeword = compabet[alphabet.index(letter)] + revCodeword 
    return revCodeword

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

# INPUT
# graph = the graph
# maxRCLength = the longest RC length the code will test for
# OUTPUT
# Status updates on what it's checking
# Will quit early if no RC's found of a given length
def revCompCheck(graph,maxRCLength):
    for currentRC in range(3,maxRCLength):
        print('Checking for reverse complements of length ' + str(currentRC))
        
        pathLength = math.ceil((currentRC+1)/2)
        paths = pathGen(graph,pathLength)
        windows = []
        for path in paths:
            windows.append(path[:currentRC])
            windows.append(path[1:currentRC+1])

        flag = True
        for window in windows:
            if revComp(window) in windows and flag:
                flag = False
                # print("Found RC windows " + window + ' and ' + revComp(window) + ' of length ' + str(currentRC))
                # print('')

        if flag:
            print('No RCs of length ' + str(currentRC) + ' were found.') 
            break
    
    print('Process has terminated')


####################
# Example          #
####################
# graph = {"AC":{"CT","GG"},"CT":{"TG","AA"},"TG":{"GA","CC"},"GA":{"AC","TT"},"CC":{"AC","GA"},"TT":{"AC","CT"},"GG":{"CT","TG"},"AA":{"GA","TG"}}
# revCompCheck(graph,6)
