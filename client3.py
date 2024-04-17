import pygame
from network import Network
import random
from pygame.locals import Rect
import pickle
pygame.font.init()
pygame.init()
# Thiết lập một số hằng số
WIDTH_MAIN = 900
WIDTH, HEIGHT = 600, 600

# Tạo màn hình
screen = pygame.display.set_mode((WIDTH_MAIN, HEIGHT))


line_1 = 3
markers = []
pos = []
winner = 0
playerv = 1
clicked = False
green = (0, 255, 0)
gray = (117, 135, 167)
red = (255, 0, 0)
gray_light = (200, 200, 200)
blue = (0, 0, 255)
font = pygame.font.SysFont(None, 40)
again_rect = Rect(WIDTH + 30, HEIGHT - 115, 140, 50)
font_max = pygame.font.SysFont(None, 40)
font_pl = pygame.font.SysFont(None, 35)
font_pl1 = pygame.font.SysFont(None, 26)
fontx = pygame.font.SysFont(None, 25)
text_part = ""
input_text = ""


class Chat:
    def __init__(self,text):
        self.text =text

chat_box = Chat("")
Name = Chat("")
def draw_grid(screen,game):
        bg = (255, 255, 255)
        grid = (128, 128, 128)
        screen.fill(bg)
        for x in range(1, 10):
            pygame.draw.line(screen, grid, (0, x * 60), (WIDTH, x * 60), line_1)
            pygame.draw.line(screen, grid, (x * 60, 0,), (x * 60, HEIGHT), line_1)
        for cell in game.find_winning_cells():
            x, y = cell
            pygame.draw.rect(screen, blue, (x * 60, y * 60, 60, 60), 3)

        pygame.draw.line(screen, (128,128,128), (600, 0), (600, 600), 2)
        pygame.draw.line(screen, (128,128,128), (0, 600), (800, 600), 2)
def redrawWindow(win, game, p,WIDTH,HEIGHT):
    bg = (255, 255, 255)
    win.fill(bg)

    if not(game.connected()):
        original_image = pygame.image.load("Images/loading.png")
        background_image = pygame.transform.scale(original_image, (900, 600))
        win.blit(background_image, (0, 0))
        font = pygame.font.SysFont(None, 35)
        text = font_pl.render("Waiting Other Player...", True, (255,255,255))
        win.blit(text, (320,380))
    else:
        draw_grid(win,game)
        font = pygame.font.SysFont("comicsans", 60)
        font1 = pygame.font.SysFont("comicsans", 35)

        win_img = font_max.render("CARO", 1, (0, 0, 255))
        win.blit(win_img, (600 + 120, 600 - 570))
        win_x = font_pl1.render("10x10", 1, (0, 0, 255))
        win.blit(win_x, (670+60, 600 - 540))
        win_xpl = font_pl.render("Player turn:", True, blue)
        screen.blit(win_xpl, (WIDTH + 90, HEIGHT - 430))

        text1 = font1.render("", 1, (0,0,0))
        text2 = font1.render("", 1, (0, 0, 0))
        font2 = pygame.font.SysFont("comicsans", 19)

        if game.p1Went and p == 0:
            text1 = font_pl1.render("Turn player 2", 1, (0,0,0))
        elif game.p1Went:
            text1 = font_pl1.render("Your turn", 1, (0, 0, 0))

        if game.p2Went and p == 1:
            text2 = font_pl1.render("Turn player 2", 1, (0,0,0))
        elif game.p2Went:
            text2 = font_pl1.render("Your turn", 1, (0, 0, 0))
        
        # original_image6 = pygame.image.load("Images/boxchat.png")
        # background_image3 = pygame.transform.scale(original_image6, (280, 250))
        # win.blit(background_image3, (610, 320))
        pygame.draw.rect(screen, (0,0,0), (610, 320, 280, 250), 1)
        original_image1 = pygame.image.load("Images/chat.png")
        background_image2 = pygame.transform.scale(original_image1, (260, 50))
        win.blit(background_image2, (620, 504))


        fontchat =pygame.font.SysFont("comicsans", 15)
        text_surface1 = fontchat.render(chat_box.text, True, (0, 0, 0))
        screen.blit(text_surface1, (680, 518))

        text_surface2 = fontchat.render( game.input_text, True, (0, 0, 0))
        screen.blit(text_surface2, (640, 410))
        text_surface3 = fontchat.render( game.text_part, True, (0, 0, 0))
        screen.blit(text_surface3, (640, 370 ))

        textp1 = font_pl1.render("You:", 1, (0, 0, 255))
        win.blit(textp1, (WIDTH + 130, HEIGHT - 500))
        textp1 = font_pl1.render("Opponent name: ", 1, (0, 0, 255))
        win.blit(textp1, (WIDTH + 60, HEIGHT - 460))



        if p == 1:
            win.blit(text2, (600 + 105, 600 - 400))
            win.blit(text1, (600 + 110, 600 - 400))
            textp1 = font_pl1.render("O", 1, (255, 0, 0))
            win.blit(textp1, (WIDTH + 167, HEIGHT - 500))
            textp1x = font_pl1.render(game.namep1, 1, (0, 0, 0))
            win.blit(textp1x, (WIDTH + 207, HEIGHT - 460))


        else:
            win.blit(text1, (600 + 105, 600 - 400))
            win.blit(text2, (600 + 110, 600 - 400))
            textp1 = font_pl1.render("X", 1, (0, 255, 0))
            win.blit(textp1, (WIDTH + 167, HEIGHT - 498))
            textp1x = font_pl1.render(game.namep2, 1, (0, 0, 0))
            win.blit(textp1x, (WIDTH + 207, HEIGHT - 460))


        x_pos = 0
        for x in range(len(game.markers)):
            y_pos = 0
            for y in range(len(game.markers[x])):
                if game.markers[x][y] == 1:
                    if (x, y) == game.last_selected:
                        pygame.draw.rect(screen, (253, 222, 167), (x_pos * 60 + 2, y_pos * 60 + 2, 57, 57))
                        pygame.draw.line(screen, green, (x_pos * 60 + 10, y_pos * 60 + 10),
                                         (x_pos * 60 + 45, y_pos * 60 + 45), 3)
                        pygame.draw.line(screen, green, (x_pos * 60 + 10, y_pos * 60 + 45),
                                         (x_pos * 60 + 45, y_pos * 60 + 10), 3)
                    else:
                        pygame.draw.line(screen, green, (x_pos * 60 + 10, y_pos * 60 + 10),
                                         (x_pos * 60 + 45, y_pos * 60 + 45), line_1)
                        pygame.draw.line(screen, green, (x_pos * 60 + 10, y_pos * 60 + 45),
                                         (x_pos * 60 + 45, y_pos * 60 + 10), line_1)
                if game.markers[x][y] == -1:
                    if (x, y) == game.last_selected:
                        pygame.draw.rect(screen, (253, 222, 167), (x_pos * 60 + 2, y_pos * 60 + 2, 57, 57))
                        pygame.draw.circle(screen, red, (x_pos * 60 + 30, y_pos * 60 + 30), 24, 3)
                    else:
                        pygame.draw.circle(screen, red, (x_pos * 60 + 30, y_pos * 60 + 30), 24, line_1)
                y_pos += 1
            x_pos += 1



    pygame.display.update()

def main(screen):
    run = True
    clicked = False
    clock = pygame.time.Clock()

    n = Network()
    player = int(n.getP())
    n.send("name|" + Name.text)

    for x in range(10):
        row = [0] * 10
        markers.append(row)



    while run:

        clock.tick(60)


        # draw_home(w)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game2")
            break
        player_win=game.check_winner()

        if game.game_over:
            redrawWindow(screen, game, player, WIDTH, HEIGHT)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game1")
                break

            print(player,"--",player_win)

            if (player == 0 and player_win == 1) or (player == 1 and player_win == 2):
                # print(player, "sadasd", player_win)
                font2 = pygame.font.SysFont("comicsans", 20)
                win_text1 = 'Win'
                win_img1 = font_pl.render(win_text1, True, (0, 0, 255))
                screen.blit(win_img1, (600 + 120, 600 - 350))
            elif (player == 0 and player_win == 3) or (player == 1 and player_win == 3):
                font2 = pygame.font.SysFont("comicsans", 20)
                win_text = 'Hòa'
                win_img = font_pl.render(win_text, True, (0, 0, 255))
                screen.blit(win_img, (600 + 120, 600 - 350))
            else:
                win_text1 = 'Thua'
                win_img1 = font_pl.render(win_text1, True, (0, 0, 255))
                screen.blit(win_img1, (600 + 120, 600 - 350))
            pygame.display.update()

            pygame.time.delay(5000)
        print(game.namep2+"a")





        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if game.connected():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        chat_box.text = chat_box.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if player == 0:

                            text = game.namep1+ ": " + chat_box.text
                            n.send("chat|" + text)
                        else:
                            text = game.namep2 + ": " + chat_box.text
                            n.send("chat|" + text)
                        chat_box.text = ""
                    else:

                        if event.unicode:  # Chỉ xử lý khi có ký tự Unicode
                            if len(chat_box.text + event.unicode) <= 20:
                                chat_box.text += event.unicode
                if player == 0:
                    if not game.p1Went:
                        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                            clicked = True
                        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                            clicked = False

                            pos = pygame.mouse.get_pos()
                            cell_x = pos[0] // 60
                            cell_y = pos[1] // 60

                            if 0 <= cell_x < 10 and 0 <= cell_y < 10:
                                if game.markers[cell_x][cell_y] == 0:
                                    coord_str = str(cell_x) + ',' + str(cell_y)
                                    n.send(coord_str)
                                    game.markers[cell_x][cell_y] = 1




                else:
                    if not game.p2Went:
                        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                            clicked = True
                        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                            clicked = False
                            pos = pygame.mouse.get_pos()
                            cell_x = pos[0] // 60
                            cell_y = pos[1] // 60

                            if 0 <= cell_x < 10 and 0 <= cell_y < 10:
                                if game.markers[cell_x][cell_y] == 0:
                                    game.markers[cell_x][cell_y] = -1

                                    coord_str = str(cell_x) + ',' + str(cell_y)
                                    n.send(coord_str)

        redrawWindow(screen, game, player,WIDTH,HEIGHT)


def menu_screen():
    run = True
    clock = pygame.time.Clock()


    while run:
        clock.tick(60)
        screen.fill((255, 255, 255))
        original_image = pygame.image.load("Images/start.jpg")
        background_image = pygame.transform.scale(original_image,(900, 600))
        screen.blit(background_image, (0, 0))


        fontchat =pygame.font.SysFont(None, 34)
        text_surface1 = fontchat.render("Enter Name: "+Name.text, True, (255, 255, 255))
        screen.blit(text_surface1, (330, 108))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                   Name.text = Name.text[:-1]
                elif event.key == pygame.K_RETURN:
                    text = Name.text
                    if len(Name.text) > 0:
                        # n.send("name|" + text)
                        run = False

                else:

                    if event.unicode:
                        if len(Name.text + event.unicode) <= 14:
                            Name.text += event.unicode
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     run = False
    main(screen)
while True:
    menu_screen()