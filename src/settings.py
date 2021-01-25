"""
Module to hold a class for Settings.
"""

class Settings:
    def __init__(self, nrows: int, ncols: int, player_color: (int, int, int)):
        self.nrows = nrows
        self.ncols = ncols
        self.player_color = player_color
