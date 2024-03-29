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
import random
import math

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
    
def randomSearch ( problem ) :
    current = problem.getStartState () 
    solution = [] 
    while (not (problem.isGoalState(current))) :
      succ = problem.getSuccessors(current)
      no_of_successors = len(succ)
      random_succ_index = int(random.random() * no_of_successors)
      next = succ[random_succ_index]
      current = next[0]
      solution.append(next[1])
    print "The solution is ", solution
    return solution

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
    visited = []
    start_node = problem.getStartState()
    if problem.isGoalState(start_node):
        return []
    my_stack = util.Stack()
    my_stack.push((start_node, []))
    while not my_stack.isEmpty():
		curr_node, actions = my_stack.pop()
		if curr_node not in visited:
			visited.append(curr_node)
			if problem.isGoalState(curr_node):
				return actions
			for succesor, next_action, cost in problem.getSuccessors(curr_node):
				new_action = actions + [next_action]
				my_stack.push((succesor, new_action))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited = []
    start_node = problem.getStartState()
    if problem.isGoalState(start_node):
        return []
    my_queue = util.Queue()
    my_queue.push((start_node, []))
    while not my_queue.isEmpty():
		curr_node, actions = my_queue.pop()
		if curr_node not in visited:
			visited.append(curr_node)
			if problem.isGoalState(curr_node):
				return actions
			for succesor, next_action, cost in problem.getSuccessors(curr_node):
				new_action = actions + [next_action]
				my_queue.push((succesor, new_action))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = []
    start_node = problem.getStartState()
    if problem.isGoalState(start_node):
        return []
    my_priorityQ = util.PriorityQueue()
    my_priorityQ.push((start_node, [], 0), 0)
    while not my_priorityQ.isEmpty():
        curr_node, actions, cost = my_priorityQ.pop()
        if curr_node not in visited:
            visited.append(curr_node)
            if problem.isGoalState(curr_node):
                return actions
            for successor, next_action, next_cost in problem.getSuccessors(curr_node):
                new_action = actions + [next_action]
                priority = cost + next_cost
                my_priorityQ.push((successor, new_action, priority), priority)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = []
    start_node = problem.getStartState()
    if problem.isGoalState(start_node):
        return []
    my_priorityQ = util.PriorityQueue()
    my_priorityQ.push((start_node, [], 0), 0)
    while not my_priorityQ.isEmpty():
        curr_node, actions, p_cost = my_priorityQ.pop()
        if curr_node not in visited:
            visited.append(curr_node)
            if problem.isGoalState(curr_node):
                return actions
            for next, action, cost in problem.getSuccessors(curr_node):
                new_action = actions + [action]
                new_cost = p_cost + cost
                new_heuristic = new_cost + heuristic(next, problem)
                my_priorityQ.push((next, new_action, new_cost), new_heuristic)
    util.raiseNotDefined()
    
def greedy(problem, heuristic=nullHeuristic):
    start_node = problem.getStartState()
    visited = []
    if problem.isGoalState(start_node):
        return []
    my_priorityQ = util.PriorityQueue()
    my_priorityQ.push((start_node, [], 0), 0)
    while not my_priorityQ.isEmpty():
        curr_node, actions, p_cost = my_priorityQ.pop()
        if curr_node not in visited:
            visited.append(curr_node)
            if problem.isGoalState(curr_node):
                return actions
            for next, action, cost in problem.getSuccessors(curr_node):
                new_action = actions + [action]
                new_cost = p_cost + cost
                my_priorityQ.push((next, new_action, new_cost), heuristic(next, problem))
    util.raiseNotDefined()
    
def iterativeDeepeningSearch(problem):
    start_node = problem.getStartState()
    my_stack = util.Stack()
    my_stack.push((start_node, [], 0))
    deep= 0
    while not my_stack.isEmpty():
        deep += 1
        curr_node, actions, cost = my_stack.pop()
        visited = []
        visited.append(curr_node)
        while True:
            for succesor, next_action, next_cost in problem.getSuccessors(curr_node):
                if succesor not in visited and (cost + next_cost) <= deep:
                    visited.append(succesor)
                    my_stack.push((succesor, actions + [next_action], cost + next_cost))
            if my_stack.isEmpty():
                break
            curr_node, actions, cost = my_stack.pop()
            if problem.isGoalState(curr_node): 
                return actions
        my_stack.push((start_node, [], 0))
   



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
grd=greedy
idfs=iterativeDeepeningSearch
