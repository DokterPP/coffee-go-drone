def solve_maze(pos_x, pos_y , maze):
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    direction = 0  # Start direction facing up
    x, y = pos_x, pos_y  # Start position
    
    start_x, start_y = None, None
    for my, row in enumerate(maze):
        for mx, cell in enumerate(row):
            if cell == 's':
                start_x, start_y = mx, my
                break
        if start_x is not None:
            break
        
    start_position = (x, y)
    # x, y = 1, len(maze) - 2  # Assuming the start position is bottom left, just for demonstration

    print(f"Start position: {start_position}")
    
    path_stack = [(x, y)]  # Initialize stack with the start position
    
    # List to store numbered path nodes and their coordinates
    numbered_path_nodes = []
    
    def turn_left(direction):
        return (direction - 1) % 4
    
    def turn_right(direction):
        return (direction + 1) % 4
    
    def is_path(x, y, direction):
        nx, ny = x + dx[direction], y + dy[direction]
        if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]):
            return maze[ny][nx] in ['.', 'e', 's']
        return False
    
    while path_stack:
        x, y = path_stack[-1]  # Get the current position from the top of the stack
        
        if maze[y][x] == 'e':  # Check if the end has been reached
            numbered_path_nodes.append((x, y))
            break
        
        moved = False
        direction = turn_left(direction)  # Always try to turn left first
        for _ in range(4):  # Try all directions in priority order
            if is_path(x, y, direction):
                maze[y][x] = '-'  # Mark the current path
                numbered_path_nodes.append((x, y))
                x += dx[direction]
                y += dy[direction]
                path_stack.append((x, y))  # Push the new position onto the stack
                moved = True
                break
            else:
                direction = turn_right(direction)  # Turn right if the current direction is blocked
        
        if not moved:  # If stuck at a dead-end, backtrack
            maze[y][x] = ','  # Optional: Mark backtracked path differently
            path_stack.pop()  # Pop the current position off the stack
            numbered_path_nodes.pop()
            if path_stack:  # Ensure the stack is not empty before resetting direction
                x, y = path_stack[-1]  # Reset to the previous position
                direction = turn_right(turn_right(direction))  # Reset to the direction before last turn
                

    # Mark the start position with 's'
    maze[start_y][start_x] = 's'
    
    print("Final maze:")  # Debug print before final maze print
    for row in maze:
        print(''.join(row))
    
    return maze, numbered_path_nodes
