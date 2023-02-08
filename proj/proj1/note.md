```
conda activate cs188
conda deactivate
```

## Q1-Q4
Searching algorithms, easy, but still have possibilities to optimize: using a generic function, passing data structure and functions as parameters to it.  

https://github.com/kechenkristin/CS188/blob/main/note/search.md  

## Q5
- pre knowledge(composition of search problem)  
![avatar](https://github.com/kechenkristin/cs188/blob/main/img/p1/s1.png)


![avatar](https://github.com/kechenkristin/cs188/blob/main/img/p1/s2.png)

- idea  
Define a data structure to represent searching corner problem, because it's about the corners, so have nothing to do other irrelevant info(i.e. the position of ghosts, where extra food is).  

The data structure we defined should contain: the current position of pacman, info about the corners.  

Now two questions arises:  
1. how to represent the data strcture
2. how to represent the info of corners

For 1, the initial idea is to define a class like
```python
class CornerState:
     def __init__(self, pacmanPosition, unvisitedCorners):
         self.pacmanPosition = pacmanPosition
         self.unvisitedCorners = unvisitedCorners
```

Personally, I think this could work, but for some reasons, it couldn't run on my laptop. Luckily, python is a very flexible language, so we can use a build-in data structure to do the same functionality. 

Since a state is deterministic, and we need something easy to access the value using index,so we use a tuple(indexed, ordered, immutable).  
So now we have:
```python
cornerstate = (pacmanPosition, corners)
```

For 2, I can think of two ways to implement it:
1. Using a tuple to record the corner we haven't yet.  
2. Using a list of bool to record whether we have visited a corner or not  

Let's focus on way1 first.
- init
```python
class CornersProblem(search.SearchProblem):
    def __init__(self, startingGameState: pacman.GameState):
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0 # DO NOT CHANGE; Number of search nodes expanded
        "*** YOUR CODE HERE ***"
        self.startState = (self.startingPosition, self.corners)
```

- getStartState  
easy, simply return self.startState

- isGoalState  

Since self.startState[1] records the corners we haven't visited yet, so when we reach the goal, that means we have vivisted all the corners, so startState[1] should be empty, now we can define:

```python
    def isGoalState(self, state: Any):
        """
        Returns whether this search state is a goal state of the problem.
        """
        "*** YOUR CODE HERE ***"
        return len(state[1]) == 0
```

- getSuccessors  
This method should return a new state, so we need to   
(1)update the newPosition   
(2)update the info of visited corners.    

We now have the next position, so just need to think about(2), if the nextPosition equals to one of the corners we haven't visited yet, remove it.  

```python
def getSuccessors(self, state: Any):
        successors = []

        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST,     Directions.WEST]:
            "*** YOUR CODE HERE ***"
            x,y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]
            if not hitsWall:
                nextPosition = (nextx, nexty)
                nextUnvisitedCorner = []
                for i in state[1]:
                    if not i == nextPosition:
                        nextUnvisitedCorner.append(i)

                nextState = (nextPosition, tuple(nextUnvisitedCorner))
                successors.append((nextState, action, 1))

        self._expanded += 1 # DO NOT CHANGE
        return successors
```

There are also other ways: 
```python
 if not hitsWall:
                nextPosition = (nextx, nexty)
                cornerLst = list(state[1])
                for i in cornerLst:
                    if nextPosition == i:
                        cornerLst.remove(i)

                nextState = (nextPosition, tuple(cornerLst))
                successors.append((nextState, action, 1)) 

```

For 2. Using a list of bool to record whether we have visited a corner or not, it's bascically the similar idea, I won't discuss it in detail.  

## Q6
![avatar](https://github.com/kechenkristin/cs188/blob/main/img/p1/a1.png)
This task asks us to implement a heuristic funtion for corner problem, ucb's question is really useful:  

Admissibility vs. Consistency: Remember, heuristics are just functions that take search states and return numbers that estimate the cost to a nearest goal. More effective heuristics will return values closer to the actual goal costs. To be admissible, the heuristic values must be lower bounds on the actual shortest path cost to the nearest goal (and non-negative). To be consistent, it must additionally hold that if an action has cost c, then taking that action can only cause a drop in heuristic of at most c.  

Remember that admissibility isn’t enough to guarantee correctness in graph search – you need the stronger condition of consistency. However, admissible heuristics are usually also consistent, especially if they are derived from problem relaxations. Therefore it is usually easiest to start out by brainstorming admissible heuristics. Once you have an admissible heuristic that works well, you can check whether it is indeed consistent, too. The only way to guarantee consistency is with a proof. However, inconsistency can often be detected by verifying that for each node you expand, its successor nodes are equal or higher in in f-value. Moreover, if UCS and A Star ever return paths of different lengths, your heuristic is inconsistent. This stuff is tricky!    

Remember, manhattan distance is a concrete implementation of heristic function, and the util.py provides it.

```python
def manhattanDistance( xy1, xy2 ):      
     "Returns the Manhattan distance between points xy1 and xy2"             
     return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )     
```

According to Semi-Lattice of Heuristics:
![avatar](https://github.com/kechenkristin/cs188/blob/main/img/p1/a2.png)


```python
def cornersHeuristic(state: Any, problem: CornersProblem):
    corners = problem.corners # These are the corner coordinates
    walls = problem.walls # These are the walls of the maze, as a Grid (game.py)
    distance = 0
    for corner in state[1]:
        distance = max(distance, util.manhattanDistance(state[0], corner))
    return distance # Default to trivial solution
```

## Q7
![avatar](https://github.com/kechenkristin/cs188/blob/main/img/p1/c1.png)
This task also asks us to implement a heristic funtion, but should satisfy consistancy, 
my implementation is:
```python
def foodHeuristic(state: Tuple[Tuple, List[List]], problem: FoodSearchProblem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can  
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state
    "*** YOUR CODE HERE ***"
    distance = 0
    foods = foodGrid.asList()
    for food in foods:
        distance = max(distance, util.manhattanDistance(position, food))
    return distance # Default to trivial solution
```
Admissible, but not consistancy, still need to improve in the future

## Q8
easy  
```python
    def findPathToClosestDot(self, gameState: pacman.GameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

```

```python
def isGoalState(self, state: Tuple[int, int]):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state

        "*** YOUR CODE HERE ***"
        return self.food[x][y]

```
