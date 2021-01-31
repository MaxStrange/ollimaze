import random
import src.settings as setts       # pylint: disable=import-error
import src.mazegraph as mazegraph  # pylint: disable=import-error


class BrownianAgent:
    """
    Agent that creates paths in the graph by way of Brownian motion (random walk).
    """
    def __init__(self, graph: mazegraph.MazeGraph):
        self._graph = graph
        self._current_node = graph._start_node

    def solve(self):
        """
        Random walk from start to finish, following usual rules.
        """
        done = False
        while not done:
            # Take a random step, governed by some rules
            node = self._step()

            # Check if we successfully took a step. If not, we need to
            # move to a new location and start over
            if node is None:
                self._backtrack()
            else:
                node.is_wall = False
                self._current_node = node

            if self._current_node.up.is_finish:
                done = True
            elif self._current_node.down.is_finish:
                done = True
            elif self._current_node.left.is_finish:
                done = True
            elif self._current_node.right.is_finish:
                done = True

    def form_path(self):
        """
        Random walk that ends... eventually.... TODO
        """
        pass  # TODO

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
            print("Node is illegal: None")
            return False
        elif self._graph.node_is_edge(node):
            print("Node is illegal: Edge")
            return False
        elif not node.is_wall:
            print("Node is illegal: Not a wall")
            return False

        # Those are all the easy ones. Now let's check if the node is adjacent to the goal
        # node (in which case, it is legal)
        adjacent_nodes = [node.left, node.up, node.right, node.down]
        if any([n.is_finish for n in adjacent_nodes]):
            print("Node is legal: Connected to finish")
            return True

        # Otherwise, if the node is adjacent to a path node, it is not legal (unless of course, that node is our current one)
        for n in adjacent_nodes:
            path_nodes_adjacent_to_node = [n for n in adjacent_nodes if not n.is_wall]
            for adj_n in path_nodes_adjacent_to_node:
                if not adj_n.is_wall and not adj_n.is_same_as(self._current_node):
                    return False

        # Otherwise, it is legal
        return True

    def _backtrack(self):
        """
        Set self._current_node to a node that has at least one legal node neighbor
        by moving along the path.
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
                self._debug_show_maze()
                # assert possible_nodes, f"Possible nodes is empty ({possible_nodes}). Cannot backtrack."

            self._current_node = random.choice(possible_nodes)
            done = any([self._node_is_legal(n) for n in [self._current_node.left, self._current_node.up, self._current_node.right, self._current_node.down]])

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

    # Make the finish node
    end_node = graph.get_node(int(random.uniform(0, settings.ncols - 1)), int(random.uniform(0, settings.nrows - 1)))
    while end_node.x == start_node.x and end_node.y == start_node.y:
        end_node = graph.get_node(int(random.uniform(0, settings.ncols - 1)), int(random.uniform(0, settings.nrows - 1)))
    end_node.is_wall = False
    end_node.is_finish = True

    # Make a random agent and have that agent do several walks through the maze, creating pathways as it goes
    agent = BrownianAgent(graph)
    agent.solve()

    for _ in range(settings.n_random_walks):
        agent.form_path()
