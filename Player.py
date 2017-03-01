"""
Player.py

This is the player class for the CE game.

Created by Eunika Wu on 28 Feb, 2017.
"""
from __future__ import division

class Player:
    def __init__(self):
        self.coins = []
        self.trust = []
        self.coop = []
        self.score = self.get_score()

    def __str__(self):
        return('Coins:' + str(self.coins) + '\n' + \
               'Trust:' + str(self.trust) + '\n' + 
               'Coop:' + str(self.coop))

    def entrust(self, player, coins):
        coins = int(coins)
        player.coins.append(coins)
        self.coins.append(-coins)
        self.trust.append(coins)

    def cooperate(self, player):
        coins = player.trust[-1]
        player.coins.append(3 * coins)
        self.coins.append(-coins)
        self.coop.append(1)

    def defect(self, player):
        self.coins.append(0)
        player.coins.append(0)
        self.coop.append(-1)

    def get_trust_score(self, rounds):
        return sum(self.trust)/rounds

    def get_coop_score(self, rounds):
        coop = [(item > 0) * item for item in self.coop]
        return sum(coop)/rounds

    def get_score(self):
        return sum(self.coins)