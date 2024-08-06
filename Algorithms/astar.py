import heapq

class AStar_MazeSolver:
    def __init__(self, pos_x, pos_y, maze):
        self.maze = maze
        self.start_x = pos_x
        self.start_y = pos_y
        self.start = (self.start_x, self.start_y)
        self.goal = self.find_goal_position()
        self.dx = [0, 1, 0, -1]
        self.dy = [-1, 0, 1, 0]
        self.numbered_path_nodes = []
        self.open_set = []
        self.came_from = {}
        self.cost_so_far = {self.start: 0}

    def find_goal_position(self):
        """Find the goal position marked with 'e'."""
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 'e':
                    return (x, y)
        return None

    def heuristic(self, a, b):
        """Calculate the heuristic value using Manhattan distance."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve_maze_astar(self):
        """Solve the maze using A* Search Algorithm."""
        heapq.heappush(self.open_set, (0 + self.heuristic(self.start, self.goal), 0, self.start))

        while self.open_set:
            _, current_cost, current = heapq.heappop(self.open_set)

            if current == self.goal:
                break

            x, y = current
            for direction in range(4):
                nx, ny = x + self.dx[direction], y + self.dy[direction]
                if 0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0]) and self.maze[ny][nx] in ['.', 'e']:
                    new_cost = self.cost_so_far[current] + 1
                    next_node = (nx, ny)
                    if next_node not in self.cost_so_far or new_cost < self.cost_so_far[next_node]:
                        self.cost_so_far[next_node] = new_cost
                        priority = new_cost + self.heuristic(self.goal, next_node)
                        heapq.heappush(self.open_set, (priority, new_cost, next_node))
                        self.came_from[next_node] = current

        self.reconstruct_path()

        return self.maze, self.numbered_path_nodes

    def reconstruct_path(self):
        """Reconstruct the path from start to goal."""
        if self.goal in self.came_from:
            current = self.goal
            path_stack = []
            while current != self.start:
                path_stack.append(current)
                current = self.came_from[current]
            path_stack.append(self.start)

            while path_stack:
                px, py = path_stack.pop()
                self.numbered_path_nodes.append((px, py))
                if self.maze[py][px] != 'e':  # Keep the end marked as 'e'
                    self.maze[py][px] = '-'

            # Mark the start and goal
            sx, sy = self.start
            ex, ey = self.goal
            self.maze[sy][sx] = 's'
            self.maze[ey][ex] = 'e'

    def print_maze(self):
        """Print the current state of the maze."""
        print("Final maze:")
        for row in self.maze:
            print(''.join(row))

    def get_path(self):
        """Return the path found by the solver."""
        return self.numbered_path_nodes