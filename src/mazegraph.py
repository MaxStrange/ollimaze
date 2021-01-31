"""
Module to hold a MazeGraph class.

The MazeGraph class is the underlying data structure
for a Maze.
"""


class MazeCell:
    """
    A node in the graph, which corresponds to a cell, if you think of the maze as a matrix.
    """
    def __init__(self, x: int, y: int, graph, wall=True):
        """
        Args
        ----
        - x: The x coordinate (leftmost column is zero).
        - y: The y coordinate (topmost column is zero).
        - wall: Are we a wall or an open space?

        """
        self.x = x
        self.y = y
        self.graph = graph
        self.is_wall = wall
        self.up = None
        self.left = None
        self.right = None
        self.down = None
        self._has_player = False
        self._is_start = False
        self._is_finish = False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"({self.x}, {self.y}): Wall: {self.is_wall}; Player: {self.has_player}; Start: {self.is_start}; Finish: {self.is_finish}"

    @property
    def has_player(self):
        return self._has_player

    @has_player.setter
    def has_player(self, value: bool):
        self._has_player = value
        if value:
            self.graph._player_node = self

    @property
    def is_start(self):
        return self._is_start

    @is_start.setter
    def is_start(self, value: bool):
        self._is_start = value
        if value:
            self.graph._start_node = self

    @property
    def is_finish(self):
        return self._is_finish

    @is_finish.setter
    def is_finish(self, value: bool):
        self._is_finish = value
        if value:
            self.graph._end_node = self

    def is_same_as(self, other) -> bool:
        """
        Returns True if we are the same node as the other one.
        """
        return self.x == other.x and self.y == other.y

class MazeGraph:
    """
    A MazeGraph is a graph data structure which can be used to represent a 2D maze.

    Each node is a location (or "cell") in the maze, and is connected to up to four other
    nodes via edges (up, down, right, left).

    This is a data structure, and as such, is mostly for holding the data that it encompasses
    in a useful way, and for providing useful generic functions over that data.

    It does not know, however, how to make a new maze for you. To do that, use the
    methods it provides to make it in whatever way you see fit.
    """
    def __init__(self, nrows: int, ncols: int, settings):
        # Settings
        self._settings = settings

        # Special nodes that we keep track of
        self._start_node = None
        self._end_node = None
        self._player_node = None

        # Nrows and ncols
        self._nrows = nrows
        self._ncols = ncols

        # A list of every node in the graph
        self._nodes = []

        # A list of lists. List c contains references to all the nodes that are in column c.
        self._nodes_by_column = [[] for _ in range(ncols)]

        # A list of lists. List r contains references to all the nodes that are in row r.
        self._nodes_by_row = [[] for _ in range(nrows)]

        # Go through and create a single node for each cell
        for y in range(0, nrows):
            for x in range(0, ncols):
                node = MazeCell(x, y, self)
                self._nodes.append(node)

                self._nodes_by_row[y].append(node)
                self._nodes_by_column[x].append(node)
        assert len(self._nodes) == nrows * ncols, f"There should be {nrows * ncols}, but there are {len(self._nodes)}"

        def _get_node(x: int, y: int):
            for n in self._nodes_by_column[x]:
                if n.y == y:
                    return n
            assert False, f"Could not find node at ({x}, {y})"

        # Go through again and fill in the nodes' relationships
        for node in self._nodes:
            if node.x != 0:
                node.left = _get_node(node.x - 1, node.y)

            if node.x != ncols - 1:
                node.right = _get_node(node.x + 1, node.y)

            if node.y != 0:
                node.up = _get_node(node.x, node.y - 1)

            if node.y != nrows - 1:
                node.down = _get_node(node.x, node.y + 1)

    def node_is_edge(self, node: MazeCell) -> bool:
        """
        Returns whether a node is on the edge.
        """
        return node.x == 0 or node.x == self._ncols - 1 or node.y == 0 or node.y == self._nrows - 1

    def get_node(self, x: int, y: int) -> MazeCell:
        """
        Get the node from the given location. This is O(n), where n is the number of columns.
        """
        node = self._nodes_by_row[y][x]
        assert node.x == x and node.y == y, f"(node.x, node.y) == ({node.x}, {node.y}), but should be ({x}, {y})"

        return node

    def get_player_node(self) -> MazeCell:
        """
        Get the node that contains the player.
        """
        return self._player_node

    def get_start_node(self) -> MazeCell:
        """
        Get the start node.
        """
        return self._start_node

    def get_end_node(self) -> MazeCell:
        """
        Get the end node.
        """
        return self._end_node

    def get_node_up(self, n: MazeCell) -> MazeCell:
        """
        Returns the node that is above `n`, if there is one, otherwise None.
        """
        if n.y == 0:
            return None
        else:
            return self.get_node(n.x, n.y - 1)

    def get_node_down(self, n: MazeCell) -> MazeCell:
        """
        Returns the node that is below `n`, if there is one, otherwise None.
        """
        if n.y == self._nrows - 1:
            return None
        else:
            return self.get_node(n.x, n.y + 1)

    def get_node_left(self, n: MazeCell) -> MazeCell:
        """
        Returns the node to the left of `n`, if there is one, otherwise None.
        """
        if n.x == 0:
            return None
        else:
            return self.get_node(n.x - 1, n.y)

    def get_node_right(self, n: MazeCell) -> MazeCell:
        """
        Returns the node to the right of `n`, if there is one, otherwise None.
        """
        if n.x == self._ncols - 1:
            return None
        else:
            return self.get_node(n.x + 1, n.y)

    def get_all_path_nodes(self) -> [MazeCell]:
        """
        Returns a list of all path nodes.
        """
        return [node for node in self._nodes if not node.is_wall]
