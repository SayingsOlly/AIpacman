# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def backPath(problem, cameFrom, goal):
    current = goal
    path = []
    while current[0] != problem.getStartState():
        path.append(current[1])
        current = cameFrom[current]
    path.reverse()
    return path

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    """
    Initiation, 

    frontier: store the search path use stack.
    
    cameFrom list: store the path which the current state came from
    
    visited list: visited state

    """

    frontier = util.Stack()
    startState = problem.getStartState()
    start = (startState, '', 0)
    goal = []
    frontier.push(start)
    cameFrom = {}
    cameFrom[start] = None
    visited = {}
    visited[startState] = True

    while not frontier.isEmpty():
         """get the current successor"""
        current = frontier.pop()
        visited[current[0]] = True
        
        """check if it reach the goal state, if not, get the next state by the scuccessor"""
        if problem.isGoalState(current[0]):
            goal = current
            break 
        for next in problem.getSuccessors(current[0]):
            """if not been visited, push into search stack"""
            if next[0] not in visited:
                frontier.push(next)
                cameFrom[next] = current
    "return path from goal to start"
    return backPath(problem, cameFrom, goal)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    """
    Initiation, 
    the search queue: store the path.
    
    cameFrom list: store the path which the current state came from
    
    visited list: visited state

    """

    frontier = util.Queue()
    startState = problem.getStartState()
    start = (startState,'', 0)# state format (state,path,value)
    goal = []
    frontier.push(start)
    
    cameFrom = {}
    cameFrom[start] = None

    visited = {}
    visited[startState] = True

    """search begin"""
    while not frontier.isEmpty():#if queue is not empty
        """get the current successor"""
        current = frontier.pop()
        
        """check if it reach the goal state, if not, get the next state by the scuccessor"""
        if problem.isGoalState(current[0]):
            goal = current
            break 
        for next in problem.getSuccessors(current[0]):
            """if not been visited, push into search queue"""
            if next[0] not in visited:
                frontier.push(next)
                cameFrom[next] = current
                visited[next[0]] = True

    "return path from goal to start"
    return backPath(problem, cameFrom, goal)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    """
    Initiation, 
    frontier: store the search path using priority queue.
    
    cameFrom list: store the path which the current state came from
    
    visited list: visited state

    costSoFar list: current cost list
    """
    frontier = util.PriorityQueue()
    startState = problem.getStartState()
    start = (startState, '', 0)
    goal = []
    frontier.push(start, 0)
    cameFrom = {}
    cameFrom[start] = None
    visited = {}
    visited[startState] = True
    """cost list"""
    costSoFar = {}
    costSoFar[startState] = 0

    "Iteration"
    while not frontier.isEmpty():

        current = frontier.pop()
        
        """check if it reach the goal state, if not, get the next state by the scuccessor"""
        if problem.isGoalState(current[0]):
            goal = current
            break 
        for next in problem.getSuccessors(current[0]):
            newCost = costSoFar[current[0]] + next[2]"add the cost"
            "if not been visted or the new cost less than current cost so far, push into search queue"
            if next[0] not in visited or newCost < costSoFar[next[0]]:
                costSoFar[next[0]] = newCost
                priority = newCost
                frontier.push(next, priority)
                cameFrom[next] = current
                visited[next[0]] = True
    "return path from goal to start"
    return backPath(problem, cameFrom, goal)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    """
    Initiation, 
    frontier: store the search path using priority queue.
    
    cameFrom list: store the path which the current state came from
    
    visited list: visited state

    costSoFar list: current cost list
    """

    frontier = util.PriorityQueue()
    startState = problem.getStartState()
    start = (startState, '', 0)
    goal = []
    frontier.push(start, 0)
    cameFrom = {}
    cameFrom[start] = None
    visited = {}
    visited[startState] = True
    costSoFar = {}
    costSoFar[startState] = 0

    while not frontier.isEmpty():
        current = frontier.pop()
        
        if problem.isGoalState(current[0]):
            goal = current
            break 
        for next in problem.getSuccessors(current[0]):
            newCost = costSoFar[current[0]] + next[2]
            "if not been visted or the new cost less than current cost so far, push into search queue"
            if next[0] not in visited or newCost < costSoFar[next[0]]:
                costSoFar[next[0]] = newCost

                """
                The cost in A* algorithm is: 
                the cost add heuristic cost 
                which represent the real distance from current point to the goal
                """
                priority = newCost + heuristic(next[0], problem)
                frontier.push(next, priority)
                
                cameFrom[next] = current
                visited[next[0]] = True

    return backPath(problem, cameFrom, goal)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
