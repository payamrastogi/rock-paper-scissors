import pygame
from network import Network
import pickle
from button import Button
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redraw_window(win, game, player):
    win.fill((128, 128, 128))
    if not game.connected():
        font=pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for a Player", 1, (255, 0, 0), True)
        win.blit(text, (width/2-text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your move", 1, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Opponent", 1, (0, 255, 255))
        win.blit(text, (380 , 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.both_players_move_locked():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1_move_locked and player == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1_move_locked:
                text1 = font.render("Locked in", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting", 1, (0, 0, 0))

            if game.p2_move_locked and player == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2_move_locked:
                text2 = font.render("Locked in", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting", 1, (0, 0, 0))

            if player == 1:
                win.blit(text2, (100, 350))
                win.blit(text1, (400, 350))
            else:
                win.blit(text1, (100, 350))
                win.blit(text2, (400, 350))
        for button in buttons:
            button.draw(win)

    pygame.display.update()



buttons = [Button("Rock", 50, 500, (0, 0, 0)), Button("Scissors", 250, 500, (255, 0, 0)),  Button("Paper", 250, 500, (0, 255, 0))]

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.get_player())
    print(f"You are player {player}")

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        if game.both_players_move_locked():
            # draw player moves
            redraw_window()
            # so that player can see what button they clicked
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break
            font = pygame.font.SysFont("comicsans", 90)
            if game.winner() == player:
                text = font.render("You won!", 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie!", 1, (255, 0, 0))
            else:
                text = font.render("You lost!", 1, (255, 0, 0))
            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.quit():
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1_move_locked:
                                n.send(button.text)
                        else:
                            if not game.p2_move_locked:
                                n.send(button.text)
        redraw_window(win, game, player)

main()