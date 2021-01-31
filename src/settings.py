"""
Module to hold a class for Settings.
"""

class Settings:
    def __init__(self, nrows: int, ncols: int, player_color: (int, int, int), n_random_walks: int, alloted_time_ms: int):
        self.nrows = nrows
        self.ncols = ncols
        self.player_color = player_color
        self.n_random_walks = n_random_walks
        self.alloted_graph_creation_time_ms = alloted_time_ms
