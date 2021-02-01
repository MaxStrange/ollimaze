import random
import src.settings as setts       # pylint: disable=import-error
import src.mazegraph as mazegraph  # pylint: disable=import-error
import time


def _get_time_ms():
    """
    Returns the current time in ms.
    """
    return time.time() * 1000


class BrownianAgent:
    """
    Agent that creates paths in the graph by way of Brownian motion (random walk).
    """
    def __init__(self, graph: mazegraph.MazeGraph, alloted_time_ms: int):
        self._graph = graph
        self._current_node = graph._start_node
        self._alloted_time = alloted_time_ms

    def solve(self) -> bool:
        """
        Random walk from start to finish, following usual rules.

        Return False if it fails to solve it within reasonable time bounds.
        """
        # Start from the start node
        self._current_node = self._graph._start_node

        # Only try for a certain amount of time before giving up
        start_time_ms = _get_time_ms()
        done = False
        while not done:
            # Take a random step, governed by some rules
            node = self._step()

            # Check if we successfully took a step. If not, we need to
            # move to a new location and start over
            if node is None:
                ret = self._backtrack(start_time_ms)
                if not ret:
                    return False
            else:
                node.is_wall = False
                self._current_node = node

            if self._current_node.up is not None and self._current_node.up.is_finish:
                done = True
            elif self._current_node.down is not None and self._current_node.down.is_finish:
                done = True
            elif self._current_node.left is not None and self._current_node.left.is_finish:
                done = True
            elif self._current_node.right is not None and self._current_node.right.is_finish:
                done = True

            if (time.time() * 1000) - start_time_ms >= self._alloted_time:
                print("Ran out of time during solve.")
                return False

        return True

    def form_path(self, n_total_walks: int):
        """
        Random walk that ends as soon as it can't take any more legal steps (i.e., no backtracking).
        """
        start_time_ms = time.time() * 1000
        self._current_node = random.choice(self._graph.get_all_path_nodes())

        done = False
        while not done:
            node = self._step()
            if node is None:
                done = True
            else:
                node.is_wall = False
                self._current_node = node

            if (time.time() * 1000) - start_time_ms >= self._alloted_time / n_total_walks:
                return

    def _step(self) -> mazegraph.MazeCell:
        """
        Takes a step in a legal direction and sets self._current_node to the node that we land on.
        If no node is legal, we set it to None.
        """
        our_neighbor_nodes = [self._current_node.left, self._current_node.up, self._current_node.right, self._current_node.down]
        our_neighbor_nodes = [n for n in our_neighbor_nodes if n is not None]
        our_neighbor_nodes = [n for n in our_neighbor_nodes if self._node_is_legal(n)]
        if our_neighbor_nodes:
            return random.choice(our_neighbor_nodes)
        else:
            return None

    def _node_is_legal(self, node: mazegraph.MazeCell) -> bool:
        """
        Returns if the given node is legal to move to.

        A node is legal to move to if it follows these rules:

        - It is not None
        - It is not an edge node
        - It is not a path node (it must be a wall)
        - It is not already attached to at least one path (unless that node is the finish)

        """
        if node is None:
            return False
        elif self._graph.node_is_edge(node):
            # This is actually legal if and only if the current node is the start node and the start node is in a corner
            if self._current_node.is_start and self._current_node.is_corner:
                return True
            else:
                return False
        elif not node.is_wall:
            return False

        # Those are all the easy ones. Now let's check if the node is adjacent to the goal
        # node (in which case, it is legal)
        adjacent_nodes = [node.left, node.up, node.right, node.down]
        if any([n.is_finish for n in adjacent_nodes]):
            return True

        # Otherwise, if the node is adjacent to a path node, it is not legal (unless of course, that node is our current one)
        for n in adjacent_nodes:
            path_nodes_adjacent_to_node = [n for n in adjacent_nodes if not n.is_wall]
            for adj_n in path_nodes_adjacent_to_node:
                if not adj_n.is_wall and not adj_n.is_same_as(self._current_node):
                    return False

        # Otherwise, it is legal
        return True

    def _backtrack(self, start_time_ms: int) -> bool:
        """
        Set self._current_node to a node that has at least one legal node neighbor
        by moving along the path.

        If we fail to finish this within the alloted time, we return False. Otherwise
        we return True.
        """
        assert self._current_node is not None
        visited = set()
        done = False
        while not done:
            visited.add(self._current_node)
            # Choose a direction. Any adjacent node that is not a wall is fine, unless I already came from that direction.
            possible_nodes = [self._current_node.left, self._current_node.up, self._current_node.right, self._current_node.down]
            possible_nodes = [node for node in possible_nodes if node is not None]
            possible_nodes = [node for node in possible_nodes if not node.is_wall]
            possible_nodes = [node for node in possible_nodes if node not in visited]
            if not possible_nodes:
                # We've back tracked into a corner. Just jump to a random spot.
                possible_nodes = self._graph.get_all_path_nodes()
                visited = set()
                # self._debug_show_maze()

            self._current_node = random.choice(possible_nodes)
            done = any([self._node_is_legal(n) for n in [self._current_node.left, self._current_node.up, self._current_node.right, self._current_node.down]])

            if (time.time() * 1000) - start_time_ms >= self._alloted_time:
                print("Ran out of time during backtrack.")
                return False

        return True

    def _debug_show_maze(self):
        # Dump everything
        print(f"Current Node: {self._current_node}")
        print(f"Start Node:   {self._graph.get_start_node()}")
        print(f"End Node:     {self._graph.get_end_node()}")

        # Display everything
        import pygame
        import src.display as display  # pylint: disable=import-error
        screen = display.make_screen(self._graph._settings)
        display.draw_maze(screen, self._graph, self._graph._settings)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:  # pylint: disable=no-member
                    exit()


def generate_random_maze(graph: mazegraph.MazeGraph, settings: setts.Settings):
    """
    Changes the state of `graph` to update its nodes so that the result is a maze that
    is solveable and random.
    """
    # Make the start node
    start_node = graph.get_node(int(random.uniform(0, settings.ncols - 1)), int(random.uniform(0, settings.nrows - 1)))
    start_node.is_wall = False
    start_node.is_start = True
    start_node.has_player = True

    # Make the finish node (make sure that the end_node is not the same as the start_node)
    end_node = graph.get_node(int(random.uniform(0, settings.ncols - 1)), int(random.uniform(0, settings.nrows - 1)))
    while (end_node.x == start_node.x and end_node.y == start_node.y) or end_node.is_corner:
        end_node = graph.get_node(int(random.uniform(0, settings.ncols - 1)), int(random.uniform(0, settings.nrows - 1)))
    end_node.is_wall = False
    end_node.is_finish = True

    # Make a random agent and have that agent do several walks through the maze, creating pathways as it goes
    agent = BrownianAgent(graph, settings.alloted_graph_creation_time_ms)

    # The agent can run out of time trying to solve a maze... because there is probably a bug in the algorithm,
    # and since this is just a crappy throwaway program I wrote in a few hours, I can't really justify fixing it...
    solved = agent.solve()
    while not solved:
        solved = agent.solve()

    # Max out at n_random_walks, but otherwise try to achieve a certain coverage instead.
    nwalks = 0
    while nwalks < settings.n_random_walks and (len(graph.get_all_path_nodes()) / len(graph._nodes)) < settings.desired_coverage:
        agent.form_path(settings.n_random_walks)
        nwalks += 1
