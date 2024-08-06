class DepthFirst_MazeSolver:
    def __init__(self, pos_x, pos_y, maze):
        self.maze = maze
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.stack = [(self.pos_x, self.pos_y)]
        self.visited = set(self.stack)
        self.numbered_path_nodes = []
        self.dx = [0, 1, 0, -1]
        self.dy = [-1, 0, 1, 0]

    def solve_maze_dfs(self):
        """Solve the maze using Depth First Search (DFS)."""
        start_x, start_y = None, None
        for my, row in enumerate(self.maze):
            for mx, cell in enumerate(row):
                if cell == 's':
                    start_x, start_y = mx, my
                    break
            if start_x is not None:
                break
            
        while self.stack:
            x, y = self.stack[-1]

            if self.maze[y][x] == 'e':  # Check if the end has been reached
                self.numbered_path_nodes.append((x, y))
                break

            moved = False
            for direction in range(4):
                nx, ny = x + self.dx[direction], y + self.dy[direction]
                if (0 <= ny < len(self.maze) and
                        0 <= nx < len(self.maze[0]) and
                        self.maze[ny][nx] in ['.', 'e', 's'] and
                        (nx, ny) not in self.visited):
                    self.stack.append((nx, ny))
                    self.visited.add((nx, ny))
                    self.maze[y][x] = '-'  # Mark the current path
                    self.numbered_path_nodes.append((x, y))
                    moved = True
                    break

            if not moved:  # If stuck at a dead-end, backtrack
                self.maze[y][x] = ','  # Optional: Mark backtracked path differently
                self.stack.pop()
                if self.numbered_path_nodes:
                    self.numbered_path_nodes.pop()

        # Mark the start position with 's'
        self.maze[start_y][start_x] = 's'
        
        return self.maze, self.numbered_path_nodes

    def print_maze(self):
        """Print the current state of the maze."""
        print("Final maze:")
        for row in self.maze:
            print(''.join(row))

    def get_path(self):
        """Return the path found by the solver."""
        return self.numbered_path_nodes