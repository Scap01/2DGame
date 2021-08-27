import pygame
pygame.init()

#creating game window
pygame.display.set_mode((800, 600))
pygame.display.set_caption("2dg - beta")

#game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()