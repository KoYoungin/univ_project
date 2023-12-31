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
        newFoodList = newFood.asList()          #newFoodList -> to calculate closest food
        distanceToClosestFood = 10000           #10000-> very big value for min dist
        score = successorGameState.getScore()   #for calculate and return

        if len(newFoodList) == 0:               #case for no food
            distanceToClosestFood = 0
        for food in newFoodList:                # Calculate distance to the closest food
            manFoodDist = util.manhattanDistance(food, newPos)
            if manFoodDist < distanceToClosestFood:
                distanceToClosestFood = manFoodDist

        # Calculate distance to the closest ghost
        distanceToClosestGhost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
        # Calculate scores based on the distance between pacman and ghost
        if distanceToClosestGhost <= 1:         #avoid ghosts when distance with ghost is smaller or equal than 1
            return -float("inf")  
        
        if distanceToClosestFood > 0:           #Eat foods!
            score += 1.0 / distanceToClosestFood
        if min(newScaredTimes) > 0 and distanceToClosestGhost > 0:
            score += 1.0 / distanceToClosestGhost  #Chase scared ghosts
            
        return score                            #return score calculated

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #1-> next action
        return self.minimaxOut(gameState, 0, self.depth)[1]
        
    def minValue(self, gameState, agentWho, depth):
        actions = []
        for action in gameState.getLegalActions(agentWho):
            #1 means ghost
            actions.append((self.minimaxOut(gameState.generateSuccessor(agentWho, action), agentWho + 1, depth)[0], action))
        return min(actions)
        
    def maxValue(self, gameState, agentWho, depth):
        actions = []
        for action in gameState.getLegalActions(agentWho):
            #1 means ghost
            actions.append((self.minimaxOut(gameState.generateSuccessor(agentWho, action), agentWho + 1, depth)[0], action))
        return max(actions)
    
    def minimaxOut(self, gameState, agentWho, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return (self.evaluationFunction(gameState), "Stop")
        #Because explore all depth, use recursive return   
        agentNum = gameState.getNumAgents()
        
        agentWho %= agentNum
        
        if agentWho == agentNum - 1:    #Like a cycle, if pacman and ghost's states updated once,
            depth -= 1                  #depth--.(loop again)
        
        if agentWho == 0:               #if pacman, return max, ghost min
            return self.maxValue(gameState, agentWho, depth)
        else:
            return self.minValue(gameState, agentWho, depth)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float("inf")       #for max value(best solution)
        beta = float("inf")        #for min value(worst solution)
        #[0] score, [1] action
        return self.alphaBetaPrune(gameState, 0, self.depth, alpha, beta)[1]
    
    def alphaBetaPrune(self, gameState, agentWho, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return (self.evaluationFunction(gameState), "Stop")
        
        agentNum = gameState.getNumAgents() #same as minimax
        
        agentWho %= agentNum
        
        if agentWho == agentNum - 1:    #Like a cycle, if pacman and ghost's states updated once,
            depth -= 1                  #depth--.(loop again)
        
        if agentWho == 0:               #almost same as minimax, only different alpha, beta
            return self.maxValue(gameState, agentWho, depth, alpha, beta)
        else:
            return self.minValue(gameState, agentWho, depth, alpha, beta)
    
    def maxValue(self, gameState, agentWho, depth, alpha, beta):
        actions = []
        for action in gameState.getLegalActions(agentWho):
            v, _ = self.alphaBetaPrune(gameState.generateSuccessor(agentWho, action), agentWho + 1, depth, alpha, beta)
            actions.append((v, action))
            if v > beta:            #different with minimax <- end calculate
                return (v, action)  # -> no calculate unnecessary operations
            alpha = max(alpha, v)   #update max alpha 
            
        return max(actions)
        
    def minValue(self, gameState, agentWho, depth, alpha, beta):
        actions = []
        for action in gameState.getLegalActions(agentWho):
            v, _ = self.alphaBetaPrune(gameState.generateSuccessor(agentWho, action), agentWho + 1, depth, alpha, beta)
            actions.append((v, action))
            if v < alpha:           # same as maxValue
                return (v, action)
            beta = min(beta, v)     #update min beta
            
        return min(actions)
        


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
