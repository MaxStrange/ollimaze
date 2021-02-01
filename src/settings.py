"""
Module to hold a class for Settings.
"""

class Settings:
    def __init__(self, nrows: int, ncols: int, player_color: (int, int, int), n_random_walks: int, alloted_time_ms: int, desired_coverage: float, fps: int,
                       path_color: (int, int, int), wall_color: (int, int, int), goal_color: (int, int, int)):
        self.nrows = nrows
        self.ncols = ncols
        self.player_color = player_color
        self.n_random_walks = n_random_walks
        self.alloted_graph_creation_time_ms = alloted_time_ms
        self.desired_coverage = desired_coverage
        self.fps = fps
        self.path_color = (255, 255, 255)
        self.wall_color = (0, 0, 0)
        self.goal_color = (0, 255, 0)
