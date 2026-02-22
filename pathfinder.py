from Point import Point
from collections import deque
from colorama import Fore, Style
import random


def bfs_path(maze: list[list[int]], en: Point, ex: Point) -> list:
    row = en.row
    col = en.column

    queue: deque = deque()
    queue.append((row, col))
    parent = {
        (row, col): (None, None)
    }
    visited = set([(row, col)])
    while queue:
        row, col = queue.popleft()
        below = (row + 1, col)
        above = (row - 1, col)
        east = (row, col + 1)
        west = (row, col - 1)
        if not maze[row][col] - 1 & 1 and above not in visited:
            queue.append(above)
            visited.add(above)
            parent[above] = (row, col)
        if not maze[row][col] - 1 & 2 and east not in visited:
            queue.append(east)
            visited.add(east)
            parent[east] = (row, col)
        if not maze[row][col] - 1 & 4 and below not in visited:
            queue.append(below)
            visited.add(below)
            parent[below] = (row, col)
        if not maze[row][col] - 1 & 8 and west not in visited:
            queue.append(west)
            visited.add(west)
            parent[west] = (row, col)
        if row == ex.row and col == ex.column:
            return extract_path(parent, en, ex)
    return []


def extract_path(parent_dict: dict, en: Point, ex: Point) -> list:
    cur = (ex.row, ex.column)
    path = []
    while cur != (en.row, en.column):
        path.append(parent_dict[cur])
        cur = parent_dict[cur]
    path.reverse()
    path.append((ex.row, ex.column))
    return path


def path_to_directions(path_coordinates: list[tuple]) -> list:
    i = 0
    j = i + 1
    path_directions = []
    while j < len(path_coordinates):
        y0, x0 = path_coordinates[i]
        y1, x1 = path_coordinates[j]
        i += 1
        j += 1
        if x1 > x0:
            path_directions.append('E')
        elif x1 < x0:
            path_directions.append('W')
        elif y1 > y0:
            path_directions.append('S')
        elif y0 > y1:
            path_directions.append('N')
    return path_directions


def show_path(
            maze: list[list], height: int, width: int, en: Point,
            ex: Point, path: list, colors: list | None
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
    path = bfs_path(maze, en, ex)

    for i in range(height):
        for j in range(width):
            if (maze[i][j] - 1 & 15) == 15:
                print(c3 + '█'*3, end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
            elif maze[i][j] - 1 & 1:
                print(c1 + '█'*3, end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
            elif (i, j) in path and (i - 1, j) in path:
                print(c1 + '█', end='', flush=True)
                print(c5 + '█', end='', flush=True)
                print(c1 + '█', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
            else:
                print(c1 + '█ █', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
        print()
        for j in range(width):
            if maze[i][j] - 1 & 15 == 15:
                print(c3 + '█'*3, end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
                continue
            if i == en.row and j == en.column:
                if maze[i][j] - 1 & 8:
                    print(c1 + '█', end='', flush=True)
                    print(Style.RESET_ALL, end='', flush=True)
                elif (i, j - 1) in path:
                    print(c5 + '█', end='', flush=True)
                else:
                    print(' ', end='', flush=True)
                print(c2 + '█', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
                if maze[i][j] - 1 & 2:
                    print(c1 + '█', end='', flush=True)
                    print(Style.RESET_ALL, end='', flush=True)
                elif (i, j + 1) in path:
                    print(c5 + '█', end='', flush=True)
                else:
                    print(' ', end='', flush=True)
                continue

            if i == ex.row and j == ex.column:
                if maze[i][j] - 1 & 8:
                    print(c1 + '█', end='', flush=True)
                    print(Style.RESET_ALL, end='', flush=True)
                elif (i, j - 1) in path:
                    print(c5 + '█', end='', flush=True)
                else:
                    print(' ', end='', flush=True)
                print(c4 + '█', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
                if maze[i][j] - 1 & 2:
                    print(c1 + '█', end='', flush=True)
                    print(Style.RESET_ALL, end='', flush=True)
                elif (i, j + 1) in path:
                    print(c5 + '█', end='', flush=True)
                else:
                    print(' ', end='', flush=True)
                continue

            elif maze[i][j] - 1 & 8:
                print(c1 + '█', end='', flush=True)
                if (i, j) in path:
                    print(c5 + '█', end='', flush=True)
                else:
                    print(' ', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
            else:
                if (i, j) in path and (i, j - 1) in path:
                    print(c5 + '██', end='', flush=True)
                elif (i, j) in path:
                    print(c5 + ' █', end='', flush=True)
                else:
                    print('  ', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)

            if maze[i][j] - 1 & 2:
                print(c1 + '█', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
            else:
                if (i, j) in path and (i, j + 1) in path:
                    print(c5 + '█', end='', flush=True)
                else:
                    print(' ', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
        print()
        for j in range(width):
            if maze[i][j] - 1 & 15 == 15:
                print(c3 + '█'*3, end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
            elif maze[i][j] - 1 & 4:
                print(c1 + '█'*3, end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
            elif (i, j) in path:
                if (i + 1, j) in path:
                    print(c1 + '█', end='', flush=True)
                    print(c5 + '█', end='', flush=True)
                    print(c1 + '█', end='', flush=True)
                    print(Style.RESET_ALL, end='', flush=True)
                else:
                    print(c1 + '█ █', end='', flush=True)
            else:
                print(c1 + '█ █', end='', flush=True)
                print(Style.RESET_ALL, end='', flush=True)
        print()
    return [c1, c2, c3, c4, c5]
