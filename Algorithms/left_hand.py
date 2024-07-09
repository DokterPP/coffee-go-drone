from generate_maze import Maze_Generator
def solve_maze(maze):
    print(type(maze))
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    direction = 0  # Start direction facing up
    
    x, y = 1, len(maze) - 2  # Assuming the start position is bottom left, just for demonstration
    start_position = (x, y)
    
    path_stack = [(x, y)]  # Initialize stack with the start position
    
    def turn_left(direction):
        return (direction - 1) % 4
    
    def turn_right(direction):
        return (direction + 1) % 4
    
    def is_path(x, y, direction):
        nx, ny = x + dx[direction], y + dy[direction]
        if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]):
            return maze[ny][nx] in ['.', 'e']
        return False
    
    while path_stack:
        x, y = path_stack[-1]  # Get the current position from the top of the stack
        
        if maze[y][x] == 'e':  # Check if the end has been reached
            break
        
        moved = False
        for _ in range(4):  # Try all directions
            if is_path(x, y, direction):
                maze[y][x] = '-'  # Mark the current path
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
            if path_stack:  # Ensure the stack is not empty before resetting direction
                x, y = path_stack[-1]  # Reset to the previous position
                # Reset direction based on backtrack position, or keep it unchanged
                # This step depends on how you want to handle direction after backtracking
                
        # After completing the pathfinding, mark the start position with 's'
    sx, sy = start_position
    maze[sy][sx] = 's'
    
    print("Final maze:")  # Debug print before final maze print
    for row in maze:
        print(''.join(row))
    
    return maze

