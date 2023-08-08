import pygame
import sys
from collections import deque
from settings import *
from cell import Cell
from bfs import BFS

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.restart()

    def restart(self):
        self.BFS = None
        self.start_point = False
        self.end_point = False
        self.start = None
        self.grid_cells = [[Cell(col, row, self) for row in range(ROWS)] for col in range(COLS)]
        #self.grid_cells = [[0]*COLS]*ROWS
        #for row in range(ROWS):
        #    for col in range(COLS):
        #        self.grid_cells[row][col] = Cell(col, row, self)
        
    def draw(self):
        self.screen.fill(pygame.Color('black'))
        [[cell.update(self.screen) for cell in row] for row in self.grid_cells]
        """ for row in self.grid_cells:
            for cell in row:
                cell.update(self.screen)"""
        
    def clean_grid(self):
        for row in self.grid_cells:
            for cell in row:
                if cell.state == State.VISITED or cell.state == State.PATH:
                    cell.state = State.UNVISITED
        
    def check_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.restart()
                elif event.key == pygame.K_SPACE:
                    self.clean_grid()
                    self.find_start()
                    self.BFS = BFS(self.grid_cells, self.start)
    
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
    
    def BFSw(self):
        self.find_start()
        self.clean_grid()
        queue = deque()
        queue.append(self.start)
        
        while queue:
            curr = queue.popleft()
            if curr.state == State.FINISH:
                break
            elif curr.state == State.UNVISITED:
                curr.state = State.VISITED
                if curr.x - 1 >= 0:
                    queue.append(self.grid_cells[curr.x - 1][curr.y])
                if curr.y - 1 >= 0:
                    queue.append(self.grid_cells[curr.x][curr.y - 1])  
                if curr.x + 1 < COLS:
                    queue.append(self.grid_cells[curr.x + 1][curr.y])    
                if curr.y + 1 < ROWS:
                    queue.append(self.grid_cells[curr.x][curr.y + 1])
            elif curr.state == State.START:
                if curr.x - 1 >= 0:
                    queue.append(self.grid_cells[curr.x - 1][curr.y])
                if curr.y - 1 >= 0:
                    queue.append(self.grid_cells[curr.x][curr.y - 1])  
                if curr.x + 1 < COLS:
                    queue.append(self.grid_cells[curr.x + 1][curr.y])    
                if curr.y + 1 < ROWS:
                    queue.append(self.grid_cells[curr.x][curr.y + 1])
                
            self.update()
            
    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
        pygame.display.set_caption('Pathfinding algorithm')
        
    def run(self):
        while True:
            self.check_events()
            if self.BFS != None:
                self.BFS.update(self.screen)
            else:
                self.draw()
            self.update()
        

if __name__ == '__main__':
    
    game = Game()
    game.run()