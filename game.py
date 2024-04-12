import pygame
import sys
import random
from pygame.locals import Rect
class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = True
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0
        self.input_text = ""
        self.text_part= ""
        self.last_selected = None
        self.markers = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.pos = []
        self.player = 1
        self.winner = 0
        self.winner_part = 0
        self.game_over = False
        # self.reset()
        self.clicked = False
        self.green = (0, 255, 0)
        self.gray=(117, 135, 167)
        self.red = (255, 0, 0)
        self.gray_light = (200, 200, 200)
        self.blue = (0, 0, 255)
        self.line_1 = 3
        self.namep1 = ""
        self.namep2 = ""


    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]
    def name(self,player,data):
        if player == 0:
            self.namep1 = data
        else:
            self.namep2 = data
        print(self.namep2+"sadasd")

    def chat(self,data):
        self.text_part = self.input_text
        self.input_text = data


    def play(self, player, move):
        cell_x_str, cell_y_str = move.split(',')

        # Convert coordinates back to integers
        cell_x = int(cell_x_str)
        cell_y = int(cell_y_str)

        self.moves[player] = move
        if player == 0:
            self.markers[cell_x][cell_y] = 1
            self.p1Went = True
            self.p2Went=False

        else:
            self.markers[cell_x][cell_y] = -1
            self.p2Went = True
            self.p1Went = False
        self.last_selected=(cell_x,cell_y)



    def connected(self):
        return self.ready

    def bothWent(self):
        return self.game_over

    def check_winner(self):
        for row in self.markers:
            for i in range(len(row) - 4):
                if sum(row[i:i + 5]) == 5:
                    self.winner = 1
                    self.game_over = True
                elif sum(row[i:i + 5]) == -5:
                    self.winner = 2
                    self.game_over = True

        for col in range(len(self.markers[0])):
            for i in range(len(self.markers) - 4):
                if sum(self.markers[row][col] for row in range(i, i + 5)) == 5:
                    self.winner = 1
                    self.game_over = True
                elif sum(self.markers[row][col] for row in range(i, i + 5)) == -5:
                    self.winner = 2
                    self.game_over = True

        # Kiểm tra đường chéo chính
        for i in range(len(self.markers) - 4):
            if sum(self.markers[i + j][i + j] for j in range(5)) == 5:
                self.winner = 1
                self.game_over = True
            elif sum(self.markers[i + j][i + j] for j in range(5)) == -5:
                self.winner = 2
                self.game_over = True

        # Kiểm tra đường chéo phụ
        for i in range(len(self.markers) - 4):
            if sum(self.markers[i + j][len(self.markers) - 1 - i - j] for j in range(5)) == 5:
                self.winner = 1
                self.game_over = True
            elif sum(self.markers[i + j][len(self.markers) - 1 - i - j] for j in range(5)) == -5:
                self.winner = 2
                self.game_over = True

        # Kiểm tra các đường chéo còn lại
        for i in range(len(self.markers) - 4):
            for j in range(len(self.markers) - 4):
                if sum(self.markers[i + k][j + k] for k in range(5)) == 5:
                    self.winner = 1
                    self.game_over = True
                elif sum(self.markers[i + k][j + k] for k in range(5)) == -5:
                    self.winner = 2
                    self.game_over = True

                if sum(self.markers[i + k][len(self.markers) - 1 - j - k] for k in range(5)) == 5:
                    self.winner = 1
                    self.game_over = True
                elif sum(self.markers[i + k][len(self.markers) - 1 - j - k] for k in range(5)) == -5:
                    self.winner = 2
                    self.game_over = True
        if all(marker != 0 for row in self.markers for marker in row):
            self.winner = 3
            self.game_over = True

        self.winner_part = self.winner
        return  self.winner_part



    def resetWent(self):
        self.p1Went = False
        self.p2Went = True
        self.markers = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.pos = []
        self.player = 1
        self.winner = 0
        self.game_over = False
        self.last_selected = None
