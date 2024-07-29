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

def solve_maze_bfs(maze):
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    
    x, y = 1, len(maze) - 2  # Assuming the start position is bottom left
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
        x, y = end_position
        while (x, y) != start_position:
            if maze[y][x] != 'e':  # Keep the end marked as 'e'
                maze[y][x] = '-'  # Mark the shortest path
            x, y = parent[(x, y)]
        # Mark the start position last to keep it as 's'
        sx, sy = start_position
        maze[sy][sx] = 's'
    
    print("Final maze:")  # Debug print before final maze print
    for row in maze:
        print(''.join(row))
    
    return maze
