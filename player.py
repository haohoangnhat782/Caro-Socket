import pygame
import sys
import random
from pygame.locals import Rect


class TicTacToe:
    def __init__(self):
        # Khởi tạo Pygame
        pygame.init()
        # Thiết lập một số hằng số
        self.WIDTH_MAIN = 800
        self.WIDTH, self.HEIGHT = 600, 600
        self.input = ""
        # Tạo màn hình
        self.screen = pygame.display.set_mode((self.WIDTH_MAIN, self.HEIGHT + 100))
        self.line_1 = 3
        self.markers = []
        self.pos = []
        self.winner = 0
        self.player = 1
        self.input_text = ""
        self.game_over = False
        self.clicked = False
        self.green = (0, 255, 0)
        self.gray = (117, 135, 167)
        self.red = (255, 0, 0)
        self.gray_light = (200, 200, 200)
        self.blue = (0, 0, 255)
        self.win_line_color = (0, 0, 255)
        self.font = pygame.font.SysFont(None, 40)
        self.again_rect = Rect(self.WIDTH + 30, self.HEIGHT - 115, 140, 50)
        self.reset()
        self.font_pl = pygame.font.SysFont(None, 35)
        self.fontx = pygame.font.SysFont(None, 25)
        self.text_part = ""

    def draw_home(self):
        title = "Caro"
        win_img = self.font.render(title, True, self.blue)
        self.screen.blit(win_img, (self.WIDTH + 60, self.HEIGHT - 570))

        title_x = "10x10"
        win_x = self.fontx.render(title_x, True, self.blue)
        self.screen.blit(win_x, (self.WIDTH + 70, self.HEIGHT - 520))

        # title_player = "Player turn:"
        # win_x = self.font_pl.render(title_player, True, self.blue)
        # self.screen.blit(win_x, (self.WIDTH + 20, self.HEIGHT -460))

        again_text = "Reset"
        again_img = self.font_pl.render(again_text, True, self.blue)
        pygame.draw.rect(self.screen, self.gray, self.again_rect)
        self.screen.blit(again_img, (self.WIDTH + 70, self.HEIGHT - 100))

        fontchat = pygame.font.Font(None, 36)
        text_surface1 = fontchat.render(self.input_text, True, (0, 0, 0))
        self.screen.blit(text_surface1, (0, self.HEIGHT + 70))

        text_surface2 = fontchat.render(self.text_part, True, (0, 0, 0))
        self.screen.blit(text_surface2, (0, self.HEIGHT + 20))

    # Vẽ bảng
    def draw_grid(self):
        bg = (255, 255, 255)
        grid = (128, 128, 128)
        self.screen.fill(bg)
        for x in range(1, 10):
            pygame.draw.line(self.screen, grid, (0, x * 60), (self.WIDTH, x * 60), self.line_1)
            pygame.draw.line(self.screen, grid, (x * 60, 0,), (x * 60, self.HEIGHT), self.line_1)
            # Vẽ đường kẻ thông qua các ô chiến thắng
        for cell in self.find_winning_cells():
            x, y = cell
            pygame.draw.rect(self.screen, self.blue, (x * 60, y * 60, 60, 60), 3)

        # Vẽ đường kẻ thông qua các ô chiến thắng
        # for cell in self.find_winning_cells():
        # x, y = cell
        # Vẽ đường kẻ ngang
        # pygame.draw.line(self.screen, self.win_line_color, (x * 60 , y * 60 + 30), (x * 60 + 50, y * 60 + 30), 3)
        # Vẽ đường kẻ dọc
        # pygame.draw.line(self.screen, self.win_line_color, (x * 60 + 30, y * 60 + 10), (x * 60 + 30, y * 60 + 50), 3)
        # Vẽ đường kẻ chéo
        # pygame.draw.line(self.screen, self.win_line_color, (x * 60 + 10, y * 60 + 10), (x * 60 + 50, y * 60 + 50), 3)
        # pygame.draw.line(self.screen,self.win_line_color, (x * 60 + 10, y * 60 + 50), (x * 60 + 50, y * 60 + 10), 3)

    def reset(self):
        self.markers = []
        self.pos = []
        self.player = 1
        self.winner = 0
        self.game_over = False
        for x in range(10):
            row = [0] * 10
            self.markers.append(row)
        print(self.markers)

    # Kiểm tra người chiến thắng
    def check_winner2(self):
        # Kiểm tra hàng và cột
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

    # Vẽ kí hiệu của người chơi
    def draw_marker(self):
        x_pos = 0
        for x in self.markers:
            y_pos = 0
            for y in x:
                if y == 1:
                    pygame.draw.line(self.screen, self.green, (x_pos * 60 + 10, y_pos * 60 + 10),
                                     (x_pos * 60 + 45, y_pos * 60 + 45), self.line_1)
                    pygame.draw.line(self.screen, self.green, (x_pos * 60 + 10, y_pos * 60 + 45),
                                     (x_pos * 60 + 45, y_pos * 60 + 10), self.line_1)
                if y == -1:
                    pygame.draw.circle(self.screen, self.red, (x_pos * 60 + 30, y_pos * 60 + 30), 24, self.line_1)
                y_pos += 1
            x_pos += 1

    # Vẽ thông báo người chiến thắng
    def draw_winner(self):
        win_text = 'Player:' + str(self.winner) + ' win!'
        win_img = self.font_pl.render(win_text, True, self.blue)
        self.screen.blit(win_img, (self.WIDTH + 20, self.HEIGHT - 350))

        # again_text = "Chơi lại"
        # again_img = self.font.render(again_text, True, self.blue)
        # pygame.draw.rect(self.screen, self.gray, self.again_rect)
        # self.screen.blit(again_img, (self.WIDTH // 2 - 80, self.HEIGHT // 2 + 10))

    def find_winning_cells(self):
        winning_cells = []

        # Kiểm tra hàng và cột
        for row_index, row in enumerate(self.markers):
            for col_index in range(len(row) - 4):
                if sum(row[col_index:col_index + 5]) == 5:
                    # Nếu hàng chiến thắng
                    winning_cells.extend([(row_index, col_index + i) for i in range(5)])
                elif sum(row[col_index:col_index + 5]) == -5:
                    winning_cells.extend([(row_index, col_index + i) for i in range(5)])

        for col_index in range(len(self.markers[0])):
            for row_index in range(len(self.markers) - 4):
                if sum(self.markers[row][col_index] for row in range(row_index, row_index + 5)) == 5:
                    # Nếu cột chiến thắng
                    winning_cells.extend([(row_index + i, col_index) for i in range(5)])
                elif sum(self.markers[row][col_index] for row in range(row_index, row_index + 5)) == -5:
                    winning_cells.extend([(row_index + i, col_index) for i in range(5)])

        # Kiểm tra đường chéo chính
        for row_index in range(len(self.markers) - 4):
            for col_index in range(len(self.markers) - 4):
                if sum(self.markers[row_index + i][col_index + i] for i in range(5)) == 5:
                    # Nếu đường chéo chính chiến thắng
                    winning_cells.extend([(row_index + i, col_index + i) for i in range(5)])
                elif sum(self.markers[row_index + i][col_index + i] for i in range(5)) == -5:
                    winning_cells.extend([(row_index + i, col_index + i) for i in range(5)])

        # Kiểm tra đường chéo phụ
        for row_index in range(len(self.markers) - 4):
            for col_index in range(4, len(self.markers)):
                if sum(self.markers[row_index + i][col_index - i] for i in range(5)) == 5:
                    # Nếu đường chéo phụ chiến thắng
                    winning_cells.extend([(row_index + i, col_index - i) for i in range(5)])
                elif sum(self.markers[row_index + i][col_index - i] for i in range(5)) == -5:
                    winning_cells.extend([(row_index + i, col_index - i) for i in range(5)])

        return winning_cells

    # Vòng lặp chính
    def main_loop(self):
        run = True
        while run:
            self.draw_grid()
            self.draw_marker()
            self.draw_home()
            winning_cells = self.find_winning_cells()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        print("Dữ liệu đã nhập:", self.input_text)
                        self.text_part = self.input_text
                        self.input_text = ""
                    else:
                        self.input_text += event.unicode

                if self.game_over == False:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                        self.clicked = True
                    if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                        self.clicked = False

                        self.pos = pygame.mouse.get_pos()
                        cell_x = self.pos[0] // 60
                        cell_y = self.pos[1] // 60
                        if 0 <= cell_x < 10 and 0 <= cell_y < 10:
                            if self.markers[cell_x][cell_y] == 0:
                                self.markers[cell_x][cell_y] = self.player
                                self.player *= -1
                                self.check_winner2()

            if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                self.clicked = True
            if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                self.clicked = False
                self.pos = pygame.mouse.get_pos()
                if self.again_rect.collidepoint(self.pos):
                    self.reset()

            if self.game_over == True:
                self.draw_winner()

            pygame.display.update()

        pygame.quit()
        sys.exit()


# Tạo một phiên bản của trò chơi và chạy vòng lặp chính
game = TicTacToe()
game.main_loop()
