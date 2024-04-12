import pygame
from network import Network
import random
from pygame.locals import Rect
import pickle
pygame.font.init()
pygame.init()
# Thiết lập một số hằng số
WIDTH_MAIN = 800
WIDTH, HEIGHT = 600, 600

# Tạo màn hình
screen = pygame.display.set_mode((WIDTH_MAIN, HEIGHT))


line_1 = 3
markers = []
pos = []
winner = 0
playerv = 1
game_over = False
clicked = False
green = (0, 255, 0)
gray = (117, 135, 167)
red = (255, 0, 0)
gray_light = (200, 200, 200)
blue = (0, 0, 255)
font = pygame.font.SysFont(None, 40)
again_rect = Rect(WIDTH + 30, HEIGHT - 115, 140, 50)
font_pl = pygame.font.SysFont(None, 35)
fontx = pygame.font.SysFont(None, 25)


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
def draw_grid(screen):
        bg = (255, 255, 255)
        grid = (128, 128, 128)
        screen.fill(bg)
        for x in range(1, 10):
            pygame.draw.line(screen, grid, (0, x * 60), (WIDTH, x * 60), line_1)
            pygame.draw.line(screen, grid, (x * 60, 0,), (x * 60, HEIGHT), line_1)


    # Vẽ thông báo người chiến thắng
def draw_winner(screen):
        win_text = 'Player:' + str(winner) + ' win!'
        win_img = font_pl.render(win_text, True, blue)
        screen.blit(win_img, (WIDTH + 20, HEIGHT -350))



def redrawWindow(win, game, p,WIDTH,HEIGHT,blue,gray,again_rect,markers):
    bg = (255, 255, 255)
    win.fill(bg)

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", True, (255,0,0), True)
        win.blit(text, (WIDTH/2 - text.get_width()/2,HEIGHT/2 - text.get_height()/2))
    else:

        draw_grid(win)

        font = pygame.font.SysFont("comicsans", 60)
        font1 = pygame.font.SysFont("comicsans", 35)
        # text = font.render("Your Move", 1, (0, 255,255))
        # win.blit(text, (80, 200))
        win_img = font1.render("Caro", 1, (0, 0, 255))
        win.blit(win_img, (600 + 60, 600 - 570))
        win_x = fontx.render("10x10", 1, (0, 0, 255))
        win.blit(win_x, (670, 600 - 520))
        win_xpl = font_pl.render("Player turn:", True, blue)
        screen.blit(win_xpl, (WIDTH + 30, HEIGHT - 460))
        again_img = font_pl.render("Reset", 1, (0, 0, 255))
        pygame.draw.rect(win, gray, again_rect)
        win.blit(again_img, (670, 500))


        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        text1 = font1.render("", 1, (0,0,0))
        text2 = font1.render("", 1, (0, 0, 0))
        font2 = pygame.font.SysFont("comicsans", 19)

        if game.p1Went and p == 0:
            text1 = font2.render("turn player2", 1, (0,0,0))
        elif game.p1Went:
            text1 = font2.render("Your turn", 1, (0, 0, 0))
        # else:
        #     text1 = font1.render("Your turn", 1, (0, 0, 0))
            # for event in pygame.event.get():
            #     player=1
            #     if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            #         clicked = True
            #     if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            #         clicked = False
            #
            #         pos = pygame.mouse.get_pos()
            #         cell_x = pos[0] // 60
            #         cell_y = pos[1] // 60
            #         if 0 <= cell_x < 10 and 0 <= cell_y < 10:
            #             if markers[cell_x][cell_y] == 0:
            #                 markers[cell_x][cell_y] = 1

                            # game.check_winner(markers)

        if game.p2Went and p == 1:
            text2 = font2.render("turn player2", 1, (0,0,0))
        elif game.p2Went:
            text2 = font2.render("Your turn", 1, (0, 0, 0))
        # else:
        #     text2 = font1.render("Your turn ", 1, (0, 0, 0))
            # for event in pygame.event.get():
            #     if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            #         clicked = True
            #     if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            #         clicked = False
            #         pos = pygame.mouse.get_pos()
            #         cell_x = pos[0] // 60
            #         cell_y = pos[1] // 60
            #         if 0 <= cell_x < 10 and 0 <= cell_y < 10:
            #             if markers[cell_x][cell_y] == 0:
            #                 markers[cell_x][cell_y] = -1

                            # game.check_winner(markers)

        if p == 1:
            win.blit(text2, (600 + 30, 600 - 430))
            win.blit(text1, (600 + 30, 600 - 430))
        else:
            win.blit(text1, (600 + 30, 600 - 430))
            win.blit(text2, (600 + 30, 600 - 430))
        # for btn in btns:
        #     btn.draw(win)

    pygame.display.update()




# btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]
def main(screen):
    run = True
    clicked = False
    n = Network()
    player = int(n.getP())



    for x in range(10):
        row = [0] * 10
        markers.append(row)
    print(markers)
    # draw_OX(screen, markers)

    while run:

        # clock.tick(60)

        # draw_home(w)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game2")
            break

        if game.bothWent() and game_over==True:
            # redrawWindow(screen, game, player)
            pygame.time.delay(500)
            # game.resetmove()
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game1")
                break

            font = pygame.font.SysFont("comicsans", 90)
            # if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
            #     text = font.render("You Won!", 1, (255,0,0))
            # elif game.winner() == -1:
            #     text = font.render("Tie Game!", 1, (255,0,0))
            # else:
            #     text = font.render("You Lost...", 1, (255, 0, 0))
            #
            # screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            # pygame.display.update()
            pygame.time.delay(5000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if game.connected():

                if player == 0:
                    if not game.p1Went:
                        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                            clicked = True
                        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                            clicked = False

                            pos = pygame.mouse.get_pos()
                            cell_x = pos[0] // 60
                            cell_y = pos[1] // 60
                            print(cell_x, cell_y)
                            if 0 <= cell_x < 10 and 0 <= cell_y < 10:
                                n.send("V")

                                if markers[cell_x][cell_y] == 0:
                                    markers[cell_x][cell_y] = 1
                                    print(markers)




                        # if game.bothWent:
                        #     game.p2Went = False
                        #     game.resetmove()

                else:
                    if not game.p2Went:
                        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                            clicked = True
                        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                            clicked = False
                            pos = pygame.mouse.get_pos()
                            cell_x = pos[0] // 60
                            cell_y = pos[1] // 60


                            print(cell_x,cell_y)


                            if 0 <= cell_x < 10 and 0 <= cell_y < 10:

                                n.send("R")
                                if markers[cell_x][cell_y] == 0:
                                    markers[cell_x][cell_y] = -1
                                    print(markers)



                        # if game.bothWent:
                        #     game.p1Went = False
                        #     game.resetmove()







            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
                # for btn in btns:
                #     if btn.click(pos) and game.connected():
                #         if player == 0:
                #             if not game.p1Went:
                #                 n.send(btn.text)
                #         else:
                #             if not game.p2Went:
                #                 n.send(btn.text)

        redrawWindow(screen, game, player,WIDTH,HEIGHT,blue,gray,again_rect,markers)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        screen.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        screen.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main(screen)

while True:
    menu_screen()