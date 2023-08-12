from settings import *
import pygame

class Cell:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x * TILE, self.y * TILE, TILE - 2, TILE - 2))
        self.state = State.UNVISITED
        self.click_time = 0
        self.click_cooldown = 300
        self.can_click = True
        self.game = game
        
    def __str__(self):
        return f"{self.state} cell at {self.x}, {self.y}"
    
    def draw(self, screen):

            pygame.draw.rect(screen, self.state.value, self.rect, border_radius = 7)
            
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and self.can_click:
                self.can_click = False
                self.click_time = pygame.time.get_ticks()
                if self.state == State.UNVISITED:
                    self.state = State.WALL
                elif self.state == State.WALL:
                    self.state = State.UNVISITED
            if pygame.mouse.get_pressed()[2] and self.can_click:
                self.can_click = False
                self.click_time = pygame.time.get_ticks()
                if self.state == State.UNVISITED and not self.game.start_point:
                    self.state = State.START
                    self.game.start_point = True
                elif self.state == State.UNVISITED and self.game.start_point and not self.game.end_point:
                    self.state = State.FINISH
                    self.game.end_point = True
                elif self.state == State.FINISH and self.game.end_point:
                    self.state= State.UNVISITED
                    self.game.end_point = False
                elif self.state == State.START and self.game.start_point:
                    self.state= State.UNVISITED
                    self.game.start_point = False
        
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_click:
            if current_time - self.click_time > self.click_cooldown:
                self.can_click = True
            
    def update(self, screen):
        self.check_click()
        self.draw(screen)
        self.cooldown()