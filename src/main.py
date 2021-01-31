"""
Super simple maze game for my son Oliver (and Alex too, if she ends up liking mazes).
"""
import argparse
import pygame
import src.maze as maze       # pylint: disable=import-error
import src.settings as setts  # pylint: disable=import-error


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nrows", "-r", type=int, default=50, help="Number of rows in the maze.")
    parser.add_argument("--ncols", "-c", type=int, default=50, help="Number of columns in the maze.")
    parser.add_argument("--n-random-walks", "-w", type=int, default=10, help="Number of random walks to create paths in the mazes.")
    parser.add_argument("--player-color", type=int, nargs=3, default=(0, 0, 255), help="R, G, and B values for the player rectangle.")
    args = parser.parse_args()

    # Make the settings out of the command line arguments
    settings = setts.Settings(args.nrows, args.ncols, args.player_color, args.n_random_walks)

    # Initialize PyGame
    pygame.init()  # pylint: disable=no-member

    # Main looop: Create a maze and play it. If we are done, we'll break, otherwise, we'll make another maze.
    done = False
    while not done:
        the_maze = maze.Maze(settings)
        done = the_maze.play()

    # Quit
    pygame.quit()  # pylint: disable=no-member
