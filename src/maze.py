"""
A Maze game that returns `True` if the user wants to exit, otherwise returns `False`.
The main loop should create a new Maze instance and play it again in that case.
"""
import pygame
import src.display as display      # pylint: disable=import-error
import src.settings as setts       # pylint: disable=import-error
import src.mazegraph as mazegraph  # pylint: disable=import-error
import src.rmg as rmg              # pylint: disable=import-error

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
        self._clock = pygame.time.Clock()

    def play(self) -> bool:
        """
        Allows the user to play through the maze or quit.

        Returns True if we want quit, False if we want to play again.
        """
        self._draw()

        # Allow the player to control the agent, redrawing only the cells that change, as we go
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True

            keys_pressed = pygame.key.get_pressed()
            for key in [K_DOWN, K_LEFT, K_RIGHT, K_UP, K_ESCAPE]:
                if keys_pressed[key]:
                    done, should_quit = self._handle_keydown_event(key)
                    if done and should_quit:
                        return True
                    elif done:
                        return False

            # Go at a reasonable FPS
            self._clock.tick(10)

    def _handle_keydown_event(self, key: int) -> (bool, bool):
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

        finished = False
        if key == K_UP:
            # Move the agent up
            finished = self._move(K_UP)
        elif key == K_DOWN:
            # Move the agent down
            finished = self._move(K_DOWN)
        elif key == K_LEFT:
            # Move the agent left
            finished = self._move(K_LEFT)
        elif key == K_RIGHT:
            # Move the agent right
            finished = self._move(K_RIGHT)
        elif key == K_ESCAPE:
            # User wants to quit
            return wants_to_quit

        if finished:
            return finished_maze
        else:
            return still_playing

    def _create_new_maze(self, settings: setts.Settings) -> mazegraph.MazeGraph:
        """
        Creates a new MazeGraph data structure, with cells which connect
        to one another in a way that is based on the settings.
        """
        graph = mazegraph.MazeGraph(settings.nrows, settings.ncols, settings)

        self._make_random_graph(graph)

        return graph

    def _draw(self):
        """
        Draw the maze in full.
        """
        display.draw_maze(self._screen, self._maze, self._settings)
        pygame.display.flip()

    def _make_random_graph(self, graph: mazegraph.MazeGraph):
        """
        Adjust all the nodes in the given graph so that we have a random maze
        based on settings.
        """
        rmg.generate_random_maze(graph, self._settings)

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

        # Uncomment below if you want to draw across the whole map
        #for c in range(0, self._settings.ncols):
        #    node = graph.get_node(c, middle_row)
        #    node.is_wall = False
        #for r in range(0, self._settings.nrows):
        #    node = graph.get_node(middle_column, r)
        #    node.is_wall = False

    def _move(self, direction) -> bool:
        """
        Moves the agent in the given direction, if possible.
        Draws the result.
        Returns True if reached the goal, False otherwise.
        """
        if direction == K_UP:
            return self._move_up()
        elif direction == K_DOWN:
            return self._move_down()
        elif direction == K_LEFT:
            return self._move_left()
        elif direction == K_RIGHT:
            return self._move_right()
        else:
            raise ValueError(f"This method is not equipped to handle the given key: {direction}")

    def _move_up(self) -> bool:
        """
        Moves the agent up, if possible.

        Returns True if reached the goal, False otherwise.
        """
        current_agent_node = self._maze.get_player_node()

        if current_agent_node.y == 0:
            # Can't go up. Already on the top row
            return False
        else:
            next_node = self._maze.get_node_up(current_agent_node)
            return self._handle_movement(current_agent_node, next_node)

    def _move_down(self) -> bool:
        """
        Moves the agent down, if possible.

        Returns True if reached the goal, False otherwise.
        """
        current_agent_node = self._maze.get_player_node()

        if current_agent_node.y == self._settings.nrows - 1:
            # Can't go down. Already on the bottom row.
            return False
        else:
            next_node = self._maze.get_node_down(current_agent_node)
            return self._handle_movement(current_agent_node, next_node)

    def _move_left(self) -> bool:
        """
        Moves the agent left, if possible.

        Returns True if reached the goal, False otherwise.
        """
        current_agent_node = self._maze.get_player_node()

        if current_agent_node.x == 0:
            # Can't go left. Already at the left-most row.
            return False
        else:
            next_node = self._maze.get_node_left(current_agent_node)
            return self._handle_movement(current_agent_node, next_node)

    def _move_right(self) -> bool:
        """
        Moves the agent to the right, if possible.

        Returns True if reached the goal, False otherwise.
        """
        current_agent_node = self._maze.get_player_node()

        if current_agent_node.x == self._settings.ncols - 1:
            # Can't go right. Already on the right-most column.
            return False
        else:
            next_node = self._maze.get_node_right(current_agent_node)
            return self._handle_movement(current_agent_node, next_node)

    def _handle_movement(self, current_agent_node: mazegraph.MazeCell, next_node: mazegraph.MazeCell) -> bool:
        """
        Handles a legal mvoe by checking for collision with wall and returning if reached the end goal.
        """
        if next_node.is_wall:
            # Can't go that way; it's a wall.
            return False
        else:
            current_agent_node.has_player = False
            next_node.has_player = True
            # TODO: Only redraw the current_agent_node cell and next_node cell
            self._draw()
            return next_node.is_finish
