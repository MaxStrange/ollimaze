"""
Module to hold a MazeGraph class.

The MazeGraph class is the underlying data structure
for a Maze.
"""


class MazeCell:
    """
    A node in the graph, which corresponds to a cell, if you think of the maze as a matrix.
    """
    def __init__(self, x: int, y: int, wall=True):
        """
        Args
        ----
        - x: The x coordinate (leftmost column is zero).
        - y: The y coordinate (topmost column is zero).
        - wall: Are we a wall or an open space?

        """
        self.x = x
        self.y = y
        self.is_wall = wall
        self.up = None
        self.left = None
        self.right = None
        self.down = None


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
    def __init__(self, nrows: int, ncols: int):
        # A list of every node in the graph
        self._nodes = []

        # A list of lists. List c contains references to all the nodes that are in column c.
        self._nodes_by_column = [[] for _ in range(ncols)]

        # A list of lists. List r contains references to all the nodes that are in row r.
        self._nodes_by_row = [[] for _ in range(nrows)]

        # Go through and create a single node for each cell
        for y in range(0, nrows):
            for x in range(0, ncols):
                node = MazeCell(x, y)
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
