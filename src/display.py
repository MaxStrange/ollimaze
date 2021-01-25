"""
Simplified functions for using the PyGame display API.
"""
import pygame
import src.mazegraph as mazegraph  # pylint: disable=import-error
import src.settings as setts       # pylint: disable=import-error

CELL_HEIGHT_PIXELS = 10
CELL_WIDTH_PIXELS = 10
BACKGROUND_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)


def make_screen(settings: setts.Settings):
    """
    Create the PyGame display for the game.
    """
    screen = pygame.display.set_mode([settings.nrows * CELL_HEIGHT_PIXELS, settings.ncols * CELL_WIDTH_PIXELS])
    return screen

def draw_maze(screen, maze: mazegraph.MazeGraph, settings: setts.Settings):
    """
    Draws the whole maze.
    """
    screen.fill(BACKGROUND_COLOR)

    for row in maze._nodes_by_row:
        # Draw this row
        for node in row:
            if node.is_wall:
                surface = pygame.Surface((CELL_WIDTH_PIXELS, CELL_HEIGHT_PIXELS))
                surface.fill(WALL_COLOR)
                screen.blit(surface, (CELL_WIDTH_PIXELS * node.x, CELL_HEIGHT_PIXELS * node.y))
            elif node.has_player:
                center_x = (CELL_WIDTH_PIXELS * node.x) + int(0.5 * CELL_WIDTH_PIXELS)
                center_y = (CELL_HEIGHT_PIXELS * node.y) + int(0.5 * CELL_HEIGHT_PIXELS)
                pygame.draw.circle(screen, settings.player_color, (center_x, center_y), min(int(CELL_WIDTH_PIXELS * 0.9), int(CELL_HEIGHT_PIXELS * 0.9)))
