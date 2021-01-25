"""
A Maze game that returns `True` if the user wants to exit, otherwise returns `False`.
The main loop should create a new Maze instance and play it again in that case.
"""
import pygame
import src.display as display      # pylint: disable=import-error
import src.settings as setts       # pylint: disable=import-error
import src.mazegraph as mazegraph  # pylint: disable=import-error


class Maze:
    def __init__(self, settings: setts.Settings):
        """
        A Maze.
        """
        self._settings = settings
        self._maze = self._create_new_maze(self._settings)
        self._screen = display.make_screen(self._settings)

    def play(self) -> bool:
        """
        Allows the user to play through the maze or quit.

        Returns True if we want quit, False if we want to play again.
        """
        self._draw()

        # Allow the player to control the agent, redrawing only the cells that change, as we go
        while True:
            pass

    def _create_new_maze(self, settings: setts.Settings) -> mazegraph.MazeGraph:
        """
        Creates a new MazeGraph data structure, with cells which connect
        to one another in a way that is based on the settings.
        """
        graph = mazegraph.MazeGraph(settings.nrows, settings.ncols)

        # TODO: Create the graph
        self._make_debug_graph(graph)

        return graph

    def _draw(self):
        """
        Draw the maze in full.
        """
        display.draw_maze(self._screen, self._maze, self._settings)
        pygame.display.flip()

    def _make_debug_graph(self, graph: mazegraph.MazeGraph):
        """
        Adjust all the nodes in the given graph so that we have a simple path from
        start to finish.
        """
        start = graph.get_node(int(self._settings.ncols * 0.5), 0)
        start.is_start = True
        start.has_player = True
        start.is_wall = False

        end = graph.get_node(0, int(self._settings.nrows * 0.5))
        end.is_finish = True
        end.is_wall = False
