import pygame
import sys
import time
import white_pawn
import black_pawn
import math


class Game:

    def __init__(self):
        self.board = ['black', 'black', 'black',
                      'black', 'black', 'black',
                      'black', 'black', 'black',
                      'X', None, 'X',
                      'white', 'white', 'white',
                      'white', 'white', 'white',
                      'white', 'white', 'white']

        self.board_copy = [None] * 21

        # 0 - ruch białych, 1 - ruch czarny
        self.color = 0

        self.black_pos = [[133, 100], [400, 100], [666, 100],
                          [222, 200], [400, 200], [578, 200],
                          [310, 300], [400, 300], [490, 300]]

        self.white_pos = [[310, 500], [400, 500], [490, 500],
                          [222, 600], [400, 600], [578, 600],
                          [133, 700], [400, 700], [666, 700]]

        self.fields_pos = [[133, 100], [400, 100], [666, 100],
                           [222, 200], [400, 200], [578, 200],
                           [310, 300], [400, 300], [490, 300],
                           [320, 400], [400, 400], [480, 400],
                           [310, 500], [400, 500], [490, 500],
                           [222, 600], [400, 600], [578, 600],
                           [133, 700], [400, 700], [666, 700]]

        self.available_moves = [[1, 3], [0, 2, 4], [1, 5],
                                [0, 4, 6], [1, 3, 5, 7], [2, 4, 8],
                                [3, 7, 10], [4, 6, 8, 10], [5, 7, 10],
                                [None], [6, 7, 8, 12, 13, 14], [None],
                                [10, 13, 15], [10, 12, 14, 16], [10, 13, 17],
                                [12, 16, 18], [13, 15, 17, 19], [14, 16, 20],
                                [15, 19], [16, 18, 20], [17, 19]]

        self.available_captures = [[2, 6], [7], [0, 8],
                                   [5, 10], [10], [3, 10],
                                   [0, 8, 14], [1, 13], [2, 6, 12],
                                   [None], [3, 4, 5, 15, 16, 17], [None],
                                   [8, 14, 18], [7, 19], [6, 12, 20],
                                   [10, 17], [10], [10, 15],
                                   [12, 20], [13], [14, 18]]

        self.jumps = [[1, 3], [4], [1, 5],
             [4, 6], [7], [4, 8],
             [3, 7, 10], [4, 10], [5, 7, 10],
             [None], [6, 7, 8, 12, 13, 14], [None],
             [10, 13, 15], [10, 16], [10, 13, 17],
             [12, 16], [13], [14, 16],
             [15, 19], [16], [17, 19]]

        self.black_pawns = []
        self.white_pawns = []
        self.clicked_white = []
        self.clicked_black = []

        self.evaluated_boards = []

        self.done = False

        self.next_move = 'white'

    def minmaxalphabeta(self, depth, node_index, maximizing_player, alpha, beta):

        if maximizing_player:
            best = -math.inf
            for x in range(0, 2):
                val = self.minmaxalphabeta(depth + 1, node_index * 2 + x, False, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)

                if beta <= alpha:
                    break

            return best
        else:
            best = math.inf
            for x in range(0, 2):
                val = self.minmaxalphabeta(depth + 1, node_index * 2 + x, True, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)

                if beta <= alpha:
                    break

            return best

    def create_pawns(self):
        for pos in self.black_pos:
            pawn = black_pawn.BlackPawn(pos[0], pos[1])
            self.black_pawns.append(pawn)

        for pos in self.white_pos:
            pawn = white_pawn.WhitePawn(pos[0], pos[1])
            self.white_pawns.append(pawn)

    def find_fields(self, xMouse, yMouse, xMouse2, yMouse2):
        for field in self.fields_pos:
            if (yMouse2 > (field[0] - 30)) and (yMouse2 < (field[0] + 30)) and (xMouse2 > (field[1] - 30)) and (
                    xMouse2 < (field[1] + 30)):
                position = self.fields_pos.index(field)
                if self.color == 0:
                    self.board[position] = 'white'
                else:
                    self.board[position] = 'black'

        # x zamieniony z y
        for field2 in self.fields_pos:
            if (yMouse > (field2[1] - 30)) and (yMouse < (field2[1] + 30)) and (xMouse > (field2[0] - 30)) and (
                    xMouse < (field2[0] + 30)):
                position2 = self.fields_pos.index(field2)
                self.board[position2] = None

    def move(self, xMouse, yMouse, xMouse2, yMouse2):
        for i in range(len(self.board)):
            self.board_copy[i] = self.board[i]

        position2 = 0

        # x = pozycja wyjściowa w available_captures, np. dla pozycji wejściowej 0 może być 2 lub 6
        x = 0

        for field in self.fields_pos:
            if (yMouse2 > (field[1] - 10)) and (yMouse2 < (field[1] + 10)) and (xMouse2 > (field[0] - 10)) and (
                    xMouse2 < (field[0] + 10)):
                position = self.fields_pos.index(field)

        # x zamieniony z y
        for field2 in self.fields_pos:
            if (yMouse > (field2[1] - 10)) and (yMouse < (field2[1] + 10)) and (xMouse > (field2[0] - 10)) and (
                    xMouse < (field2[0] + 10)):
                position2 = self.fields_pos.index(field2)

        # gdzie
        # print(position)

        # skad
        # print(position2)

        # print(board_copy)
        # print()

        if position in self.available_moves[position2] and self.board_copy[position] is None:
            #print('POPRAWNY RUCH')
            self.board_copy[position2] = None
            if self.color == 0:
                self.board_copy[position] = 'white'
                #print(self.board_copy)
                #print()
            else:
                self.board_copy[position] = 'black'
                #print(self.board_copy)
                #print()

            for i in range(len(self.board_copy)):
                self.board[i] = self.board_copy[i]

            if self.next_move == 'white':
                self.next_move = 'black'
            elif self.next_move == 'black':
                self.next_move = 'white'

            # print('CALCULATED WHITE: ', self.calculate_moves('white'))
            # print('CALCULATED BLACK: ', self.calculate_moves('black'))
            return True

        for inner in self.available_captures[position2]:
            if inner == position:
                x = self.available_captures[position2].index(inner)

        #pozycja bitego pionka
        s = self.jumps[position2][x]
        #print('S: ', s)

        if self.color == 0 and self.board_copy[s] == 'black' and self.board_copy[
            position] is None or self.color == 1 and self.board_copy[s] == 'white' and self.board_copy[
            position] is None:
            #print('POPRAWNE BICIE')
            self.board_copy[position2] = None
            self.board_copy[s] = None
            if self.color == 0:
                self.board_copy[position] = 'white'
                coordinatesX_black = self.fields_pos[s][0]
                coordinatesY_black = self.fields_pos[s][1]

                for pawn in self.black_pawns:
                    if (pawn.x < coordinatesX_black + 8) and (pawn.x > coordinatesX_black - 8):
                        if (pawn.y < coordinatesY_black + 8) and (pawn.y > coordinatesY_black - 8):
                            pawn.x = 0
                            pawn.y = 0
                            pawn.rect.center = (0, 0)

            else:
                self.board_copy[position] = 'black'
                coordinatesX_white = self.fields_pos[s][0]
                coordinatesY_white = self.fields_pos[s][1]

                for pawn in self.white_pawns:
                    if (pawn.x < coordinatesX_white + 8) and (pawn.x > coordinatesX_white - 8):
                        if (pawn.y < coordinatesY_white + 8) and (pawn.y > coordinatesY_white - 8):
                            pawn.x = 0
                            pawn.y = 0
                            pawn.rect.center = (0, 0)

            for i in range(len(self.board_copy)):
                self.board[i] = self.board_copy[i]

            if self.next_move == 'white':
                self.next_move = 'black'
            elif self.next_move == 'black':
                self.next_move = 'white'

            # print('CALCULATED WHITE: ', self.calculate_moves('white'))
            # print('CALCULATED BLACK: ', self.calculate_moves('black'))
            return True

        # for white in self.white_pawns:
        #     print(white.x, white.y)
        #
        # print()
        #
        # for black in self.black_pawns:
        #     print(black.x, black.y)

        return False

    def evaluate_board(self, board):
        evaluation = 0
        white = 0
        black = 0
        for position in board:
            if position == 'white':
                white += 1
            elif position == 'black':
                black += 1

        evaluation = white - black
        #print('EVALUATION: ', evaluation)
        return evaluation

    def calculate_moves(self, color, board):
        calculated_moves = [None] * 21
        moves = []
        k = 0

        for position in range(len(board)):
            if color == 'white':
                if board[position] == 'white':
                    moves = []
                    k = 0
                    #print(position)
                    for i in self.available_moves[position]:
                        if board[i] is None:
                            moves.append(i)
                            calculated_moves[position] = moves
                    for j in self.available_captures[position]:
                        if board[j] is None:
                            value = self.jumps[position][k]
                            if board[value] == 'black':
                                moves.append(j)
                                calculated_moves[position] = moves
                        k += 1

            elif color == 'black':
                if board[position] == 'black':
                    moves = []
                    k = 0
                    #print(position)
                    for i in self.available_moves[position]:
                        if board[i] is None:
                            moves.append(i)
                            calculated_moves[position] = moves
                    for j in self.available_captures[position]:
                        if board[j] is None:
                            value = self.jumps[position][k]
                            if board[value] == 'white':
                                moves.append(j)
                                calculated_moves[position] = moves
                        k += 1

        return calculated_moves

    def minmax(self, depth, color, board, alpha, beta):
        captured = False
        virtual_board = board.copy()
        # for i in range(len(board)):
        #     virtual_board[i] = board[i]

        if depth == 0:
            return self.evaluate_board(virtual_board)

        moves = None
        if color == 'white':
            maxEval = -math.inf
            moves = self.calculate_moves('white', virtual_board)
            #print('CALCULATED WHITE: ', moves)
            for move in moves:
                if move is not None:
                    index = moves.index(move)
                    virtual_board[index] = None
                    for pos in move:
                        x = None
                        for captures in self.available_captures[index]:
                            if captures == pos:
                                captures_index = self.available_captures[index].index(captures)
                                x = self.jumps[index][captures_index]
                                if virtual_board[x] == 'black':
                                    captured = True
                                    virtual_board[x] = None
                                    for pawn in self.black_pawns:
                                        if (pawn.x < self.fields_pos[x][0] + 8) and (pawn.x > self.fields_pos[x][0] - 8):
                                            if (pawn.y < self.fields_pos[x][1] + 8) and (pawn.y > self.fields_pos[x][1] - 8):
                                                pawn.x = 0
                                                pawn.y = 0
                                                pawn.rect.center = (0, 0)

                        virtual_board[pos] = 'white'
                        eval = self.minmax(depth - 1, 'black', virtual_board, alpha, beta)
                        maxEval = max(maxEval, eval)
                        alpha = max(alpha, eval)

                        if depth == 3:
                            tmp = [virtual_board, maxEval]
                            self.evaluated_boards.append(tmp)

                        if beta <= alpha:
                            break

                        if depth < 3:
                            virtual_board[pos] = None
                            virtual_board[index] = 'white'
                            if captured and x is not None:
                                virtual_board[x] = 'black'

            # if depth == 3:
            #     tmp = [virtual_board, maxEval]
            #     self.evaluated_boards.append(tmp)

            return maxEval

        else:
            minEval = math.inf
            moves = self.calculate_moves('black', virtual_board)
            print('CALCULATED BLACK: ', moves)
            for move in moves:
                if move is not None:
                    index = moves.index(move)
                    virtual_board[index] = None
                    for pos in move:
                        x = None
                        for captures in self.available_captures[index]:
                            if captures == pos:
                                #print('CAPTURES: ', captures)
                                captures_index = self.available_captures[index].index(captures)
                                x = self.jumps[index][captures_index]
                                if virtual_board[x] == 'white':
                                    captured = True
                                    virtual_board[x] = None
                                    for pawn in self.white_pawns:
                                        if (pawn.x < self.fields_pos[x][0] + 8) and (pawn.x > self.fields_pos[x][0] - 8):
                                            if (pawn.y < self.fields_pos[x][1] + 8) and (pawn.y > self.fields_pos[x][1] - 8):
                                                pawn.x = 0
                                                pawn.y = 0
                                                pawn.rect.center = (0, 0)

                        virtual_board[pos] = 'black'
                        eval = self.minmax(depth - 1, 'white', virtual_board, alpha, beta)
                        minEval = min(minEval, eval)
                        beta = min(beta, eval)

                        if depth == 3:
                            tmp = [virtual_board, minEval]
                            #print('TMP: ', tmp)
                            self.evaluated_boards.append(tmp)

                        if beta <= alpha:
                            break

                        if depth < 3:
                            virtual_board[pos] = None
                            virtual_board[index] = 'black'
                            if captured and x is not None:
                                virtual_board[x] = 'white'

            # if depth == 3:
            #     tmp = [virtual_board, minEval]
            #     self.evaluated_boards.append(tmp)

            return minEval

    def play(self):
        pygame.init()
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 18)
        textsurface = font.render('', False, (0, 0, 0))

        screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Lau kata kati')

        background = pygame.image.load('assets/board.png').convert()
        white = pygame.image.load('assets/white.png')
        black = pygame.image.load('assets/black.png')

        clock = pygame.time.Clock()

        self.create_pawns()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if self.next_move == 'white':
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.done:
                        self.done = True
                        xMouse = event.pos[0]
                        yMouse = event.pos[1]
                        #print(xMouse, yMouse)

                        # clicked_white = [p for p in white_pawns if p.rect.collidepoint(xMouse, yMouse)]
                        # clicked_black = [p for p in black_pawns if p.rect.collidepoint(xMouse, yMouse)]

                        index = None
                        for p in self.white_pawns:
                            if p.rect.collidepoint(xMouse, yMouse):
                                self.clicked_white.append(p)
                                index = self.white_pawns.index(p)
                        if len(self.clicked_white) == 1:
                            print('BIAŁY ZŁAPANY')
                            clicked_pawn = self.clicked_white[0]
                            self.color = 0
                            textsurface = font.render('', False, (0, 0, 0))
                        else:
                            self.done = False
                            textsurface = font.render('Pionek wybrany niepoprawnie!', False, (0, 0, 0))

                    elif event.type == pygame.MOUSEBUTTONDOWN and self.done:
                        self.done = False
                        xMouse2 = event.pos[0]
                        yMouse2 = event.pos[1]
                        # clicked_pawn.x = xMouse2
                        # clicked_pawn.y = yMouse2

                        if self.move(xMouse, yMouse, xMouse2, yMouse2):
                            if self.color == 0:
                                self.white_pawns[index].x = xMouse2
                                self.white_pawns[index].y = yMouse2
                                self.white_pawns[index].rect.center = (xMouse2, yMouse2)

                            elif self.color == 1:
                                self.black_pawns[index].x = xMouse2
                                self.black_pawns[index].y = yMouse2
                                self.black_pawns[index].rect.center = (xMouse2, yMouse2)

                            textsurface = font.render('', False, (0, 0, 0))

                        else:
                            textsurface = font.render('Niepoprawny ruch!', False, (0, 0, 0))

                        #for whitepawn in self.white_pawns:
                            #print(whitepawn.x, whitepawn.y)

                        #print()

                        #for blackpawn in self.black_pawns:
                            #print(blackpawn.x, blackpawn.y)

                        # clicked_pawn.rect.center = (clicked_pawn.x, clicked_pawn.y)

                        self.clicked_white = []
                        self.clicked_black = []

                elif self.next_move == 'black':
                    miN = 100
                    eval = self.minmax(3, 'black', self.board, -math.inf, math.inf)
                    for element in self.evaluated_boards:
                        #print('ELEMENT: ', element[0])
                        if element[1] == eval:
                            self.board = element[0]
                            self.evaluated_boards = []
                            break

                    # for element in self.evaluated_boards:
                    #     if element[1] < miN:
                    #         miN = element[1]
                    #
                    # print('MIN: ', miN)
                    #
                    # for x in self.evaluated_boards:
                    #     if x[1] == miN:
                    #         self.board = x[0]
                    #         self.evaluated_boards = []
                    #         break

                    self.color = 1
                    self.next_move = 'white'

                        # for p in self.black_pawns:
                        #     if p.rect.collidepoint(xMouse, yMouse):
                        #         self.clicked_black.append(p)
                        #         index = self.black_pawns.index(p)
                        # if len(self.clicked_black) == 1:
                        #     print('CZARNY HEHE ZŁAPANY')
                        #     clicked_pawn = self.clicked_black[0]
                        #     self.color = 1
                        #     textsurface = font.render('', False, (0, 0, 0))
                        # else:
                        #     self.done = False
                        #     textsurface = font.render('Pionek wybrany niepoprawnie!', False, (0, 0, 0))

                    # for pawn in white_pawns:
                    #     print(pawn.x, pawn.y)
                    #     if pawn.rect.collidepoint(xMouse, yMouse):
                    #         pawn.x = xMouse
                    #         pawn.y = yMouse
                    #         pawn.rect.center = (pawn.x, pawn.y)

            screen.blit(background, (0, 0))
            screen.blit(textsurface, (0, 0))
            # for pawn in black_pawns:
            #     screen.blit(pawn.image, (pawn.x-32.5, pawn.y-32.5))
            #
            # for pawn in white_pawns:
            #     screen.blit(pawn.image, (pawn.x-32.5, pawn.y-32.5))

            for x in range(len(self.board)):
                if self.board[x] == 'white':
                    screen.blit(white, (self.fields_pos[x][0] - 32.5, self.fields_pos[x][1] - 32.5))
                elif self.board[x] == 'black':
                    screen.blit(black, (self.fields_pos[x][0] - 32.5, self.fields_pos[x][1] - 32.5))

                # if pawn == 'white':
                #     print(x)
                #     screen.blit(white, (fields_pos[x][0]-32.5, fields_pos[x][1]-32.5))
                # elif pawn == 'black':
                #     print(x)
                #     screen.blit(black, (fields_pos[x][0] - 32.5, fields_pos[x][1] - 32.5))

            print(self.board)
            pygame.display.update()
            clock.tick(60)
            time.sleep(0.5)
