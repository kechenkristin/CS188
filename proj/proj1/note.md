```
conda activate cs188
conda deactivate
```

### Q1-Q4
Searching algorithms, easy, but still have possibilities to optimize: using a generic function, passing data structure and functions as parameters to it.  

https://github.com/kechenkristin/CS188/blob/main/note/search.md  

### Q5
- pre knowledge(composition of search problem)
https://inst.eecs.berkeley.edu/~cs188/fa22/assets/lectures/cs188-fa22-lec01.pdf  
pay attention to slide 8 & 10  

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
1. Using a list of bool to record whether we have 
