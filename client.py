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
        win.blit(text, (380, 200))

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