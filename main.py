import pygame
import consts
import random


class Cell(pygame.sprite.Sprite):
    def __init__(self, spr, center):
        pygame.sprite.Sprite.__init__(self)
        self.center = center
        self.image = pygame.image.load(spr).convert_alpha()
        self.rect = self.image.get_rect(center=self.center)

        self.states = {'cell': 1, 'empty': 0, 'flag': 0}
        self.isBombed = False

    def set_bomb(self):
        self.isBombed = True

    def click_left(self, n):
        if self.isBombed:
            self.image = pygame.image.load(consts.spr_bomb).convert_alpha()
        else:
            string = consts.spr_i
            string = string.replace('I', str(n))
            self.image = pygame.image.load(string).convert_alpha()

        self.states.update({'cell': 0, 'empty': 1, 'flag': 0})

    def click_right(self):
        self.states.update({'cell': 0, 'empty': 0, 'flag': 1})
        self.image = pygame.image.load(consts.spr_flag).convert_alpha()


class Board:
    def __init__(self, spr, size, bombs):
        self.size = size
        self.numberOfBombs = bombs

        self.board = [[Cell(spr, (i*40, j*40)) for i in range(1, self.size+1)] for j in range(1, self.size+1)]

        self.sbombs = 0
        while self.sbombs < self.numberOfBombs:
            i = random.choice(range(self.size))
            j = random.choice(range(self.size))

            if self.board[i][j].isBombed is False:
                self.board[i][j].set_bomb()
                self.sbombs += 1

    def update(self, surface):
        for i in range(self.size):
            for j in range(self.size):
                surface.blit(self.board[i][j].image, self.board[i][j].rect)

    def check(self):
        for i in self.board:
            for j in i:
                j.click_left(1)


pygame.init()
sc = pygame.display.set_mode((consts.W, consts.H))
clock = pygame.time.Clock()

board = Board(consts.spr_cell, 10, 10)

pygame.display.update()

board.check()

while True:
    clock.tick(consts.FPS)

    for item in pygame.event.get():
        if item.type == pygame.QUIT:
            exit()

    board.update(sc)

    pygame.display.update()
