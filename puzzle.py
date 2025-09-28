from __future__ import division
import resource
import heapq
# from __future__ import print_function

import sys
import math
import time
import queue


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if 0 in self.config[0:self.n]:
            return None

        new_config = list(self.config)

        new_config[self.blank_index] = new_config[self.blank_index - self.n]
        new_config[self.blank_index - self.n] = 0
        self.blank_index = self.config.index(0)

        return PuzzleState(new_config, self.n, self, "Up", self.cost + 1)


    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if 0 in self.config[-self.n:]:
            return None

        new_config = list(self.config)

        new_config[self.blank_index] = new_config[self.blank_index + self.n]
        new_config[self.blank_index + self.n] = 0
        self.blank_index = self.config.index(0)

        return PuzzleState(new_config, self.n, self, "Down", self.cost + 1)

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == 0:
            return None

        new_config = list(self.config)

        new_config[self.blank_index] = new_config[self.blank_index - 1]
        new_config[self.blank_index - 1] = 0
        self.blank_index = self.config.index(0)

        return PuzzleState(new_config, self.n, self, "Left", self.cost + 1)

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == self.n - 1:
            return None

        new_config = list(self.config)

        new_config[self.blank_index] = new_config[self.blank_index + 1]
        new_config[self.blank_index + 1] = 0
        self.blank_index = self.config.index(0)

        return PuzzleState(new_config, self.n, self, "Right", self.cost + 1)

    def expand(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(state, numNodesExpanded, maxSearchDepth, runningTime, maxRamUsage):
    ### Student Code Goes here

    cost = state.cost
    path = []
    getPathNode = state
    while True:
        if state.action == "Initial":
            break
        path = [state.action] + path
        state = state.parent

    with open("output.txt", "w") as f:
        f.write("path_to_goal: "     + str(path)             + "\n")
        f.write("cost_of_path: "     + str(cost)             + "\n")
        f.write("nodes_expanded: "   + str(numNodesExpanded) + "\n")
        f.write("search_depth: "     + str(cost)             + "\n")
        f.write("max_search_depth: " + str(maxSearchDepth)   + "\n")
        f.write("running_time: "     + str(runningTime)      + "\n")
        f.write("max_ram_usage: "    + str(maxRamUsage)      + "\n")

def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    expanded = 0
    frontier = queue.Queue()
    frontierSet = set()
    frontier.put(initial_state)
    frontierSet.add(tuple(initial_state.config))

    explored = set()

    maxDepth = 0

    while len(frontierSet) != 0:
        state = frontier.get()
        frontierSet.remove(tuple(state.config))
        explored.add(tuple(state.config))

        if test_goal(state):
            return state, expanded, maxDepth

        neighbors = state.expand()
        expanded += 1

        for neighbor in neighbors:
            if tuple(neighbor.config) not in frontierSet and \
               tuple(neighbor.config) not in explored:

                if neighbor.cost > maxDepth:
                    maxDepth = neighbor.cost
                frontier.put(neighbor)
                frontierSet.add(tuple(neighbor.config))

    return False

def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    expanded = 0
    frontier = list()
    frontierSet = set()
    frontier.append(initial_state)
    frontierSet.add(tuple(initial_state.config))

    explored = set()

    maxDepth = 0

    while len(frontierSet) != 0:
        state = frontier.pop()
        frontierSet.remove(tuple(state.config))
        explored.add(tuple(state.config))

        if test_goal(state):
            return state, expanded, maxDepth

        neighbors = state.expand()[::-1]
        expanded += 1

        for neighbor in neighbors:
            if tuple(neighbor.config) not in frontierSet and \
               tuple(neighbor.config) not in explored:
                if neighbor.cost > maxDepth:
                    maxDepth = neighbor.cost
                frontier.append(neighbor)
                frontierSet.add(tuple(neighbor.config))

    return False

def getTieBreaker(action):
    """Get a tie breaker value for a state"""
    if action == "Up":
        return 1
    
    elif action == "Down":
        return 2
    
    elif action == "Left":
        return 3
    
    elif action == "Right":
        return 4

    return 0

def addToPriorityQueue(priorityQueue, queueDict, explored, state, counter):
    """Add a state to the priority queue"""    
    stateCost = calculate_total_cost(state)

    if tuple(state.config) not in queueDict or tuple(state.config) not in explored:
        # Have not visited config - Add to queue
        heapq.heappush(priorityQueue, (stateCost, getTieBreaker(state.action), state.cost, counter, state))
        queueDict[tuple(state.config)] = stateCost
        depth = state.cost

    elif stateCost < queueDict[tuple(state.config)]:
        # Visited config but found a cheaper path - Update priority
        queueDict[tuple(state.config)] = stateCost
        heapq.heappush(priorityQueue, (stateCost, getTieBreaker(state.action), state.cost, counter, state))
        depth = state.cost

    else:
        # Visited config and have not found a cheaper path - Do nothing
        depth = None
        pass

    return depth

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    frontier = []
    frontierDict = {}
    explored = set()

    finalTieBreakerCounter = 0

    expanded = 0
    maxDepth = 0

    heapq.heappush(frontier, (calculate_total_cost(initial_state), 0, 0, finalTieBreakerCounter, initial_state))
    frontierDict[tuple(initial_state.config)] = calculate_total_cost(initial_state)


    while len(frontier) != 0:
        priority, _, _, _, state = heapq.heappop(frontier)

        if priority > frontierDict[tuple(state.config)]:
            # Outdated entry in priority queue - Skip
            pass
        else:
            if tuple(state.config) not in explored:
                explored.add(tuple(state.config))

            if test_goal(state):
                return state, expanded, maxDepth

            neighbors = state.expand()
            expanded += 1

            for neighbor in neighbors:
                finalTieBreakerCounter += 1
                neighborDepth = addToPriorityQueue(frontier, frontierDict, explored, neighbor, finalTieBreakerCounter)

                if neighborDepth is not None and neighborDepth > maxDepth:
                    maxDepth = neighborDepth


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    g_of_n = state.cost

    f_of_n = 0
    for idx, value in enumerate(state.config):
        f_of_n += calculate_manhattan_dist(idx, value, state.n)

    return g_of_n + f_of_n

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    distanceConfig = abs(idx - value)

    # Move up/down is of size n (divide), move left/right is of size 1 (remainder)
    return int(distanceConfig / n) + (distanceConfig % n)

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    goalState = [0,1,2,3,4,5,6,7,8]
    return puzzle_state.config == goalState

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()

    startRam = float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if   search_mode == "bfs":
        finalState, expanded, maxDepth = bfs_search(hard_state)
    elif search_mode == "dfs":
        finalState, expanded, maxDepth = dfs_search(hard_state)
    elif search_mode == "ast":
        finalState, expanded, maxDepth = A_star_search(hard_state)
    else:
        finalState = None
        print("Enter valid command arguments !")

    endRam = float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    end_time = time.time()

    if finalState is not None:
        writeOutput(finalState, expanded, maxDepth, end_time - start_time, (endRam - startRam) / (2.0**20.0))

    print("Program completed in %.3f second(s)"%(end_time-start_time))


if __name__ == '__main__':
    main()
