import time
import pygame
import constants

class TrafficSignal(pygame.sprite.Sprite):
    def __init__(self, cord):
        pygame.sprite.Sprite.__init__(self)
        self.redSignal = pygame.image.load('images/signals/red.png')
        self.yellowSignal = pygame.image.load('images/signals/yellow.png')
        self.greenSignal = pygame.image.load('images/signals/green.png')

        self.x = cord[0]
        self.y = cord[1]
        self.direction = cord[2]

        self.current_green = False
        self.current_yellow = False

        constants.group_signals.add(self)

    # Método para quando o sinal fica vermelho
    def red_turn(self):
        time.sleep(0.5)
        self.current_yellow = False
        self.current_green = False

    # Método para quando o sinal fica verde
    def green_turn(self):
        self.current_yellow = False
        self.current_green = False
        time.sleep(2)
        self.current_green = True
        self.current_yellow = False