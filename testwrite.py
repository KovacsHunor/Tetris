import pygame
from pygame.locals import*
size = 20
width = size*35
height = size*35

def Field(b):
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    for i in range(24):
        for j in range(7):
            if b[j][i]:
                pygame.draw.rect(screen, (255, 240, 31),
                pygame.Rect(300 + j*size, 100 + i*size, size - 1, size - 1))
            else:
                pygame.draw.rect(screen, (30, 30, 30),
                pygame.Rect(300 + j*size, 100 + i*size, size, size))
    pygame.display.update()
def ExitCheck():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
def Write(a):
    pygame.init()
    pygame.display.set_caption('Tetris')
    
    Field(a)
    ExitCheck()
