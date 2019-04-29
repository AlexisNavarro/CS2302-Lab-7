# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 07:57:25 2019

@author: Alexis Navarro
CS 2302
Olac Fuentes

Purpose: to find the path to solve the maze made from lab 6 and to use the graph functions.
"""

# -*- coding: utf-8 -*-



import matplotlib.pyplot as plt
import numpy as np
import random

#import datetime # need to use datetime instead of time because when using time, I would always get 0 for my running time when the size of my maze was too small
                # datetime is more precise for smaller mazes when being tested
import time


    
#GIVEN FUNCTIONS (PROVIDED BY CS 2302)

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1
        
def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])



def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j) 
    if ri!=rj: # Do nothing if i and j belong to the same set 
        S[rj] = ri  # Make j's root point to i's root
        
def findC(S,i):
    if S[i]<0:
        return i
    r = findC(S,S[i])
    S[i]=r
    return r   

#combines the two set by using their size as reference
def union_by_Size(S,i,j):
    ri = findC(S,i)
    rj = findC(S,j)
    if ri!=rj: # Do nothing if i and j belong to the same set 
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri
   
#------------------------------------------------------------------------------
#MADE METHOD/FUNCTION REQUIRED TO ACCOMPLISH THE LAB
            
#method to count the amount of sets in the DSF
def setAmount(S):
    count=0
    for i in range(len(S)):
        if S[i]<0:
            count +=1
    return count


def removeC(S,maze_walls,numSets):
    while numSets > 1:
        w = random.choice(maze_walls)# w gets the wall that was randomly selected
        i=maze_walls.index(w)#gets the position where we chose the wall to delete
        if find(S,w[0]) != find(S,w[1]):
            maze_walls.pop(i) #deletes the wall
            union_by_Size(S,w[0],w[1])# combines the walls after the deletion
            numSets-=1
    return w
#------------------------------------------------------------------------------
#METHOD TO DRAW THE MAZE (PROVIDED BY THE CS2302)
def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)


    
def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w

#------------------------------------------------------------------------------
#Lab 7 Code

#Method to find the cells in the maze
def cellsAmount(S):
    count = 0
    if S is None:
        return 0
    for i in S:
        count+=1
    return count

#Method  where n displays the number of cells and m is the amount  of walls the user wants to remove
def display_numCells(n,m):
    if m < n-1:
        print('Path does not Exist')
    elif m == n-1:
        print('Unique path Exists')
    elif m > n-1:
        print('There is atleast one path from the source to destination')
        
'''
def graph_toList(S,original,maze_walls,numCells, duplicate=False):
    adj=[] #empty adjacency List
    
    for i in range(numCells):   #traverse throught the amount of cells in maze_walls
        if original[i] in maze_walls:
            adj.append(original)
    return  adj
'''

#made a class that will create the funcitions to make a graoh
class Graph:
    def __init__(self,vertices):
        self.vertices = vertices
        self.graph = []
        for v in range(vertices):
            self.graph.append([])
     
 #  method to create the adjacency List its also a method that applies to this lab better
 #  unlike the graph to list method
def addEdge(G,v1,v2):
    G.graph[v1].append(v2)

#method to use Breadth First Search
def Breadth_FirstSearch(adjList,v):
    visited= [False]*(len(adjList.graph))
   
    Q=[]
    Q.append(v)
    visited[v]=True
    
    while Q:
        v = Q.pop(0)
        print(v,end=" ")
        
        for i in adjList.graph[v]:
            if visited[i]==False:
                Q.append(i)
                visited[i]=True
   
#method to use depth First Search
def dfs(adjList, startNode):
    visited=[]
    stack = [startNode]
    while stack:
        startNode=stack.pop()
        visited.append(startNode)
        print(startNode,end=" ")
        
        for i in adjList.graph[startNode]:
            stack.append(i)
    return visited
        
#method to use depth First Search with recursion
def dfs2(adjList,startNode, visited = None):
    if visited is None:
        visited = []
    visited.append(startNode)
    for i in adjList.graph[startNode]:
        if i not in visited:
            dfs2(adjList,i,visited)
    return visited


plt.close("all") 
#------------------------------------------------------------------------------
#MAIN

#size of rows and columns (Dimensions of the maze)
#Various sizes to test
maze_rows = 10    # use datetime for these dimensions since they are smaller
maze_cols = 15

#maze_rows = 20 # for bigger maze dimensions use time import
#maze_cols = 25

#maze_rows = 40
#maze_cols = 45

#maze_rows = 2
#maze_cols = 4
adjList=Graph(maze_rows*maze_cols)

x=input('Input the amount of walls you want to remove from the maze: ') # ask for users input to remove the walls
numRemove=int(x) # convert the string input into a integer
numRemove+=1

maze_walls = wall_list(maze_rows,maze_cols)#Gets the list of walls in the maze

draw_maze(maze_walls,maze_rows,maze_cols,cell_nums=True) #calls the draw maze method and makes the complete maze without deletion

S = DisjointSetForest(maze_rows*maze_cols)# makes the new DSF by combining the rows and columns


numCells=cellsAmount(S) # cells amount of the dsf

#numSets=setAmount(S)

display_numCells(numCells,numRemove) # question 1

# The remove walls method had to be moved to the main in order to be able to function with the search methods
while numRemove > 0:
    w = random.choice(maze_walls)# w gets the wall that was randomly selected
    i=maze_walls.index(w)#gets the position where we chose the wall to delete
    if find(S,w[0]) != find(S,w[1]):
        maze_walls.pop(i) #deletes the wall
        union(S,w[0],w[1])# combines the walls after the deletion
        addEdge(adjList,w[0],w[1]) # used to create the adjacency List (question 2)
        numRemove-=1
        
draw_maze(maze_walls,maze_rows,maze_cols)

print(adjList.graph) # use this to print the graph with the adjacency List


#Question 3
start_Time1=time.time()
print('\nBreadth First Search')
Breadth_FirstSearch(adjList,0)
end_Time1=time.time()
print('\nRunning time Breadth First Search: %s '%(end_Time1-start_Time1))



start_Time2=time.time()
print('\n\nDepth First Search ')
dfs(adjList,0)
end_Time2=time.time()
print('\nRunning time Depth First Search: %s '%(end_Time2-start_Time2))



start_Time3=time.time()
print('\n\n Depth First Search with Recursion')
print(dfs2(adjList,0))
end_Time3=time.time()
print('Running time Depth First Search with Recursion: %s '%(end_Time3-start_Time3))

