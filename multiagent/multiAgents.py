# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        score = 0
         
        minFoodDist = 1000000000000000
        newFoodPos = newFood.asList()
        for foodPos in newFoodPos:
            foodDist = util.manhattanDistance(foodPos, newPos)
            minFoodDist = min(foodDist, minFoodDist)
         
        score += 10.0 / minFoodDist
        
        minGhostDist = 1000000000000000
        for newGhostState in newGhostStates:
            newGhostDist = util.manhattanDistance(newGhostState.getPosition(), newPos)
            minGhostDist = min(minGhostDist, newGhostDist)
            
        score += minGhostDist
#         score += successorGameState.getScore()
#         print currentGameState.getScore()
#         print successorGameState.getScore()
#         print "###"
        score += successorGameState.getScore()
        if action == Directions.STOP:
            score += -5000
        return score
    
#    return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
 
    def maxValue(self, state, curDepth, curAgentIdx):
        maxVal = float('-Inf')
        maxAction = None
        for action in state.getLegalActions(self.pacmanIdx):
            curVal = self.val(state.generateSuccessor(self.pacmanIdx, action), curDepth, curAgentIdx + 1)
            if curVal[0] >= maxVal:
                maxAction = action
                maxVal = curVal[0]
        return (maxVal, maxAction)
 
    def minValue(self, state, curDepth, curAgentIdx):
        minVal = float('Inf')
        minAction = None
        for action in state.getLegalActions(curAgentIdx):
            curVal = self.val(state.generateSuccessor(curAgentIdx, action), curDepth, curAgentIdx + 1)
            if curVal[0] <= minVal:
                minAction = action
                minVal = curVal[0]
#         self.curDepth -= 1
        return (minVal, minAction)
      
    def val(self, state, curDepth, curAgentIdx):
        if(curAgentIdx >= self.agentsNum):
            curAgentIdx = 0
            curDepth += 1
        if state.isWin() or state.isLose() or curDepth > self.depth:
            return (self.evaluationFunction(state), None)
        if curAgentIdx == self.pacmanIdx:
            return self.maxValue(state, curDepth, curAgentIdx)
        else:
            return self.minValue(state, curDepth, curAgentIdx)
         
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
 
          Here are some method calls that might be useful when implementing minimax.
 
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
 
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
 
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        self.pacmanIdx = 0
#         self.curDepth = 0
        curDepth = 1
        curAgentIdx = 0
        self.agentsNum = gameState.getNumAgents()
        result = self.val(gameState, curDepth, curAgentIdx);
        return result[1]
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

#     def getAction(self, gameState):
#         """
#           Returns the minimax action using self.depth and self.evaluationFunction
#         """
#         "*** YOUR CODE HERE ***"
# #         util.raiseNotDefined()
    def maxValue(self, state, curDepth, curAgentIdx, alpha, beta):
        maxVal = float('-Inf')
        maxAction = None
        for action in state.getLegalActions(self.pacmanIdx):
            curVal = self.val(state.generateSuccessor(self.pacmanIdx, action), curDepth, curAgentIdx + 1, alpha, beta)
            if curVal[0] >= maxVal:
                maxAction = action
                maxVal = curVal[0]
            if maxVal > beta:
                return (maxVal, maxAction)
            alpha = max(alpha, maxVal)
        return (maxVal, maxAction)
 
    def minValue(self, state, curDepth, curAgentIdx, alpha, beta):
        minVal = float('Inf')
        minAction = None
        for action in state.getLegalActions(curAgentIdx):
            curVal = self.val(state.generateSuccessor(curAgentIdx, action), curDepth, curAgentIdx + 1, alpha, beta)
            if curVal[0] <= minVal:
                minAction = action
                minVal = curVal[0]
            if minVal < alpha:
                return (minVal, minAction)
            beta = min(beta, minVal)
#         self.curDepth -= 1
        return (minVal, minAction)
      
    def val(self, state, curDepth, curAgentIdx, alpha, beta):
        if(curAgentIdx >= self.agentsNum):
            curAgentIdx = 0
            curDepth += 1
        if state.isWin() or state.isLose() or curDepth > self.depth:
            return (self.evaluationFunction(state), None)
        if curAgentIdx == self.pacmanIdx:
            return self.maxValue(state, curDepth, curAgentIdx, alpha, beta)
        else:
            return self.minValue(state, curDepth, curAgentIdx, alpha, beta)
         
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
 
          Here are some method calls that might be useful when implementing minimax.
 
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
 
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
 
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        self.pacmanIdx = 0
#         self.curDepth = 0
        curDepth = 1
        curAgentIdx = 0
        self.agentsNum = gameState.getNumAgents()
        alpha = float('-Inf')
        beta = float('Inf')
        result = self.val(gameState, curDepth, curAgentIdx, alpha, beta);
        return result[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        agentNum = gameState.getNumAgents()-1
        evaluationFunction = self.evaluationFunction
        PacmanIndex = 0; 

        def expectimax(agent,depth,curState):

          if depth<=0:
            return evaluationFunction(curState)       

          if curState.isWin() == True:
            return evaluationFunction(curState)       

          successors = [curState.generateSuccessor(agent, action) for action in curState.getLegalActions(agent)]        

          if agent == PacmanIndex:
            value = float("-inf")
          else:
            value = 0       

          for successor in successors:        

            if agent == PacmanIndex:
              value = max(value,expectimax(1,depth,successor))
            else:
              if agent == agentNum:
                depth = depth - 1
                agent = -1        

              value += expectimax(agent+1, depth, successor)/float(len(successors))        

          return value

        """
        -------------------above is local expectimax function-----------------------------
        """
        
        bestValue = float("-inf")

        bestAction = []

        successors = [(action, gameState.generateSuccessor(PacmanIndex, action)) for action in gameState.getLegalActions(PacmanIndex)]

        for successor in successors:
          curValue = expectimax(1, self.depth, successor[1])
          if curValue > bestValue:
            bestValue = curValue
            bestAction = successor[0]

        return bestAction




def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    ghostState = currentGameState.getGhostStates()
    pacmanPos = currentGameState.getPacmanPosition()
    curScore = currentGameState.getScore()
    ghost_dis = 0
    
    for ghost in ghostState:
      ghost_dis += manhattanDistance(pacmanPos, ghost.getPosition())


    return curScore - float(ghost_dis)

# Abbreviation
better = betterEvaluationFunction

