import pygame
from settings import *
from queue import PriorityQueue

class A_Star:
    def __init__(self, grid, start, end):
        self.count = 0
        self.grid = grid
        self.start = start
        self.current = self.start
        self.end = end
        self.not_found = True
        
        self.queue = PriorityQueue()
        self.queue.put((0, self.count, self.start))
        self.g_score = {cell: float('inf') for row in grid for cell in row}
        self.g_score[self.start] = 0
        self.f_score = {cell: float('inf') for row in grid for cell in row}
        self.f_score[start] = self.claculate_manhatan_distance(self.start, self.end)
        self.previous_nodes = {}
        self.visited_nodes = set()
        self.visited_nodes.add(self.start)
               
    def claculate_manhatan_distance(self, current, end):
        dx = abs(end.x - current.x)
        dy = abs(end.y - current.y)
        return dx + dy
    
    def reconstruct_path(self):
        while self.current in self.previous_nodes:
            self.current = self.previous_nodes[self.current]
            if self.current.state not in [State.START, State.FINISH]:
                self.current.state = State.PATH
    
    def A_star(self):
         
        if not self.queue.empty():
            self.current = self.queue.get()[2]
            self.visited_nodes.remove(self.current)
            
            if self.current == self.end:
                self.not_found = False
                self.reconstruct_path()
            else:
                neighbours = self.get_neighbours(self.current)
                for neighbour in neighbours:
                    temp_g_score = self.g_score[self.current] + 1
                    
                    if temp_g_score < self.g_score[neighbour]:
                        self.previous_nodes[neighbour] = self.current
                        self.g_score[neighbour] = temp_g_score
                        self.f_score[neighbour] = temp_g_score + self.claculate_manhatan_distance(neighbour, self.end)
                        
                    if neighbour not in self.visited_nodes:
                        self.count += 1
                        self.queue.put((self.f_score[neighbour], self.count, neighbour))
                        self.visited_nodes.add(neighbour)
                        if neighbour.state == State.UNVISITED:
                            neighbour.state = State.VISITED
                 
    def get_neighbours(self, curr):
        neighbours = []
        if curr.x - 1 >= 0:
            if self.grid[curr.x - 1][curr.y].state in [State.UNVISITED, State.FINISH]:
                neighbours.append(self.grid[curr.x - 1][curr.y])
        if curr.y - 1 >= 0:
            if self.grid[curr.x][curr.y - 1].state in [State.UNVISITED, State.FINISH]:
                neighbours.append(self.grid[curr.x][curr.y - 1])
        if curr.x + 1 < COLS:
            if self.grid[curr.x + 1][curr.y].state in [State.UNVISITED, State.FINISH]:
                neighbours.append(self.grid[curr.x + 1][curr.y])
        if curr.y + 1 < ROWS:
            if self.grid[curr.x][curr.y + 1].state in [State.UNVISITED, State.FINISH]:
                neighbours.append(self.grid[curr.x][curr.y + 1])
             
        return neighbours
             
             
    def update(self, screen):
        if self.not_found:
            self.A_star()
        
        for row in self.grid:
            for cell in row:
                cell.draw(screen)