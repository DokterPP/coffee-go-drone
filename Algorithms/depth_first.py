def solve_maze_dfs(maze):
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    
    x, y = 1, len(maze) - 2  # Assuming the start position is bottom left
    start_position = (x, y)
    
    stack = [(x, y)]
    visited = set(stack)
    numbered_path_nodes = []
    while stack:
        x, y = stack[-1]
        
        if maze[y][x] == 'e':  # Check if the end has been reached
            numbered_path_nodes.append((x, y))
            break
        
        moved = False
        for direction in range(4):
            nx, ny = x + dx[direction], y + dy[direction]
            if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] in ['.', 'e'] and (nx, ny) not in visited:
                stack.append((nx, ny))
                visited.add((nx, ny))
                maze[y][x] = '-'  # Mark the current path
                numbered_path_nodes.append((x, y))
                moved = True
                break
        
        if not moved:  # If stuck at a dead-end, backtrack
            maze[y][x] = ','  # Optional: Mark backtracked path differently
            stack.pop()
            numbered_path_nodes.pop()
    
    # Mark the start position with 's'
    sx, sy = start_position
    maze[sy][sx] = 's'
    
    print("Final maze:")  # Debug print before final maze print
    for row in maze:
        print(''.join(row))
    
    return maze, numbered_path_nodes
