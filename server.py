import socket
from _thread import *

import pickle
from game import Game
from config import Config

config = Config()
server = config.get_host()
port = config.get_port()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print("Server started. Waiting for a connection...")

connected = set()
games = {}
id_count = 0

def threaded_client(conn, player, game_id):
    global id_count
    conn.send(str.encode(str(player)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            if game_id in games:
                game = games[game_id]

                if not data:
                    break;
                else:
                    if data == "reset":
                        game.reset_players_move()
                    elif data != "get":
                        game.play(player, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break;
        except:
            break;
    print("Connection lost.")
    try:
        del games[game_id]
        print(f"Aborting game: {game_id}")
    except:
        pass
    id_count -= 1
    conn.close()


while True:
    # when someone connects
    conn, addr = s.accept()
    print(f"Connected to: {addr}")

    id_count  += 1
    player = 0
    # every two people that connects to the server
    # we are going to increment the game_id by 1
    game_id = (id_count-1)//2

    if id_count%2 == 1:
        games[game_id] = Game(game_id)
        print("New game created.")
    else:
        games[game_id].ready = True
        player = 1
    start_new_thread(threaded_client, (conn, player, game_id))