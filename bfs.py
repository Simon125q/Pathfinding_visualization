import pygame
from collections import deque
from settings import *


class BFS:
    def __init__(self, grid, start_node):
        self.graph = grid
        self.start_node = start_node
        self.queue = deque()
        self.queue.append(self.start_node)
        self.previous_nodes = {}
    
    def append_neighbours(self, curr):
        if curr.x - 1 >= 0:
            self.queue.append(self.graph[curr.x - 1][curr.y])
            if self.graph[curr.x - 1][curr.y] not in self.previous_nodes:
                self.previous_nodes[self.graph[curr.x - 1][curr.y]] = curr
        if curr.y - 1 >= 0:
            self.queue.append(self.graph[curr.x][curr.y - 1])
            if self.graph[curr.x][curr.y - 1] not in self.previous_nodes:
                self.previous_nodes[self.graph[curr.x][curr.y - 1]] = curr
        if curr.x + 1 < COLS:
            self.queue.append(self.graph[curr.x + 1][curr.y])
            if self.graph[curr.x + 1][curr.y] not in self.previous_nodes:
                self.previous_nodes[self.graph[curr.x + 1][curr.y]] = curr
        if curr.y + 1 < ROWS:
            self.queue.append(self.graph[curr.x][curr.y + 1])
            if self.graph[curr.x][curr.y + 1] not in self.previous_nodes:
                self.previous_nodes[self.graph[curr.x][curr.y + 1]] = curr
    
    def BFS(self):
         
         if self.queue:
             curr = self.queue.popleft()
             if curr.state == State.FINISH:
                 self.backtrack(curr)
                 self.queue = deque()
             elif curr.state == State.UNVISITED:
                 curr.state = State.VISITED
                 self.append_neighbours(curr)
             elif curr.state == State.START:
                 self.append_neighbours(curr)
                 
    def backtrack(self, node):
        if node == self.start_node or node not in self.previous_nodes:
            return
        prev_node = self.previous_nodes[node]
        prev_node.state = State.PATH
        self.backtrack(prev_node)
        
             
    def update(self, screen):
        self.BFS()
        
        for row in self.graph:
            for cell in row:
                cell.draw(screen)
        
