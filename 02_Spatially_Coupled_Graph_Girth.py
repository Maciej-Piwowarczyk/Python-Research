from collections import deque
from copy import deepcopy
from tqdm import tqdm

# Create the spatially-coupled graph using parameters of which edges are sent forward, and whether tail-biting or terminated
# graph should be an adjacency list, num_copies an integer, forwarded edges a list of tuples (c,v,n), TBTE 1 for tail-biting and 0 for terminating
def SCgraph(graph, num_copies, forwarded_edges, tail_biting):
    # How many vertices are in the graph
    g_len = len(graph)

    # Initialize the spatially-coupled graph with a deepcopy of the base graph
    # deepcopy allows the changing of inner lists without changing all of them
    scgraph = deepcopy(graph)
    
    # This block adds num_copies-1 additional copies of the input graph which we modify before tacking onto the end
    for copy in range(num_copies-1):
        # Each adjacency list needs to be updated with unique vertices
        # We do this by adding g_len to everything in input graph
        for vertex in range(g_len):
            for adjVert in range(len(graph[vertex])):
                graph[vertex][adjVert] += g_len

        # Now that the graph is modified to have unique vertices, we can add it to scgraph
        scgraph += deepcopy(graph)

    # This block forwards the edges of each copy of the graph according to the rules set by the input cvn
    # An input of (u,v,n) means edge (u,v) will be forwarded n copies
    sc_len = len(scgraph)
    for cvn in forwarded_edges:
        # We go block-by-block
        for i in range(num_copies):
            # First we remove the edge in the block we are currently looking at
            # This entails removing both vertices from each other's adjacency lists
            scgraph[cvn[0]+i*g_len].remove(cvn[1]+i*g_len)
            scgraph[cvn[1]+i*g_len].remove(cvn[0]+i*g_len)

            # Then we add two new half-edges stemming from the block we are working with
            # The other halves will be added when we are working with the blocks the edges were forwarded to
            # The 'or' statement only fails when the graph is NOT tail-biting and an edge would be forwarded right-to-left
            if not (cvn[1]+i*g_len-cvn[2]*g_len)//sc_len != 0 or tail_biting:
                scgraph[cvn[0]+i*g_len].append((cvn[1]+i*g_len-cvn[2]*g_len)%sc_len)
            if not (cvn[0]+i*g_len+cvn[2]*g_len)//sc_len != 0 or tail_biting:
                scgraph[cvn[1]+i*g_len].append((cvn[0]+i*g_len+cvn[2]*g_len)%sc_len)
        
    return scgraph

# Our algorithm for finding girth involves removing each edge and calculating the shortest path between the removed edge's vertices
# Single-pair shortest path using a BFS algorithm
def shortestPathBreak(graph,root,goal,stop):
    # Initialize the queue, marked, and the level tracking for each vertex
    queue = deque()
    marked = [0]*len(graph)
    level = [99999]*len(graph)

    # Add the root to the queue, mark it, and set its level to 0
    queue.append(root)
    marked[root] = 1
    level[root] = 0

    # Main loop
    # To-do: Add a break condition for when we reach a level beyond the current smallest path
    while len(queue) != 0:
        s = queue.popleft()
        for adjVert in graph[s]:
            if not marked[adjVert]:
                marked[adjVert] = 1
                level[adjVert] = level[s] + 1
                queue.append(adjVert)

                # This piece only triggers if the potential girth is already more than the current smallest 
                if level[adjVert] >= stop:
                    return level[adjVert]
                
                # After updating the level of adjacent, unmarked vertices, check to see if we just updated the goal vertex
                # BFS means that the first time we encounter goal vertex is the earliest we could have found it up to reordering of the levels above
                if adjVert == goal:
                    return level[goal]
                    
    # This line is for if we never encounter the goal vertex, i.e., it's in a different component
    return level[goal]

def Girth(graph):
    girth = 99999
    # edge_list is to make sure we only remove each edge once, as otherwise we'd double the work
    edge_list = set()
    for vertex in range(len(graph)):
        for adjVertex in graph[vertex]:
            edge_list.add(tuple(sorted((vertex,adjVertex))))

    # For each edge in the graph...
    for vert in tqdm(range(len(graph))):
        for adjVert in graph[vert]:
            # ... check if it's been removed and tested yet...
            if tuple(sorted((vert,adjVert))) in edge_list:
                edge_list.remove(tuple(sorted((vert,adjVert))))
                # ... and then create a deepcopy of the graph that we can remove an edge from and test
                # This preserves the original graph so we don't have to readd the edge
                cutGraph = deepcopy(graph)
                cutGraph[vert].remove(adjVert)
                cutGraph[adjVert].remove(vert)
                testLength = shortestPathBreak(cutGraph, vert, adjVert, girth) + 1
                if testLength < girth:
                    girth = testLength
    return girth
