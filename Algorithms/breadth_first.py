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

class BreadthFirst_MazeSolver:
    def __init__(self, pos_x, pos_y, maze):
        self.maze = maze
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.queue = Deque()  # Use the custom Deque class
        self.queue.append((self.pos_x, self.pos_y))
        self.visited = set([(self.pos_x, self.pos_y)])
        self.numbered_path_nodes = []
        self.parent = {}  # To keep track of the path
        self.dx = [0, 1, 0, -1]
        self.dy = [-1, 0, 1, 0]

    def solve_maze_bfs(self):
        """Solve the maze using Breadth-First Search (BFS)."""
        end_found = False
        end_position = None
        start_x, start_y = None, None
        for my, row in enumerate(self.maze):
            for mx, cell in enumerate(row):
                if cell == 's':
                    start_x, start_y = mx, my
                    break
            if start_x is not None:
                break
            
        while len(self.queue) > 0:
            x, y = self.queue.popleft()

            if self.maze[y][x] == 'e':  # Check if the end has been reached
                end_found = True
                end_position = (x, y)
                break

            if self.maze[y][x] == '.':  # Only mark paths, not start or end
                self.maze[y][x] = ','  # Mark visited

            for direction in range(4):
                nx, ny = x + self.dx[direction], y + self.dy[direction]
                if (0 <= ny < len(self.maze) and
                        0 <= nx < len(self.maze[0]) and
                        self.maze[ny][nx] in ['.', 'e'] and
                        (nx, ny) not in self.visited):
                    self.queue.append((nx, ny))
                    self.visited.add((nx, ny))
                    self.parent[(nx, ny)] = (x, y)

        if end_found:
            self.trace_path(end_position, start_x, start_y)

        return self.maze, self.numbered_path_nodes

    def trace_path(self, end_position, start_x, start_y):
        """Trace back from the end position to the start position to build the path."""
        x, y = end_position
        path_stack = []

        while (x, y) != (self.pos_x, self.pos_y):
            path_stack.append((x, y))
            x, y = self.parent[(x, y)]

        path_stack.append((self.pos_x, self.pos_y))

        while path_stack:
            px, py = path_stack.pop()
            self.numbered_path_nodes.append((px, py))
            if self.maze[py][px] != 'e':  # Keep the end marked as 'e'
                self.maze[py][px] = '-'  # Mark the shortest path

        # Mark the start position last to keep it as 's'
        self.maze[start_y][start_x] = 's'

    def print_maze(self):
        """Print the current state of the maze."""
        print("Final maze:")
        for row in self.maze:
            print(''.join(row))

    def get_path(self):
        """Return the path found by the solver."""
        return self.numbered_path_nodes
