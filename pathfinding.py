import pygame
import sys
from collections import deque
RES = WIDTH, HEIGHT = (1200, 800)
FPS = 100
TILE = 30
ROWS = HEIGHT // TILE
COLS = WIDTH // TILE


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.restart()

    def restart(self):
        self.start_point = 0
        self.end_point = 0
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
                if cell.state == 'visited':
                    cell.state = 'not_visited'
        
    def check_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.restart()
                elif event.key == pygame.K_SPACE:
                    self.BFS()
    
    def define_endpoints(self):
        if self.start_point == 0 and self.grid_cells[0][0].state != 'end':
            self.grid_cells[0][0].state = 'start'
            self.start_point = 1
        elif self.start_point == 0 and self.grid_cells[-1][-1].state != 'end':
            self.grid_cells[-1][-1].state = 'start'
            self.start_point = 1
        if self.end_point == 0 and self.grid_cells[-1][-1].state != 'start':
            self.grid_cells[-1][-1].state = 'end'
            self.end_point = 1
        elif self.end_point == 0 and self.grid_cells[0][0].state != 'start':
            self.grid_cells[0][0].state = 'end'
            self.end_point = 1
            
    def find_start(self):
        self.define_endpoints()
        for row in self.grid_cells:
            for cell in row:
                if cell.state == 'start':
                    self.start = cell
                    return
    
    def BFS(self):
        self.find_start()
        self.clean_grid()
        queue = deque()
        queue.append(self.start)
        
        while queue:
            curr = queue.popleft()
            if curr.state == 'end':
                break
            
            if curr.x - 1 >= 0 and self.grid_cells[curr.x - 1][curr.y].state == 'not_visited':
                queue.append(self.grid_cells[curr.x - 1][curr.y])
                self.grid_cells[curr.x - 1][curr.y].state = 'visited'
            if curr.y - 1 >= 0 and self.grid_cells[curr.x][curr.y - 1].state == 'not_visited':
                queue.append(self.grid_cells[curr.x][curr.y - 1])
                self.grid_cells[curr.x][curr.y - 1].state = 'visited'
            if curr.x + 1 < COLS and self.grid_cells[curr.x + 1][curr.y].state == 'not_visited':
                queue.append(self.grid_cells[curr.x + 1][curr.y])
                self.grid_cells[curr.x + 1][curr.y].state = 'visited'
            if curr.y + 1 < ROWS and self.grid_cells[curr.x][curr.y + 1].state == 'not_visited':
                queue.append(self.grid_cells[curr.x][curr.y + 1])
                
            self.update()
            
    def update(self):
        self.check_events()
        self.draw()
        pygame.display.flip()
        self.clock.tick(FPS)
        pygame.display.set_caption('Pathfinding algorithm')
        
    def run(self):
        while True:
            self.update()
        
class Cell:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x * TILE, self.y * TILE, TILE - 2, TILE - 2))
        self.state = 'not_visited'
        self.click_time = 0
        self.click_cooldown = 200
        self.can_click = True
        self.game = game
        
    def draw(self, screen):
        
        if self.state == 'not_visited':
            pygame.draw.rect(screen, pygame.Color('white'), self.rect, border_radius = 7)
        elif self.state == 'visited':
            pygame.draw.rect(screen, pygame.Color('blue'), self.rect, border_radius = 7)
        elif self.state == 'wall':
            pygame.draw.rect(screen, pygame.Color('red'), self.rect, border_radius = 7)
        elif self.state == 'start':
            pygame.draw.rect(screen, pygame.Color('green'), self.rect, border_radius = 7)
        elif self.state == 'end':
            pygame.draw.rect(screen, pygame.Color('gold'), self.rect, border_radius = 7)
            
    def check_click(self):
        global endpoints
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and self.can_click:
                self.can_click = False
                self.click_time = pygame.time.get_ticks()
                if self.state == 'not_visited':
                    self.state = 'wall'
                elif self.state == 'wall':
                    self.state = 'not_visited'
            if pygame.mouse.get_pressed()[2] and self.can_click:
                self.can_click = False
                self.click_time = pygame.time.get_ticks()
                if self.state == 'not_visited' and self.game.start_point == 0:
                    self.state = 'start'
                    self.game.start_point = 1
                elif self.state == 'not_visited' and self.game.start_point == 1 and self.game.end_point == 0:
                    self.state = 'end'
                    self.game.end_point = 1
                elif self.state == 'end' and self.game.end_point == 1:
                    self.state= 'not_visited'
                    self.game.end_point = 0
                elif self.state == 'start' and self.game.start_point == 1:
                    self.state= 'not_visited'
                    self.game.start_point = 0
        
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_click:
            if current_time - self.click_time > self.click_cooldown:
                self.can_click = True
            
    def update(self, screen):
        self.check_click()
        self.draw(screen)
        self.cooldown()
        

if __name__ == '__main__':
    
    game = Game()
    game.run()