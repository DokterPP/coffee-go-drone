import random
class Maze_Generator:
    def __init__(self):
        pass
    
    def generate_maze(self, width, height):
        # Initialize the maze grid, 0 for wall, 1 for path
        maze = [[0 for x in range(width)] for y in range(height)]

        # Directions to move: up, right, down, left
        dx = [0, 1, 0, -1]
        dy = [-1, 0, 1, 0]

        # Stack for backtracking
        stack = []

        # Start with a random cell
        cx, cy = random.randint(1, width-2), random.randint(1, height-2)  # Adjust starting point
        maze[cy][cx] = 1
        stack.append((cx, cy))

        while stack:
            cx, cy = stack[-1]
            # Find unvisited neighbors
            neighbors = []
            for i in range(4):
                nx, ny = cx + dx[i], cy + dy[i]
                if 1 <= nx < width-1 and 1 <= ny < height-1 and maze[ny][nx] == 0:  # Adjust condition
                    # Count the number of visited neighbors
                    count = 0
                    for j in range(4):
                        ex, ey = nx + dx[j], ny + dy[j]
                        if 0 <= ex < width and 0 <= ey < height and maze[ey][ex] == 1:
                            count += 1
                    if count == 1:  # Add neighbor if it has one visited neighbor
                        neighbors.append(i)

            if neighbors:
                # Choose a random direction
                direction = random.choice(neighbors)
                # Move to the new cell
                nx, ny = cx + dx[direction], cy + dy[direction]
                maze[ny][nx] = 1
                stack.append((nx, ny))
            else:
                stack.pop()

        maze[height - 2][1] = 's'  # Start
        maze[1][width - 2] = 'e'  # End

        return maze

    def print_maze(self,maze):
        for row in maze:
            # if the cell is 0, print 'X', if it is 1, print '.', otherwise print the character
            print(''.join(['X' if cell == 0 else '.' if cell == 1 else cell for cell in row]))

    def write_maze_to_file(self, maze, filename):
        with open(filename, 'w') as file:
            for row in maze:
                file.write(''.join(['X' if cell == 0 else '.' if cell == 1 else cell for cell in row])+ '\n')

    def remove_random_walls(self, maze):
        
        height = len(maze)
        width = len(maze[0])
        removable_walls = []

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                # Ensure the cell value is an integer before comparison
                cell_value = int(maze[y][x]) if str(maze[y][x]).isdigit() else 0 if maze[y][x] == 'X' else 1
                if cell_value == 0:  # It's a wall
                    # Convert adjacent cells to integers, handling both 'X'/'.' and 0/1 representations
                    up_cell = int(maze[y-1][x]) if str(maze[y-1][x]).isdigit() else 0 if maze[y-1][x] == 'X' else 1
                    down_cell = int(maze[y+1][x]) if str(maze[y+1][x]).isdigit() else 0 if maze[y+1][x] == 'X' else 1
                    left_cell = int(maze[y][x-1]) if str(maze[y][x-1]).isdigit() else 0 if maze[y][x-1] == 'X' else 1
                    right_cell = int(maze[y][x+1]) if str(maze[y][x+1]).isdigit() else 0 if maze[y][x+1] == 'X' else 1
        
                    # Check if removing the wall does not create a direct path between two corridors
                    if (up_cell + down_cell == 2) or (left_cell + right_cell == 2):
                        removable_walls.append((x, y))

        walls_to_remove = random.sample(removable_walls, min(10, len(removable_walls)))

        for x, y in walls_to_remove:
            maze[y][x] = 1  # Remove the wall

        return maze
    # After gene
    
    # rating the maze and before returning it, call remove_random_walls
    def generate_maze_final(self):
        width = random.randint(10, 50)
        height = random.randint(10, 30)
        maze = self.generate_maze(width, height)
        output = self.remove_random_walls(maze)
        return output
