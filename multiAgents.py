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
        # print "successorGameState: " + str(successorGameState)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        foodDistance = self.foodDistance(newPos, newFood)
        minFoodDistance = min(foodDistance) if foodDistance else 1000
        avgFoodDistance = sum(foodDistance)/float(len(foodDistance)) if foodDistance else 0
        avgFoodDistance = 1 if not avgFoodDistance else avgFoodDistance
        minGhostDistance = self.minGhostDistance(newPos, newGhostStates)
        minGhostDistance = 1 if not minGhostDistance else minGhostDistance
        getGhostScore = self.getGhostScore(newPos, newGhostStates)
        getGhostScore = 1 if not getGhostScore else getGhostScore
        a = successorGameState.getScore() if successorGameState.getScore() else 1
        # print a
        return 2.0/minGhostDistance + a + self.surroundingFood(newPos, newFood) + 10.0/avgFoodDistance

    def countRemainingFood(self, newFood):
        return sum([len(filter(lambda y: y, x)) for x in newFood])

    def getGhostScore(self, newPos, newGhostStates):
        total, distances = 0, []
        for ghostState in newGhostStates:
            ghostCoordinate = ghostState.getPosition()
            distances.append(manhattanDistance(newPos, ghostCoordinate))
            # approachingGhosts = len(filter(lambda x: x < 5, distances))
            # if approachingGhosts:
            #     return -10*approachingGhosts
        return sum(distances)

    def foodDistance(self, newPos, newFood):
        distances = []
        for x, row in enumerate(newFood):
            for y, column in enumerate(newFood[x]):
                if newFood[x][y]:
                    distances.append(manhattanDistance(newPos, (x,y)))
        return distances

    def surroundingFood(self, newPos, newFood):
        count = 0
        for x in range(newPos[0]-2, newPos[0]+2):
            for y in range(newPos[1]-2, newPos[1]+2):
                if (0 <= x and x < len(list(newFood))) and (0 <= y and y < len(list(newFood[1]))) and newFood[x][y]:
                    count += 1
        return count

    def minGhostDistance(self, newPos, newGhostStates):
        distances = []
        for ghostState in newGhostStates:
            ghostCoordinate = ghostState.getPosition()
            distances.append(manhattanDistance(newPos, ghostCoordinate))
        return min(distances)

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

        def value(state, index, depth):
          # print("index = " + str(index)+ " depth = " + str(depth))
          index = index%state.getNumAgents()
          print(index, depth)
          if state.isLose() or state.isWin() or depth == 0:
            print("EVALUATING LEAVES")
            #evaluate the leaves
            a = self.evaluationFunction(state)
            #print(a)
            return a
            # bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            # chosenIndex = random.choice(bestIndices)
            # return legalMoves[chosenIndex]
          if index%state.getNumAgents()==0:
            return max_val(state, index, depth-1)
          return min_val(state, index, depth-1)

        def max_val(state, index, depth):
          val = float("-inf")
          legalActions = state.getLegalActions(index)
          if len(legalActions)==0:
            return value(state,index,0)
          succState = [state.generateSuccessor(index, x) for x in legalActions]
          for each in succState:
            val = max(val, value(each, index+1, depth))
          return val

        def min_val(state, index, depth):
          val = float("inf")
          legalActions = state.getLegalActions(index)
          if len(legalActions)==0:
            return value(state,index,0)
          succState = [state.generateSuccessor(index, x) for x in legalActions]
          for each in succState:
            val = min(val, value(each, index+1, depth))
          return val

        print ("self.depth = " + str(self.depth))
        print ("agent#s = " + str(gameState.getNumAgents()))
        print (gameState.isLose())
        actions = gameState.getLegalActions
        return value(gameState,0, (self.depth*gameState.getNumAgents()))


        # def minimax(state, depth, index):
        #   if depth = 0 or state.isLose():
        #     print "evaluate leaves"
        #     return
        #   else:
        #     val = float("-inf")
        #     for _ in state.getNumAgents():
        #       val =
        #       for action in legalMoves:
        #         val = max(val, -minimax(action, depth-1, index%state.getNumAgents()))
        #       return val
        # return minimax(gameState, self.depth*gameState.getNumAgents(), 0)
        # return minimax(gameState,self.depth*gameState.getNumAgents())
        util.raiseNotDefined()

        # print("number of agents = " + str(gameState.getNumAgents()))
        # legalMoves = gameState.getLegalActions()
        # scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # bestScore = max(scores)
        # bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # chosenIndex = random.choice(bestIndices)
        # def maxvalue(state):
        #   v = float("-inf")
        #   x = gameState.generateSuccessor(0,)
        #   return v
        # def minvalue(state):
        #   v = float("inf")
        #   return v
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

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

