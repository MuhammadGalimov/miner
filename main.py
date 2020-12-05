import pygame
import consts
import random


class Cell(pygame.sprite.Sprite):
    def __init__(self, spr, center):
        pygame.sprite.Sprite.__init__(self)
        self.center = center
        self.image = pygame.image.load(spr).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.center)

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
    def __init__(self, size, bombs):
        self.size = size
        self.numberOfBombs = bombs

        self.board = [[Cell(consts.spr_cell, (i*40, j*40)) for i in range(1, self.size+1)]
                      for j in range(1, self.size+1)]
        self.neighbors = [[0 for i in range(self.size)] for j in range(self.size)]

        self.sbombs = 0 # setted bombs
        while self.sbombs < self.numberOfBombs:
            i = random.choice(range(self.size))
            j = random.choice(range(self.size))

            if self.board[i][j].isBombed is False:
                self.board[i][j].set_bomb()
                self.sbombs += 1

        self.dop_cell = Cell(consts.spr_cell, (0, 0))
        self.copy_board = self.board.copy()

        self.copy_board = [[self.dop_cell] + l + [self.dop_cell] for l in self.copy_board]
        self.copy_board = [[self.dop_cell] * len(self.copy_board[1])] + self.copy_board \
                        + [[self.dop_cell] * len(self.copy_board[1])]

        self.nei = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]

        for row in range(1, self.size+1):
            for col in range(1, self.size+1):
                self.neighbors[row-1][col-1] = sum([int(self.copy_board[row+i[0]][col+i[1]].isBombed) for i in self.nei])

    def update(self, surface):
        for i in range(self.size):
            for j in range(self.size):
                surface.blit(self.board[i][j].image, self.board[i][j].rect)

    def check(self):
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j].click_left(self.neighbors[i][j])

    def show_bombs(self):
        pass

    def left_click(self, position):
        pass

    def right_click(self, position):
        pass


def main():
    pygame.init()
    sc = pygame.display.set_mode((consts.W, consts.H))
    clock = pygame.time.Clock()

    board = Board(10, 20)

    pygame.display.update()

    board.check()

    while True:
        clock.tick(consts.FPS)

        for item in pygame.event.get():
            if item.type == pygame.QUIT:
                exit()

            if item.type == pygame.MOUSEBUTTONDOWN:
                if item.button == 1:
                    board.left_click(item.pos)

                if item.button == 3:
                    board.right_click(item.pos)

        board.update(sc)

        pygame.display.update()


if __name__ == '__main__':
    main()
