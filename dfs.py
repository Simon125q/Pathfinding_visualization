from settings import *
import pygame
from random import choice

class DFS:
    def __init__(self, grid, start_node):
        self.graph = grid
        self.start_node = start_node
        self.stack = []
        self.path = []
        self.current_cell = self.start_node
        self.not_found = True
        
    def check_neighbours(self, curr):
        neighbours = []
        if curr.x - 1 >= 0 and self.graph[curr.x - 1][curr.y].state in [State.UNVISITED, State.FINISH]:
            neighbours.append(self.graph[curr.x - 1][curr.y])
            
        if curr.y - 1 >= 0 and self.graph[curr.x][curr.y - 1].state in [State.UNVISITED, State.FINISH]:
            neighbours.append(self.graph[curr.x][curr.y - 1])
            
        if curr.x + 1 < COLS and self.graph[curr.x + 1][curr.y].state in [State.UNVISITED, State.FINISH]:
            neighbours.append(self.graph[curr.x + 1][curr.y])
            
        if curr.y + 1 < ROWS and self.graph[curr.x][curr.y + 1].state in [State.UNVISITED, State.FINISH]:
            neighbours.append(self.graph[curr.x][curr.y + 1])
            
        return choice(neighbours) if neighbours else False
           
    
    def DFS(self):
         
        self.next_cell = self.check_neighbours(self.current_cell)
        
        if self.next_cell and self.next_cell.state == State.FINISH:
            self.stack.append(self.current_cell)
            for cell in self.stack:
                if cell.state not in [State.FINISH, State.START]:
                    cell.state = State.PATH
            self.not_found = False
        elif self.next_cell:
            self.next_cell.state = State.VISITED
            self.stack.append(self.current_cell)
            self.current_cell = self.next_cell
        elif self.stack:
            self.current_cell = self.stack.pop()
            self.current_cell.state = State.VISITED
            
    def update(self, screen):
        if self.not_found:
            self.DFS()
        
        for row in self.graph:
            for cell in row:
                cell.draw(screen)