class Deque:
    def __init__(self):
        self.items = []
    
    def append(self, item):
        self.items.append(item)
    
    def popleft(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("pop from an empty deque")
    
    def is_empty(self):
        return len(self.items) == 0
    
    def __len__(self):
        return len(self.items)

def solve_maze_bfs(pos_x, pos_y, maze):
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    numbered_path_nodes = []
    
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
    
    queue = Deque()
    queue.append((x, y))
    visited = set([(x, y)])
    parent = {}  # To keep track of the path
    
    end_found = False
    while len(queue) > 0:
        x, y = queue.popleft()
        if maze[y][x] == 'e':  # Check if the end has been reached
            end_found = True
            end_position = (x, y)
            break
        if maze[y][x] == '.':  # Only mark paths, not start or end
            maze[y][x] = ','  # Mark visited
        for direction in range(4):
            nx, ny = x + dx[direction], y + dy[direction]
            if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] in ['.', 'e'] and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
    
    if end_found:
        # Trace back from the end position to the start position
        x, y = end_position
        path_stack = []
        while (x, y) != start_position:
            path_stack.append((x, y))
            x, y = parent[(x, y)]
        path_stack.append(start_position)
        
        # Reverse the path stack to get the path from start to end
        while path_stack:
            px, py = path_stack.pop()
            numbered_path_nodes.append((px, py))
            if maze[py][px] != 'e':  # Keep the end marked as 'e'
                maze[py][px] = '-'  # Mark the shortest path
        
        # Mark the start position last to keep it as 's'
        maze[start_y][start_x] = 's'
    
    print("Final maze:")  # Debug print before final maze print
    for row in maze:
        print(''.join(row))
    
    return maze, numbered_path_nodes
