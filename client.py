import pygame
from network import Network
import pickle
from button import Button
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, game, player):
    win.fill((128, 128, 128))
    pass

def main():
    pass


buttons = [Button("Rock", 50, 500, (0, 0, 0)), Button("Scissors", 250, 500, (255, 0, 0)),  Button("Paper", 250, 500, (0, 255, 0))]
main()