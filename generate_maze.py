import random

def generate_maze(width, height):
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
            
    maze[height - 2][1] = 'S'  # Start
    maze[1][width - 2] = 'E'  # End
    
    return maze

def print_maze(maze):
    for row in maze:
        # if the cell is 0, print 'X', if it is 1, print '.', otherwise print the character
        print()

def write_maze_to_file(maze, filename):
    with open(filename, 'w') as file:
        for row in maze:
            file.write(''.join(['X' if cell == 0 else '.' for cell in row]) + '\n')

# Generate and print a maze
width = random.randint(10, 50)
height = random.randint(10, 40)

maze = generate_maze(width, height)
print_maze(maze)

# Write the maze to a text file
write_maze_to_file(maze, 'maze.txt')