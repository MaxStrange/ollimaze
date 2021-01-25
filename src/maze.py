"""
A Maze game that returns `True` if the user wants to exit, otherwise returns `False`.
The main loop should create a new Maze instance and play it again in that case.
"""
import pygame
import src.settings as setts       # pylint: disable=import-error
import src.mazegraph as mazegraph  # pylint: disable=import-error


class Maze:
    def __init__(self, settings: setts.Settings):
        """
        A Maze.
        """
        self.settings = settings
        self._maze = self._create_new_maze(self.settings)

    def play(self) -> bool:
        """
        Allows the user to play through the maze or quit.

        Returns True if we want quit, False if we want to play again.
        """
        # Draw the maze
        # TODO

        # Allow the player to control the agent, redrawing only the cells that change, as we go
        while True:
            pass

    def _create_new_maze(self, settings: setts.Settings) -> mazegraph.MazeGraph:
        """
        Creates a new MazeGraph data structure, with cells which connect
        to one another in a way that is based on the settings.
        """
        return mazegraph.MazeGraph(settings.nrows, settings.ncols)
