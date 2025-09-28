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
            # print('Up Return: None')
            return None

        new_config = list(self.config)

        new_config[self.blank_index] = new_config[self.blank_index - self.n]
        new_config[self.blank_index - self.n] = 0
        self.blank_index = self.config.index(0)

        # print('Up Return: ' + str(new_config))

        return PuzzleState(new_config, self.n, self, "Up", self.cost + 1)


    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if 0 in self.config[-self.n:]:
            # print('Down Return: None')
            return None

        new_config = list(self.config)

        new_config[self.blank_index] = new_config[self.blank_index + self.n]
        new_config[self.blank_index + self.n] = 0
        self.blank_index = self.config.index(0)

        # print('Down Return: ' + str(new_config))
        return PuzzleState(new_config, self.n, self, "Down", self.cost + 1)

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == 0:
            # print('Left Return: None')
            return None

        new_config = list(self.config)

        new_config[self.blank_index] = new_config[self.blank_index - 1]
        new_config[self.blank_index - 1] = 0
        self.blank_index = self.config.index(0)

        # print('Left Return: ' + str(new_config))
        return PuzzleState(new_config, self.n, self, "Left", self.cost + 1)

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == self.n - 1:
            # print('Right Return: None')
            return None

        new_config = list(self.config)

        new_config[self.blank_index] = new_config[self.blank_index + 1]
        new_config[self.blank_index + 1] = 0
        self.blank_index = self.config.index(0)

        # print('Right Return: ' + str(new_config))
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
def writeOutput(state, numNodesExpanded, searchDepth, maxSearchDepth, runningTime, maxRamUsage):
    ### Student Code Goes here

    path = []
    getPathNode = state
    while state.parent is not None:
        path = [getPathNode.action] + path
        getPathNode = getPathNode.parent

    with open("output.txt", "w") as f:
        f.write("path_to_goal: " + str(path) + "\n")
        f.write("cost_of_path: " + str(state.cost) + "\n")
        f.write("nodes_expanded: " + str(getPathNode.cost) + "\n")
        f.write("search_depth: " + str(getPathNode.cost) + "\n")
    pass

def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    expanded = 0
    frontier = queue.Queue()
    frontierSet = set()
    frontier.put(initial_state)
    frontierSet.add(tuple(initial_state.config))

    explored = set()

    while len(frontierSet) != 0:
        state = frontier.get()
        frontierSet.remove(tuple(state.config))
        explored.add(tuple(state.config))
        expanded += 1

        if test_goal(state):
            return state
            # return state, numNodesExpanded, searchDepth, maxSearchDepth, runningTime, maxRamUsage

        for neighbor in state.expand():
            if tuple(neighbor.config) not in frontierSet and \
               tuple(neighbor.config) not in explored:
                frontier.put(neighbor)
                frontierSet.add(tuple(neighbor.config))

        print(expanded)

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

    while len(frontierSet) != 0:
        state = frontier.pop()
        frontierSet.remove(tuple(state.config))
        explored.add(tuple(state.config))
        # print('\n\n\nState: ' + str(state.config) + '\n')
        # print(str(state.action))

        if test_goal(state):
            return state

        neighbors = state.expand()[::-1]
        expanded += 1
        for neighbor in neighbors:
            # print(neighbor.config)
            if tuple(neighbor.config) not in frontierSet and \
               tuple(neighbor.config) not in explored:
                frontier.append(neighbor)
                frontierSet.add(tuple(neighbor.config))

        print(expanded)
        # import pdb; pdb.set_trace()
    return False

# def updatePriority(pqueue, state, priority):
#     """Update the priority of a state in the priority queue"""
    
#     for index, (p, c, s) in enumerate(pqueue):
#         if s == state:
#             if p <= priority:
#                 return
#             del pqueue[index]
#             pqueue.append((priority, c, s))
#             heapq.heapify(pqueue)
#             return

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

    print('\n\nEntering addToPriorityQueue')
    print(state.config)
    # import pdb; pdb.set_trace()

    if tuple(state.config) not in queueDict or tuple(state.config) not in explored:
        # Have not visited config - Add to queue
        print('AAAAAAAAAAAA')
        print(stateCost)
        heapq.heappush(priorityQueue, (stateCost, getTieBreaker(state.action), state.cost, counter, state))
        queueDict[tuple(state.config)] = stateCost

    elif stateCost < queueDict[tuple(state.config)]:
        # Visited config but found a cheaper path - Update priority
        print('BBBBBBBBBBBB')
        queueDict[tuple(state.config)] = stateCost
        heapq.heappush(priorityQueue, (stateCost, getTieBreaker(state.action), state.cost, counter, state))

    else:
        # Visited config and have not found a cheaper path - Do nothing
        print('CCCCCCCCCCCC')
        pass

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    frontier = []
    frontierDict = {}
    explored = set()

    finalTieBreakerCounter = 0

    heapq.heappush(frontier, (calculate_total_cost(initial_state), 0, 0, finalTieBreakerCounter, initial_state))
    frontierDict[tuple(initial_state.config)] = calculate_total_cost(initial_state)


    while len(frontier) != 0:
        # import pdb; pdb.set_trace()
        priority, _, _, _, state = heapq.heappop(frontier)

        if priority > frontierDict[tuple(state.config)]:
            # Outdated entry in priority queue - Skip
            pass
        else:
            if tuple(state.config) not in explored:
                explored.add(tuple(state.config))

            if test_goal(state):
                return state
            
            # if tuple(state.config) not in frontierDict:
            for neighbor in state.expand():
                finalTieBreakerCounter += 1
                addToPriorityQueue(frontier, frontierDict, explored, neighbor, finalTieBreakerCounter)


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
    print(puzzle_state.config)
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

    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))


if __name__ == '__main__':
    main()
