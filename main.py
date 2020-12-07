import pygame
import consts
import random
import time


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
        self.game_over = False
        self.win = False

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
        self.copy_board = []
        self.nei = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]

        self.openCell = []  # спиоск ячеек на открытие
        self.foundBombs = 0  # количество бомб помеченных флажком
        self.numberOfFlags = 0  # количество ячеек помеченных флажком

        self.dop_cell = Cell(consts.spr_cell, (0, 0))
        self.dop_cell.callable = False
        self.firstClick = False
        self.sec = 0
        self.end_time = 0

    def setting_bombs(self, cell):
        # устанавливаем бомбы
        sbombs = 0  # количество установленных бомб

        while sbombs < self.numberOfBombs:
            i = random.choice(range(self.size))
            j = random.choice(range(self.size))

            if self.board[i][j].isBombed is False and i != cell[0] and j != cell[1]:
                self.board[i][j].set_bomb()
                sbombs += 1

    def count_neig(self):
        # считаем для каждого cell количетсво соседей с бомбами
        self.copy_board = self.board.copy()

        self.copy_board = [[self.dop_cell] + l + [self.dop_cell] for l in self.copy_board]
        self.copy_board = [[self.dop_cell] * len(self.copy_board[1])] + self.copy_board \
                          + [[self.dop_cell] * len(self.copy_board[1])]

        for row in range(1, self.size + 1):
            for col in range(1, self.size + 1):
                self.neighbors[row - 1][col - 1] = sum([int(self.copy_board[row + i[0]][col + i[1]].isBombed)
                                                        for i in self.nei])

    def update(self, surface, font):
        if not self.firstClick:
            t = 0
        else:
            t = time.time() - self.sec

        if self.win or self.game_over:
            t = self.end_time - self.sec

        for i in range(self.size):
            for j in range(self.size):
                surface.blit(self.board[i][j].image, self.board[i][j].rect)

        text_b = font.render('Bombs: {}'.format(self.numberOfBombs - self.numberOfFlags), True, (0, 180, 0))
        text_go = font.render('Game over', True, (180, 0, 0))
        text_gj = font.render('Good job!', True, (0, 180, 0))
        text_time = font.render('{} sec'.format(int(t)), True, (0, 180, 0))
        surface.blit(text_b, text_b.get_rect(topleft=(self.left_frame, self.top_frame + self.cellSize * self.size +
                                                      30)))

        surface.blit(text_time, text_time.get_rect(topright=(consts.W - self.left_frame, self.top_frame + self.cellSize
                                                             * self.size + 30)))

        if self.win:
            surface.blit(text_gj, text_gj.get_rect(topleft=(self.left_frame, self.top_frame +
                                                            self.cellSize * self.size + 80)))

        if self.game_over:
            surface.blit(text_go, text_go.get_rect(topleft=(self.left_frame, self.top_frame +
                                                            self.cellSize * self.size + 80)))

    def check_flag(self):
        if self.foundBombs == self.numberOfBombs:
            self.win = True
            self.end_time = time.time()

    def show_bombs(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].isBombed and self.board[i][j].states['flag'] == 0:
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
        self.check_flag()

        if self.win or self.game_over:
            return 0

        cell = self.get_cell(position)
        if cell:
            if not self.firstClick:
                self.first_click_function(cell)

            if self.board[cell[0]][cell[1]].states['empty'] == 0:
                if self.board[cell[0]][cell[1]].states['flag'] == 0:
                    self.numberOfFlags += 1
                if self.board[cell[0]][cell[1]].states['flag'] == 1:
                    self.numberOfFlags -= 1
                self.board[cell[0]][cell[1]].click_right()

            if self.board[cell[0]][cell[1]].states['flag'] == 0 and self.board[cell[0]][cell[1]].isBombed:
                self.foundBombs += 1
            if self.board[cell[0]][cell[1]].states['flag'] == 1 and self.board[cell[0]][cell[1]].isBombed:
                self.foundBombs -= 1

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

    def first_click_function(self, cell):
        self.setting_bombs(cell)
        self.count_neig()
        self.firstClick = True
        self.sec = time.time()
        # self.show_bombs()  # убрать

    def left_click(self, position):
        if self.win or self.game_over:
            return 0

        cell = self.get_cell(position)

        if cell:
            if not self.firstClick:
                self.first_click_function(cell)

            if not self.board[cell[0]][cell[1]].isBombed:
                self.addCellsToOpen(cell)
            else:
                self.game_over = True
                self.end_time = time.time()
                # self.openCell.append(cell)
                self.show_bombs()

            for item in self.openCell:
                self.board[item[0]][item[1]].click_left(self.neighbors[item[0]][item[1]])

            self.openCell.clear()


def main():
    pygame.init()
    sc = pygame.display.set_mode((consts.W, consts.H))
    pygame.display.set_caption("Сапер")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)

    board = Board(10, 15)

    pygame.display.update()

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
        board.update(sc, font)

        pygame.display.update()


if __name__ == '__main__':
    main()
