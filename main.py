import pygame
import consts


class Cell(pygame.sprite.Sprite):
    def __init__(self, spr, center, isBombed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(spr).convert_alpha()
        self.rect = self.image.get_rect(center=center)

        self.isBombed = isBombed
        self.isOpened = False
        self.isFlagged = False
        self.numberOfBombs = 0

    def update(self):
        if self.isFlagged:
            self.image = pygame.image.load(consts.spr_flag).convert_alpha()

        if self.isOpened:
            self.image = pygame.image.load(consts.spr_empty).convert_alpha()


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
