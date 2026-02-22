from a_maze_ing import prim_algorithm
from pathfinder import show_path
import os
import sys
from a_maze_ing import display, collect_maze_info


class MazeGenerator():
    def __init__(self) -> None:
        self.mazes: dict = {}

    def render(self, seed: int) -> int:
        flag = False
        height, width, perfect, en, ex, file = collect_maze_info(
                    sys.argv[1]
                )
        maze, path, colors = prim_algorithm(
            height, width, seed, file, en, ex, perfect
        )
        while True:
            print('=== A-Maze-ing ===')
            print('1- Re-generate a new maze')
            print('2- Show/Hide path from entry to exit')
            print('3- Rotate maze colors')
            print('4- Quit')
            print()
            try:
                choice = int(input('Choice? (1-4): '))
            except Exception:
                print('Error invalid choice')
                sys.exit(1)
            if choice == 1:
                os.system('clear')
                0
                maze, path, colors = prim_algorithm(
                    height, width, seed, file, en, ex, perfect
                )
                flag = False
            if choice == 2:
                flag = not flag
                os.system('clear')
                if flag:
                    colors = show_path(
                        maze, height, width, en, ex, path, colors
                    )
                else:
                    display(maze, en, ex, colors, False)
            if choice == 3:
                if flag:
                    os.system('clear')
                    colors = show_path(
                        maze, height, width, en, ex, path, None
                    )
                else:
                    os.system('clear')
                    colors = display(maze, en, ex, [], False)
            if choice == 4:
                return 0


mazegen = MazeGenerator()
mazegen.render(5)
