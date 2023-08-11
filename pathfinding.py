import pygame
import sys
from collections import deque
from random import randint
from settings import *
from cell import Cell
from bfs import BFS
from dfs import DFS
from mesagge import message

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.restart()

    def restart(self):
        self.algorithm = None
        self.algorithm_name = ''
        self.start_point = False
        self.end_point = False
        self.start = None
        self.grid_cells = [[Cell(col, row, self) for row in range(ROWS)] for col in range(COLS)]
        
    def draw(self):
        self.screen.fill(pygame.Color('black'))
        [[cell.update(self.screen) for cell in row] for row in self.grid_cells]
        
    def clean_grid(self):
        self.algorithm_name = ''
        for row in self.grid_cells:
            for cell in row:
                if cell.state == State.VISITED or cell.state == State.PATH:
                    cell.state = State.UNVISITED
        
    def random_seed(self):
        self.algorithm_name = ''
        self.start_point = False
        self.end_point = False
        self.start = None
        for row in self.grid_cells:
            for cell in row:
                if randint(0, 100) % 3 == 0:
                    cell.state = State.WALL
                else:
                    cell.state = State.UNVISITED
        
    def check_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.restart()
                elif event.key == pygame.K_1:
                    self.clean_grid()
                    self.find_start()
                    self.algorithm = BFS(self.grid_cells, self.start)
                    self.algorithm_name = 'BFS'
                elif event.key == pygame.K_2:
                    self.clean_grid()
                    self.find_start()
                    self.algorithm = DFS(self.grid_cells, self.start)
                    self.algorithm_name = 'DFS'
                elif event.key == pygame.K_0:
                    self.random_seed()
                    self.algorithm = None
                elif event.key == pygame.K_SPACE:
                    self.clean_grid()
                    self.algorithm = None
    
    def define_endpoints(self):
        if self.start_point == False and self.grid_cells[0][0].state != State.FINISH:
            self.grid_cells[0][0].state = State.START
            self.start_point = True
        elif self.start_point == False and self.grid_cells[-1][-1].state != State.FINISH:
            self.grid_cells[-1][-1].state = State.START
            self.start_point = True
        if self.end_point == False and self.grid_cells[-1][-1].state != State.START:
            self.grid_cells[-1][-1].state = State.FINISH
            self.end_point = True
        elif self.end_point == False and self.grid_cells[0][0].state != State.START:
            self.grid_cells[0][0].state = State.FINISH
            self.end_point = True
            
    def find_start(self):
        self.define_endpoints()
        for row in self.grid_cells:
            for cell in row:
                if cell.state == State.START:
                    self.start = cell
                    return
            
    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
        pygame.display.set_caption('Pathfinding algorithm')
        
    def run(self):
        while True:
            self.check_events()
            if self.algorithm != None:
                self.algorithm.update(self.screen)
            else:
                self.draw()
            message(self.algorithm_name)
            self.update()
        

if __name__ == '__main__':
    
    game = Game()
    game.run()