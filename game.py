class Game:
    # current game id
    def __init__(self, id):
        self.p1_move_locked = False
        self.p2_move_locked = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, player):
        """
        :param player: 0 and 1 only
        :return: move
        """
        return self.moves[player]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1_move_locked = True
        else:
            self.p2_move_locked = True

    def connected(self):
        return self.ready

    def both_players_move_locked(self):
        return self.p1_move_locked and self.p2_move_locked

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def reset_players_move(self):
        self.p1_move_locked = False
        self.p2_move_locked = False