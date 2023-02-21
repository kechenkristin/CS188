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
from pacman import GameState

import math

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        "*** YOUR CODE HERE ***"
        #获取吃豆人的位置、豆子的位置和幽灵的状态
        newPos = currentGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        newGhostStates = currentGameState.getGhostStates()

    # 维护豆、幽灵、惊吓状态的幽灵三个值，以达到评价效果
        INF = 100000000.0
        WEIGHT_FOOD = 1.0  # 豆基础值
        WEIGHT_GHOST = -1.0  # 幽灵基值
        WEIGHT_SCARED_GHOST = 10.0  # 惊吓状态的幽灵基础值

    # 当然所有得分建立在基础分的基础上
        score = currentGameState.getScore()

    #计算最近的豆的影响
        distancesToFoodList = [util.manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]
        if len(distancesToFoodList) > 0:
            score += WEIGHT_FOOD / min(distancesToFoodList)
        else:
            score += WEIGHT_FOOD

    # 评价幽灵的影响
        for ghost in newGhostStates:
            distance = manhattanDistance(newPos, ghost.getPosition())
            if distance > 0:
            #分正常状态和惊吓状态
            #这里要考虑惊吓剩余时间
                if ghost.scaredTimer > 0:  #如果幽灵属于惊吓状态（可以吃掉幽灵）则增加权重
                    score += WEIGHT_SCARED_GHOST / distance
                else:
                    score += WEIGHT_GHOST / distance
            else:
                return -INF  #吃豆人死掉了
        return score

        # ghost
        """

        ghostDistances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates if ghost.scaredTimer == 0]
            minGhostDist = min(ghostDistances, default=100)

            if minGhostDist == 0:
                return -math.inf
            numFood = successorGameState.getNumFood()
            if numFood == 0:
                return math.inf

        """

        # foodVal
        foods = newFood.asList()
        foodDistances = [manhattanDistance(newPos, i) for i in foods]
        minFoodDist = min(foodDistances, default=0)


        
        danger = 1 / (minGhostDist - 0.8)
        profit = 1 / (minFoodDist + 0.5)
        score = -danger + profit
        return score

        # ghost place
        """
        for ghost in newGhostStates:
            distance = manhattanDistance(newPos, ghost.getPosition())
            if distance > 0:
                if ghost.scaredTimer > 0:
                    score += SCARED_GHOST / distance
                else:
                    score += GHOST / distance
            else:
                return -99999999
        """

        if len(newGhostStates) > 0:
            nearestGhost = min(ghosts)
            dangousScore = -1000 if nearestGhost < 2 else 0
            score += dangousScore

        totalScaredTime = sum([ghost.scaredTimer for ghost in newGhostStates])
        score += totalScaredTime

        return score


def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
