import pygame
import consts


class Cell(pygame.sprite.Sprite):
    def __init__(self, spr, center, isBombed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(spr).convert_alpha()
        self.rect = self.image.get_rect(center=center)

        self.states = {'cell': 1, 'empty': 0, 'flag': 0}
        self.isBombed = isBombed

    def click_empty(self):
        self.states.update({'cell': 0, 'empty': 1, 'flag': 0})
        self.image = pygame.image.load(consts.spr_empty).convert_alpha()

    def click_flag(self):
        self.states.update({'cell': 0, 'empty': 0, 'flag': 1})
        self.image = pygame.image.load(consts.spr_flag).convert_alpha()


class Board:
    def __init__(self, spr, size):
        self.size = size
        self.board = [[Cell(spr, (i*40, j*40), False) for i in range(1, self.size+1)] for j in range(1, self.size+1)]


pygame.init()
sc = pygame.display.set_mode((consts.W, consts.H))
clock = pygame.time.Clock()

board = Board(consts.spr_cell, 10)

board.board[1][1].isFlagged = True
board.board[5][5].isOpened = True
board.board[1][1].update()
board.board[5][5].update()

pygame.display.update()

while True:
    clock.tick(consts.FPS)

    for item in pygame.event.get():
        if item.type == pygame.QUIT:
            exit()

    for i in range(board.size):
        for j in range(board.size):
            sc.blit(board.board[i][j].image, board.board[i][j].rect)

    pygame.display.update()
