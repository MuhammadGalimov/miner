import pygame
import consts
import random


class Cell(pygame.sprite.Sprite):
    def __init__(self, spr, topleft):
        pygame.sprite.Sprite.__init__(self)
        self.pt = topleft
        self.image = pygame.image.load(spr).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pt)

        self.states = {'cell': 1, 'empty': 0, 'flag': 0}
        self.isBombed = False
        self.callable = True

    def set_bomb(self):
        self.isBombed = True

    def click_left(self, n):
        if self.isBombed:
            self.image = pygame.image.load(consts.spr_bomb).convert_alpha()
        elif self.states['flag'] == 1:
            return False
        else:
            string = consts.spr_i
            string = string.replace('I', str(n))
            self.image = pygame.image.load(string).convert_alpha()
            self.states.update({'cell': 0, 'empty': 1, 'flag': 0})

    def click_right(self):
        if self.states['flag'] == 1:
            self.states.update({'cell': 1, 'empty': 0, 'flag': 0})
            self.image = pygame.image.load(consts.spr_cell).convert_alpha()
        elif self.states['empty'] == 1:
            return False
        else:
            self.states.update({'cell': 0, 'empty': 0, 'flag': 1})
            self.image = pygame.image.load(consts.spr_flag).convert_alpha()


class Board:
    def __init__(self, size, bombs):
        """
        size - размер игрового поля
        bombs - количество бомб
        """
        self.size = size
        self.numberOfBombs = bombs

        self.cellSize = 40
        self.top_frame = self.cellSize
        self.left_frame = self.cellSize
        self.right_frame = consts.W - (self.left_frame + self.size * self.cellSize)
        self.bottom_frame = consts.H - (self.top_frame + self.size * self.cellSize)

        self.board = [[Cell(consts.spr_cell, (i*self.cellSize, j*self.cellSize)) for i in range(1, self.size+1)]
                      for j in range(1, self.size+1)]
        self.neighbors = [[0 for i in range(self.size)] for j in range(self.size)]

        # устанавливаем бомбы
        self.sbombs = 0 # setted bombs
        while self.sbombs < self.numberOfBombs:
            i = random.choice(range(self.size))
            j = random.choice(range(self.size))

            if self.board[i][j].isBombed is False:
                self.board[i][j].set_bomb()
                self.sbombs += 1

        # считаем для каждого cell количетсво соседей с бомбами
        self.dop_cell = Cell(consts.spr_cell, (0, 0))
        self.dop_cell.callable = False
        self.copy_board = self.board.copy()

        self.copy_board = [[self.dop_cell] + l + [self.dop_cell] for l in self.copy_board]
        self.copy_board = [[self.dop_cell] * len(self.copy_board[1])] + self.copy_board \
            + [[self.dop_cell] * len(self.copy_board[1])]

        self.nei = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]

        for row in range(1, self.size+1):
            for col in range(1, self.size+1):
                self.neighbors[row-1][col-1] = sum([int(self.copy_board[row+i[0]][col+i[1]].isBombed)
                                                    for i in self.nei])

        self.openCell = []

    def update(self, surface):
        for i in range(self.size):
            for j in range(self.size):
                surface.blit(self.board[i][j].image, self.board[i][j].rect)

    def check(self):
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j].click_left(self.neighbors[i][j])

    def show_bombs(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].isBombed:
                    self.board[i][j].click_left(self.neighbors[i][j])

    def get_cell(self, position):
        if self.left_frame <= position[0] <= consts.W - self.right_frame \
                and self.top_frame <= position[1] <= consts.H - self.bottom_frame:
            x = (position[0] - self.cellSize) // self.cellSize
            y = (position[1] - self.cellSize) // self.cellSize

            return [y, x]
        else:
            return False

    def right_click(self, position):
        cell = self.get_cell(position)
        if cell:
            self.board[cell[0]][cell[1]].click_right()

    # сюда приходят только ячейки без бомбы
    def addCellsToOpen(self, cell):
        self.openCell.append(cell)
        neigWithBombs = False
        for n in self.nei:
            if self.copy_board[cell[0] + 1 + n[0]][cell[1] + 1 + n[1]].isBombed:
                neigWithBombs = True

        if neigWithBombs:
            return 'done'
        else:
            for n in self.nei:
                if self.copy_board[cell[0] + 1 + n[0]][cell[1] + 1 + n[1]].callable:
                    self.copy_board[cell[0] + 1 + n[0]][cell[1] + 1 + n[1]].callable = False
                    self.addCellsToOpen((cell[0] + n[0], cell[1] + n[1]))

    def left_click(self, position):
        cell = self.get_cell(position)

        if cell:
            if not self.board[cell[0]][cell[1]].isBombed:
                self.addCellsToOpen(cell)
            else:
                self.openCell.append(cell)

            for item in self.openCell:
                self.board[item[0]][item[1]].click_left(self.neighbors[item[0]][item[1]])

            self.openCell.clear()


def main():
    pygame.init()
    sc = pygame.display.set_mode((consts.W, consts.H))
    clock = pygame.time.Clock()

    board = Board(10, 20)

    pygame.display.update()

    board.show_bombs()

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

        sc.fill((255, 250, 250))
        board.update(sc)

        pygame.display.update()


if __name__ == '__main__':
    main()
