import random
import sys
import time
from colorama import Fore, Style
from Point import Point
from pathfinder import bfs_path, path_to_directions, show_path
import os


def print_first_row(c1: str, c3: str, line: list, delay: bool) -> None:
    for i in line:
        if ((i - 1) & 15) == 15:
            print(c3 + '█'*3, end='', flush=True)
            print(Style.RESET_ALL, end='', flush=True)
        elif i - 1 & 1:
            print(c1 + '█'*3, end='', flush=True)
            print(Style.RESET_ALL, end='', flush=True)
        else:
            print(c1 + '█ █', end='', flush=True)
            print(Style.RESET_ALL, end='', flush=True)
        if delay:
            time.sleep(0.015)


def print_second_row(
            c1: str, c2: str, c3: str, c4: str, line: list, row: int,
            en: Point,
            ex: Point,
            delay: bool
        ) -> None:

    col = 0
    for i in line:
        if (i - 1) & 15 == 15:
            print(c3 + '█'*3, end='', flush=True)
            print(Style.RESET_ALL, end='', flush=True)
            col += 1
            if delay:
                time.sleep(0.0075)
            continue
        if row == en.row and col == en.column:
            if i - 1 & 8:
                print(c1 + '█', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
            else:
                print(' ', end='', flush=True)
            print(c2 + '█', end='', flush=True)
            print(Style.RESET_ALL, end='', flush=True)
            if delay:
                time.sleep(0.0075)
            if i - 1 & 2:
                print(c1 + '█', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
            else:
                print(' ', end='', flush=True)
            col += 1
            if delay:
                time.sleep(0.0075)
            continue

        if row == ex.row and col == ex.column:
            if i - 1 & 8:
                print(c1 + '█', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
            else:
                print(' ', end='', flush=True)
            print(c4 + '█', end='', flush=True)
            print(Style.RESET_ALL, end='', flush=True)
            if i - 1 & 2:
                print(c1 + '█', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
            else:
                print(' ', end='', flush=True)
            col += 1
            if delay:
                time.sleep(0.0075)
            continue

        elif i - 1 & 8:
            print(c1 + '█ ', end='', flush=True)
            print(Style.RESET_ALL, end='', flush=True)
        else:
            print('  ', end='', flush=True)
        if delay:
            time.sleep(0.0075)

        if i - 1 & 2:
            print(c1 + '█', end='', flush=True)
            print(Style.RESET_ALL, end='', flush=True)
        else:
            print(' ', end='', flush=True)
        if delay:
            time.sleep(0.0075)
        col += 1


def print_third_row(c1: str, c3: str, line: list, delay: bool) -> None:
    for i in line:
        if (i - 1) & 15 == 15:
            print(c3 + '█'*3, end='', flush=True)
            print(Style.RESET_ALL, end='', flush=True)
        elif i - 1 & 4:
            print(c1 + '█'*3, end='', flush=True)
            print(Style.RESET_ALL, end='', flush=True)
        else:
            print(c1 + '█ █', end='', flush=True)
            print(Style.RESET_ALL, end='', flush=True)
        if delay:
            time.sleep(0.015)


def display(
        maze: list[list[int]], entry: Point, leave: Point, colors: list[str],
        delay: bool
        ) -> list:
    if not colors:
        colors = [
            Fore.RED,
            Fore.GREEN,
            Fore.MAGENTA,
            Fore.WHITE,
            Fore.CYAN,
            Fore.YELLOW
        ]
        c1 = random.choice(colors)
        colors.pop(colors.index(c1))
        c2 = random.choice(colors)
        colors.pop(colors.index(c2))
        c3 = random.choice(colors)
        colors.pop(colors.index(c3))
        c4 = random.choice(colors)
        colors.pop(colors.index(c4))
        c5 = random.choice(colors)
        colors.pop(colors.index(c5))
    else:
        c1 = colors[0]
        c2 = colors[1]
        c3 = colors[2]
        c4 = colors[3]
        c5 = colors[4]

    row = 0
    for line in maze:
        if delay:
            time.sleep(0.01)
        print_first_row(c1, c3, line, delay)
        print()
        print_second_row(c1, c2, c3, c4, line, row, entry, leave, delay)
        print()
        print_third_row(c1, c3, line, delay)
        if delay:
            time.sleep(0.015)
        print()
        row += 1
    return [c1, c2, c3, c4, c5]


def collect_maze_info(filename: str) -> tuple:
    perfect = None
    with open(filename, 'r') as f:
        content = f.read()
        content_dict = {}
        if not content:
            print('Error: no configuration in file!')
            sys.exit(1)

        for line in content.split('\n'):
            if line.startswith('#'):
                continue
            lines = line.split('=')
            try:
                content_dict[lines[0]] = lines[1]
                if lines[1] == '':
                    print("Can't have keys with empty values in config file")
                    sys.exit(1)
            except IndexError:
                pass
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

    try:
        seed = int(content_dict['SEED'])
    except KeyError as e:
        print(f"Error: missing {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    try:
        width = int(content_dict['WIDTH'])
    except ValueError:
        print("Error: width must be an integer")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: missing {e}")
        sys.exit(1)
    try:
        height = int(content_dict['HEIGHT'])
    except ValueError:
        print("Error: Height must be an integer")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: missing {e}")
        sys.exit(1)
    try:
        if content_dict['PERFECT'].lower() == 'false':
            perfect = False
        elif content_dict['PERFECT'].lower() == 'true':
            perfect = True
        else:
            print('Error: unknown maze type')
            sys.exit(1)
    except KeyError as e:
        print(f'Error: missing {e}')
        sys.exit(1)
    entrance = content_dict['ENTRY'].split(',')
    try:
        entry = Point(int(entrance[0]), int(entrance[1]))
        if entry.row >= height or entry.column >= width:
            raise ValueError("entrance must be inside the maze")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: missing {e}")
        sys.exit(1)

    leave = content_dict['EXIT'].split(',')
    try:
        portal = Point(int(leave[0]), int(leave[1]))
        if portal.row >= height or portal.column >= width:
            raise ValueError("exit must be inside the maze")
        if portal.row == entry.row and portal.column == entry.column:
            raise ValueError("exit and entry can't be the same")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: missing {e}")
        sys.exit(1)

    file = content_dict['OUTPUT_FILE']
    if not file.endswith('.txt'):
        print("Error: Output file is not a txt file")
        sys.exit(0)
    return height, width, perfect, entry, portal, file, seed


def reserved(open_cell: Point, reserved_cells: list[Point]) -> bool:
    for cell in reserved_cells:
        if cell.row == open_cell.row and cell.column == open_cell.column:
            return True
    return False


def prim_algorithm(
        height: int,
        width: int, seed: int, file: str, en: Point, ex: Point, perfect: bool
        ) -> tuple:
    random.seed(seed)
    maze = []
    i = 0
    while i < height:
        row = []
        j = 0
        while j < width:
            row.append(16)
            j += 1
        maze.append(row)
        i += 1

    cells_in_maze: list[Point] = []

    def in_maze(row: int, col: int) -> bool:
        return (row, col) in cells_in_maze_set

    def to_hex(index: int) -> str:
        return "0123456789ABCDEF"[index]

    def get_range() -> tuple:
        if height >= 9 and width >= 9:
            return ((height - 7) // 2 + 1), ((width - 5) // 2 - 1)
        print('Error: Maze too small to create 42 pattern')
        return (-1, -1)

    ft_row, ft_column = get_range()
    if ft_column >= 0 and ft_row >= 0:
        reserved_cells = [
            Point(ft_row, ft_column),
            Point(ft_row + 1, ft_column),
            Point(ft_row + 2, ft_column),
            Point(ft_row + 2, ft_column + 1),
            Point(ft_row + 2, ft_column + 2),
            Point(ft_row + 3, ft_column + 2),
            Point(ft_row + 4, ft_column + 2),
            Point(ft_row, ft_column + 4),
            Point(ft_row, ft_column + 5),
            Point(ft_row, ft_column + 6),
            Point(ft_row + 1, ft_column + 6),
            Point(ft_row + 2, ft_column + 6),
            Point(ft_row + 2, ft_column + 5),
            Point(ft_row + 2, ft_column + 4),
            Point(ft_row + 3, ft_column + 4),
            Point(ft_row + 4, ft_column + 4),
            Point(ft_row + 4, ft_column + 5),
            Point(ft_row + 4, ft_column + 6),
        ]
    else:
        reserved_cells = []
    if reserved(en, reserved_cells) or reserved(ex, reserved_cells):
        print("Error: entrance and exit can't be in the 42 drawing")
        sys.exit(1)
    cells_in_maze_set: set = set()
    while len(cells_in_maze_set) < (height * width) - len(reserved_cells):
        if len(cells_in_maze) == 0:
            while True:
                random_cell = Point(
                    random.randint(0, height - 1), random.randint(0, width - 1)
                )
                if not reserved(random_cell, reserved_cells):
                    break
            cells_in_maze.append(random_cell)
            cells_in_maze_set.add((random_cell.row, random_cell.column))
        else:
            index = random.randint(0, len(cells_in_maze) - 1)
            random_cell = cells_in_maze[index]

        random_cell.frontier = []

        if random_cell.column + 1 < width:
            if not in_maze(random_cell.row, random_cell.column + 1):
                random_cell.frontier.append(
                    Point(random_cell.row, random_cell.column + 1)
                )

        if random_cell.column - 1 >= 0:
            if not in_maze(random_cell.row, random_cell.column - 1):
                random_cell.frontier.append(
                    Point(random_cell.row, random_cell.column - 1)
                )

        if random_cell.row + 1 < height:
            if not in_maze(random_cell.row + 1, random_cell.column):
                random_cell.frontier.append(
                    Point(random_cell.row + 1, random_cell.column)
                )

        if random_cell.row - 1 >= 0:
            if not in_maze(random_cell.row - 1, random_cell.column):
                random_cell.frontier.append(
                    Point(random_cell.row - 1, random_cell.column)
                )

        if len(random_cell.frontier) == 0:
            continue

        open_index = random.randint(0, len(random_cell.frontier) - 1)
        open_cell = random_cell.frontier[open_index]

        if not in_maze(open_cell.row, open_cell.column):
            if not reserved(open_cell, reserved_cells):
                if open_cell.row < random_cell.row:
                    maze[random_cell.row][random_cell.column] -= 1
                    maze[open_cell.row][open_cell.column] -= 4
                if open_cell.row > random_cell.row:
                    maze[random_cell.row][random_cell.column] -= 4
                    maze[open_cell.row][open_cell.column] -= 1
                if open_cell.column > random_cell.column:
                    maze[random_cell.row][random_cell.column] -= 2
                    maze[open_cell.row][open_cell.column] -= 8
                if open_cell.column < random_cell.column:
                    maze[random_cell.row][random_cell.column] -= 8
                    maze[open_cell.row][open_cell.column] -= 2

                cells_in_maze.append(open_cell)
                cells_in_maze_set.add((open_cell.row, open_cell.column))

    i = 0
    if not perfect:
        cells = list(cells_in_maze_set)
        if len(cells) >= 3:
            if len(cells) <= 4:
                k = 1
            elif len(cells) > 4 and len(cells) < 10:
                k = 2
            else:
                k = random.randint(
                    len(cells) // 3, len(cells) - len(cells) // 2
                )

            while k:
                walls = [1, 2, 4, 8]
                r, c = random.choice(cells)
                if (r == 0 or reserved(
                    Point(r - 1, c), reserved_cells
                ) or not maze[r][c] - 1 & 1
                 or (r == en.row and c == en.column)
                 or (r == ex.row and c == ex.column)):
                    walls.pop(0)
                if (c == 0 or reserved(
                    Point(r, c - 1), reserved_cells
                ) or not maze[r][c] - 1 & 8
                 or (r == en.row and c == en.column)
                 or (r == ex.row and c == ex.column)):
                    walls.pop(walls.index(8))
                if (c == width - 1 or reserved(
                    Point(r, c + 1), reserved_cells
                ) or not maze[r][c] - 1 & 2
                 or (r == en.row and c == en.column)
                 or (r == ex.row and c == ex.column)):
                    walls.pop(walls.index(2))
                if (r == height - 1 or reserved(
                    Point(r + 1, c), reserved_cells
                ) or not maze[r][c] - 1 & 4
                 or (r == en.row and c == en.column)
                 or (r == ex.row and c == ex.column)):
                    walls.pop(walls.index(4))
                if len(walls) > 0:
                    choice = random.choice(walls)
                    maze[r][c] -= choice
                    if choice == 1:
                        maze[r - 1][c] -= 4
                    elif choice == 2:
                        maze[r][c + 1] -= 8
                    elif choice == 4:
                        maze[r + 1][c] -= 1
                    elif choice == 8:
                        maze[r][c - 1] -= 2
                    k -= 1

    colors = display(maze, en, ex, [], True)
    path = bfs_path(maze, en, ex)
    output_file = open(file, 'w+')
    while i < height:
        j = 0
        line = ""
        while j < width:
            v = maze[i][j] - 1
            line += to_hex(v)
            j += 1
        output_file.write(line + '\n')
        i += 1
    output_file.write(f'\n{en.row},{en.column}')
    output_file.write(f'\n{ex.row},{ex.column}\n')
    for j in path_to_directions(path):
        output_file.write(j)
    output_file.write('\n')

    output_file.close()
    return maze, path, colors


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[-1] != 'config.txt':
        if len(sys.argv) > 2:
            print("Error: ambiguous arguments!")
        else:
            print('Error: no configuration file')
        sys.exit(1)
    height, width, perfect, entry, ex, file, seed = collect_maze_info(
        sys.argv[1]
    )
    colors = None
    maze, path, colors = prim_algorithm(
        height, width, seed, file, entry, ex, perfect
    )
    flag = False
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
            height, width, perfect, entry, ex, file, seed = collect_maze_info(
                sys.argv[1]
            )
            maze, path, colors = prim_algorithm(
                height, width, seed, file, entry, ex, perfect
            )
            flag = False
        if choice == 2:
            flag = not flag
            os.system('clear')
            if flag:
                colors = show_path(
                    maze, height, width, entry, ex, path, colors
                )
            else:
                display(maze, entry, ex, colors, False)
        if choice == 3:
            if flag:
                os.system('clear')
                colors = show_path(
                    maze, height, width, entry, ex, path, None
                )
            else:
                os.system('clear')
                colors = display(maze, entry, ex, [], False)
        if choice == 4:
            return 0


main()
