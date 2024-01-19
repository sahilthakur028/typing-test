# Module Imports
import sys
import pygame
import time
import json
import random

# Program Constants
WIDTH, HEIGHT = 800, 600
FPS = 30

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Typing Master')
pygame.init()

background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Functions

def draw_text(surface, message, y_cord, font_size, color):
    '''Function to draw text exactly on the middle of user's screen'''
    font = pygame.font.Font('./FiraCode.ttf', font_size)
    text = font.render(message, 1,  color)
    text_rect = text.get_rect(center=(WIDTH/2, y_cord))
    surface.blit(text, text_rect)

def draw_surface(surface):
    '''Function to draw everything (backgrounds, texts, etc) on the surface'''
    surface.fill((0, 0, 0))
    surface.blit(background, (0, 0))
    draw_text(surface, 'Typing Test', 100, 60, (249, 231, 159))
    if user.prompt:
        if len(user.prompt) >= 60:
            lis = user.prompt.split()
            w1 = ' '.join(lis[:len(lis)//2])
            w2 = ' '.join(lis[len(lis)//2:])
            draw_text(surface, w1, 200, 20, (88, 214, 141))
            draw_text(surface, w2, 240, 20, (88, 214, 141))
    surface.fill((0, 0, 0), (50, 300, 700, 80))
    pygame.draw.rect(surface, (133, 193, 233), (50, 300, 700, 80), 2)
    if user.input:
        if len(user.input) >= 45:
            lis = user.input.split()
            w1 = ' '.join(lis[:len(lis)//2])
            w2 = ' '.join(lis[len(lis)//2:])
            draw_text(surface, w1, 325, 17, (93, 173, 226))
            draw_text(surface, w2, 355, 17, (93, 173, 226))
        else:
            draw_text(surface, user.input, 325, 17, (93, 173, 226))
    if user.end:
        draw_text(surface, user.result, 500, 22, (236, 112, 99))
    pygame.display.update()

def reset_game():
    '''Function to reset the whole game'''
    user.timer_started, user.end = False, False
    user.total_time, user.time_started = 0, 0
    user.prompt, user.input = user.get_sentence(), ''
    user.accuracy, user.wpm = 0, 0
    user.result = ''

def show_results():
    '''Function to end the game and show results'''
    if user.timer_started and not user.end:
        user.total_time = time.time() - user.time_started

        count = 0
        for i, c in enumerate(user.prompt):
            try:
                if user.input[i] == c:
                    count += 1
            except:
                pass
        
        # Calculating accuracy, wpm, and displaying results
        user.accuracy = count / len(user.prompt) * 100
        user.wpm = len(user.input) * 60 / (5 * user.total_time)
        user.end = True
        user.result = f'Time : {round(user.total_time)}s || Accuracy : {round(user.accuracy)}% || WPM : {round(user.wpm)}'
        print(user.result)

# User Class

class User:
    def __init__(self):
        self.prompt = self.get_sentence()
        self.input = ''
        self.time_started = 0
        self.total_time = 0
        self.timer_started = False
        self.end = False
        self.accuracy = 0
        self.wpm = 0
        self.result = ''
    
    def get_sentence(self):
        '''Function to get a sentence of 10 words'''
        data = json.load(open('words.json'))
        dat = random.choices(data, k=10)
        return ' '.join(dat)

running = True
clock = pygame.time.Clock()
user = User()

# Game Loop
while running:
    clock.tick(FPS)
    draw_surface(WIN)
    for event in pygame.event.get():
        # Quit Event
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        # Mouse Click Event
        elif event.type == pygame.MOUSEBUTTONUP:
            if not user.timer_started:
                # Starting the timer
                user.time_started = time.time()
                user.timer_started = True
            x, y = pygame.mouse.get_pos()
            if user.end:
                # Resetting the game if the game ended
                reset_game()
        
        # Key pressed event
        elif event.type == pygame.KEYDOWN:
            if user.timer_started and not user.end:
                # Checking for keys pressed (letters, enter and backspace) 
                if event.key == pygame.K_RETURN:
                    show_results()
                elif event.key == pygame.K_BACKSPACE:
                    user.input = user.input[:-1]
                else:
                    try:
                        user.input += event.unicode
                    except:
                        pass
            if not user.timer_started and not user.end:
                # If the timer did not start but the user pressed a key
                user.time_started = time.time()
                user.timer_started = True
                try:
                    user.input += event.unicode
                except:
                    pass
    pygame.display.update()
