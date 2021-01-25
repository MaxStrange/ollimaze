"""
A Maze game that returns `True` if the user wants to exit, otherwise returns `False`.
The main loop should create a new Maze instance and play it again in that case.
"""
import pygame
import src.display as display      # pylint: disable=import-error
import src.settings as setts       # pylint: disable=import-error
import src.mazegraph as mazegraph  # pylint: disable=import-error

from pygame.locals import (  # pylint: disable=no-member,no-name-in-module
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


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
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    done, should_quit = self._handle_keydown_event(event)
                    if done and should_quit:
                        return True
                    elif done:
                        return False
                elif event.type == QUIT:
                    return True

    def _handle_keydown_event(self, event) -> (bool, bool):
        """
        Handles the user pushing a button by adjusting state and redrawing
        the parts that changed.

        Returns:
        - (True, True) -> User wants to quit
        - (True, False) -> User has finished this maze
        - (False, *) -> User is not done yet
        """
        wants_to_quit = (True, True)
        finished_maze = (True, False)
        still_playing = (False, None)

        if event.key == K_UP:
            # Move the agent up
            finished = self._move(K_UP)
        elif event.key == K_DOWN:
            # Move the agent down
            finished = self._move(K_DOWN)
        elif event.key == K_LEFT:
            # Move the agent left
            finished = self._move(K_LEFT)
        elif event.key == K_RIGHT:
            # Move the agent right
            finished = self._move(K_RIGHT)
        elif event.key == K_ESCAPE:
            # User wants to quit
            return *wants_to_quit

        if finished:
            return *finished_maze
        else:
            return *still_playing

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
        middle_column = int(self._settings.ncols * 0.5)
        middle_row = int(self._settings.nrows * 0.5)

        # Set up the start cell
        start = graph.get_node(0, middle_row)
        start.is_start = True
        start.has_player = True
        start.is_wall = False

        # Set up the end cell (the goal)
        end = graph.get_node(middle_column, 0)
        end.is_finish = True
        end.is_wall = False

        for c in range(0, middle_column + 1):
            node = graph.get_node(c, middle_row)
            node.is_wall = False

        for r in range(0, middle_row):
            node = graph.get_node(middle_column, r)
            node.is_wall = False

    def _move(self, direction) -> bool:
        """
        Moves the agent in the given direction, if possible.
        Draws the result.
        Returns True if reached the goal, False otherwise.
        """
        current_agent_node = self._maze.get_player_node()

        if direction == K_UP:
            # TODO:
            pass
