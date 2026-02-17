import random
import sys
from Point import Point




def collect_maze_info(filename: str):
    with open(filename, 'r') as f:
        content = f.read()
        content_dict = {}

        for line in content.split('\n'):
            if line.startswith('#'):
                continue
            line = line.split('=')
            try:
                content_dict[line[0]] = line[1]
                if line[1] == '':
                    print("Can't have keys with empty values in config file")
                    sys.exit(1)
            except IndexError:
                pass
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

    try:
        seed = int(content_dict['SEED'])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    try:
        width = int(content_dict['WIDTH'])
    except ValueError:
        print("Error: width must be an integer")
        sys.exit(1)
    try:
        height = int(content_dict['HEIGHT'])
    except ValueError:
        print("Error: Height must be an integer")
        sys.exit(1)

    perfect = False if content_dict['PERFECT'].lower() == 'false' else True
    entrance = content_dict['ENTRY'].split(',')
    try:
        entry = Point(int(entrance[0]), int(entrance[1]))
        if entry.row >= height or entry.column >= width:
            raise ValueError("entrance must be inside the maze")
    except ValueError as e:
        print(f"Error: {e}")
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

    file = content_dict['OUTPUT_FILE']
    if not file.endswith('.txt'):
        print("Error: Output file is not a txt file")
        sys.exit(0)
    return height, width, perfect, entry, portal, file, seed


def reserved(open_cell: Point, reserved_cells: list[Point]):
    for cell in reserved_cells:
        if cell.row == open_cell.row and cell.column == open_cell.column:
            return True
    return False


def prim_algorithm(
        height: int, width: int, seed: int, file: str, en: Point, ex: Point
    ) -> None:
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

    cells_in_maze = []

    def in_maze(row, col):
        return (row, col) in cells_in_maze_set

    def to_hex(index: int) -> str:
        return "0123456789ABCDEF"[index]

    def get_range():
        if height > 8 and width > 8:
                return ((height - 7) // 2 + 1), ((width - 5) // 2 - 1)
        return (-1, -1)

    ft_row, ft_column = get_range()
    if ft_column > 0 and ft_row > 0:
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
    cells_in_maze_set = set()
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
    output_file.write(f'\n{ex.row},{ex.column}')
    output_file.close()


def main():
    if len(sys.argv) != 2:
        print("Error: no configuration file")
        sys.exit(1)
    height, width, perfect, entry, portal, file, seed = collect_maze_info(
        sys.argv[1]
    )
    prim_algorithm(height, width, seed, file, entry, portal)


main()
from PIL import Image, ImageDraw

# Your maze as a list of strings
maze_hex = [
    "93B9555517",
    "AC40555783",
    "AF907FFFEA",
    "AFEC157FD2",
    "AFFFAFFF96",
    "813FAFD503",
    "AAEFAFFFEE",
    "AED541517B",
    "87D1103852",
    "C57EEEEC7E"
]

cell_size = 40
wall_width = 6
rows = len(maze_hex)
cols = len(maze_hex[0])

img_width = cols * cell_size + wall_width
img_height = rows * cell_size + wall_width
img = Image.new("RGB", (img_width, img_height), "white")
draw = ImageDraw.Draw(img)

def hex_to_int(h):
    return int(h, 16)

for y, row in enumerate(maze_hex):
    for x, hex_digit in enumerate(row):
        cell = hex_to_int(hex_digit)
        x0 = x*cell_size
        y0 = y*cell_size
        x1 = x0 + cell_size
        y1 = y0 + cell_size

        draw.rectangle([x0, y0, x1, y1], fill="#F0F0F0")

        if cell & 1:
            draw.line([(x0, y0), (x1, y0)], fill="black", width=wall_width)
        if cell & 2:
            draw.line([(x1, y0), (x1, y1)], fill="black", width=wall_width)
        if cell & 4:
            draw.line([(x0, y1), (x1, y1)], fill="black", width=wall_width)
        if cell & 8:
            draw.line([(x0, y0), (x0, y1)], fill="black", width=wall_width)

draw.rectangle([0, 0, cols*cell_size, rows*cell_size], outline="black", width=wall_width)

img.save("maze.png")
