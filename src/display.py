"""
Simplified functions for using the PyGame display API.
"""
import pygame
import src.mazegraph as mazegraph  # pylint: disable=import-error
import src.settings as setts       # pylint: disable=import-error

# This is the base height of a maze cell
BASE_CELL_HEIGHT = 10

# This is the base widht of a maze cell
BASE_CELL_WIDTH = 10

# This is the real height of each cell. It gets adjusted based on how many rows there are
CELL_HEIGHT_PIXELS = BASE_CELL_HEIGHT

 # This is the real width of each cell. It gets adjusted based on how many columns there are
CELL_WIDTH_PIXELS = BASE_CELL_WIDTH

FINISH_COLOR = (0, 255, 0)


def make_screen(settings: setts.Settings):
    """
    Create the PyGame display for the game.
    """
    CELL_HEIGHT_PIXELS = max(10, int(500 * (1 / settings.nrows)))
    CELL_WIDTH_PIXELS  = max(10, int(500 * (1 / settings.ncols)))

    screen = pygame.display.set_mode([settings.ncols * CELL_WIDTH_PIXELS, settings.nrows * CELL_HEIGHT_PIXELS])
    return screen

def draw_maze(screen, maze: mazegraph.MazeGraph, settings: setts.Settings):
    """
    Draws the whole maze.
    """
    CELL_HEIGHT_PIXELS = max(10, int(500 * (1 / settings.nrows)))
    CELL_WIDTH_PIXELS  = max(10, int(500 * (1 / settings.ncols)))

    screen.fill(settings.path_color)

    for row in maze._nodes_by_row:
        # Draw this row
        for node in row:
            if node.is_finish:
                surface = pygame.Surface((CELL_WIDTH_PIXELS, CELL_HEIGHT_PIXELS))
                surface.fill(settings.goal_color)
                screen.blit(surface, (CELL_WIDTH_PIXELS * node.x, CELL_HEIGHT_PIXELS * node.y))
            elif node.is_wall:
                surface = pygame.Surface((CELL_WIDTH_PIXELS, CELL_HEIGHT_PIXELS))
                surface.fill(settings.wall_color)
                screen.blit(surface, (CELL_WIDTH_PIXELS * node.x, CELL_HEIGHT_PIXELS * node.y))

            if node.has_player:
                center_x = (CELL_WIDTH_PIXELS * node.x) + int(0.5 * CELL_WIDTH_PIXELS)
                center_y = (CELL_HEIGHT_PIXELS * node.y) + int(0.5 * CELL_HEIGHT_PIXELS)
                pygame.draw.circle(screen, settings.player_color, (center_x, center_y), min(int(CELL_WIDTH_PIXELS * 0.5), int(CELL_HEIGHT_PIXELS * 0.5)))
