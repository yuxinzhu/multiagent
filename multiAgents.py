# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

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
        if "Stop" in legalMoves:
            legalMoves.remove("Stop")

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

        minGhostDistance = self.minGhostDistance(newPos, newGhostStates)
        score = successorGameState.getScore()
        surroundingFood = self.surroundingFood(newPos, newFood)
        avgFoodDistance = self.avgFoodDistance(newPos, newFood)
        return 2.0/minGhostDistance + score + surroundingFood + 10.0/avgFoodDistance

    def avgFoodDistance(self, newPos, newFood):
        distances = []
        for x, row in enumerate(newFood):
            for y, column in enumerate(newFood[x]):
                if newFood[x][y]:
                    distances.append(manhattanDistance(newPos, (x,y)))
        avgDistance = sum(distances)/float(len(distances)) if (distances and sum(distances) != 0) else 1
        return avgDistance

    def surroundingFood(self, newPos, newFood):
        count = 0
        for x in range(newPos[0]-2, newPos[0]+3):
            for y in range(newPos[1]-2, newPos[1]+3):
                if (0 <= x and x < len(list(newFood))) and (0 <= y and y < len(list(newFood[1]))) and newFood[x][y]:
                    count += 1
        return count

    def minGhostDistance(self, newPos, newGhostStates):
        distances = []
        for ghostState in newGhostStates:
            ghostCoordinate = ghostState.getPosition()
            distances.append(manhattanDistance(newPos, ghostCoordinate))
        if distances and min(distances) != 0:
            return min(distances)
        return 1

def manhattanDistance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

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


        def maximizer(state, depth=0):
          if state.isLose() or state.isWin() or depth == 0:
            #evaluate the leaves
            return self.evaluationFunction(state)
          val = float("-inf")
          legalActions = state.getLegalActions()
          succState = [state.generateSuccessor(0,x) for x in legalActions]
          for each in succState:
            val = max(val, minimizer(each, depth, state.getNumAgents()-1))
          return val


        def minimizer(state, depth=0, index=0):
          if state.isLose() or state.isWin() or depth == 0:
            #evaluate the leaves
            return self.evaluationFunction(state)
          val = float("inf")
          legalActions = state.getLegalActions(index)
          succState = [state.generateSuccessor(index, x) for x in legalActions]
          for each in succState:
            if index > 1:
              val = min(val, minimizer(each, depth, index-1))
            else:
              val = min(val, maximizer(each, depth-1))
          return val


        legalActions = gameState.getLegalActions()
        move = Directions.STOP
        val = float("-inf")
        for action in legalActions:
          tmp = minimizer(gameState.generateSuccessor(0,action), self.depth, gameState.getNumAgents()-1)
          if tmp > val:
            val = tmp
            move = action
        return move



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def maximizer(state, depth, a, b):
          if state.isLose() or state.isWin() or depth == 0:
            #evaluate the leaves
            return self.evaluationFunction(state)    
          val = float("-inf")
          legalActions = state.getLegalActions()
          succState = [state.generateSuccessor(0,x) for x in legalActions]
          for each in succState:
            val = max(val, minimizer(each, depth, state.getNumAgents()-1, a, b))
            if val > b:
              return val
            a = max(a, val)
          return val


        def minimizer(state, depth, index, a, b):
          if state.isLose() or state.isWin() or depth == 0:
            #evaluate the leaves
            return self.evaluationFunction(state)          
          val = float("inf")
          legalActions = state.getLegalActions(index)
          succState = [state.generateSuccessor(index, x) for x in legalActions]
          for each in succState:
            if index > 1:
              val = min(val, minimizer(each, depth, index-1, a, b))
            else:
              val = min(val, maximizer(each, depth-1, a, b))
            if val < a:
              return val
            b = min(b, val)
          return val

          
        legalActions = gameState.getLegalActions()
        move = Directions.STOP
        val = float("-inf")
        a = float("-inf")
        b = float("inf")
        for action in legalActions:
          tmp = minimizer(gameState.generateSuccessor(0,action), self.depth, gameState.getNumAgents()-1, a, b)
          if tmp>val:
            val = tmp
            move = action
          if val > b:
            return value
          a = max(a,val)
        return move



        util.raiseNotDefined()

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
        def maximizer(state, depth=0):
            if state.isLose() or state.isWin() or depth == 0:
                #evaluate the leaves
                return self.evaluationFunction(state)
            val = float("-inf")
            legalActions = state.getLegalActions()
            succState = [state.generateSuccessor(0,x) for x in legalActions]
            for each in succState:
                val = max(val, minimizer(each, depth, state.getNumAgents()-1))
            return val


        def minimizer(state, depth=0, index=0):
          if state.isLose() or state.isWin() or depth == 0:
            #evaluate the leaves
            return self.evaluationFunction(state)
          val = float("inf")
          legalActions = state.getLegalActions(index)
          succState = [state.generateSuccessor(index, x) for x in legalActions]
          temp = 0
          for each in succState:
            if index > 1:
              temp += minimizer(each, depth, index-1)
            else:
              temp += maximizer(each, depth-1)
          return float(temp)/len(succState)


        legalActions = gameState.getLegalActions()
        move = Directions.STOP
        val = float("-inf")
        for action in legalActions:
          tmp = minimizer(gameState.generateSuccessor(0,action), self.depth, gameState.getNumAgents()-1)
          if tmp > val:
            val = tmp
            move = action
        return move


def countRemainingFood(newFood):
    return sum([len(filter(lambda y: y, x)) for x in newFood])

def getGhostScore(newPos, newGhostStates):
    total, distances = 0, []
    for ghostState in newGhostStates:
        ghostCoordinate = ghostState.getPosition()
        distances.append(manhattanDistance(newPos, ghostCoordinate))
        # approachingGhosts = len(filter(lambda x: x < 5, distances))
        # if approachingGhosts:
        #     return -10*approachingGhosts
    return sum(distances)

def avgFoodDistance(newPos, newFood):
    distances = []
    for x, row in enumerate(newFood):
        for y, column in enumerate(newFood[x]):
            if newFood[x][y]:
                distances.append(manhattanDistance(newPos, (x,y)))
    avgDistance = sum(distances)/float(len(distances)) if (distances and sum(distances) != 0) else 1
    return avgDistance

def surroundingFood(newPos, newFood):
    count = 0
    for x in range(newPos[0]-2, newPos[0]+3):
        for y in range(newPos[1]-2, newPos[1]+3):
            if (0 <= x and x < len(list(newFood))) and (0 <= y and y < len(list(newFood[1]))) and newFood[x][y]:
                count += 1
    return count

def minGhostDistance(newPos, newGhostStates):
    distances = []
    for ghostState in newGhostStates:
        ghostCoordinate = ghostState.getPosition()
        distances.append(manhattanDistance(newPos, ghostCoordinate))
    if distances and min(distances) != 0:
        return min(distances)
    return 1

def betterEvaluationFunction(currentGameState):
    """
        Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
        evaluation function (question 5).

        DESCRIPTION: betterEvalulationFunction consists primarily of four features:
        1) The inverse of the distance to the closest ghost
        2) The current score
        3) The number of food pellets surrounding Pacman within 2 on each direction
        4) The inverse of the average distance to all food pellets
    """
    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    currentGhostStates = currentGameState.getGhostStates()

    return (
        2.0/minGhostDistance(currentPos, currentGhostStates) + currentGameState.getScore() +
        surroundingFood(currentPos, currentFood) + 10.0/avgFoodDistance(currentPos, currentFood)
    )

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

