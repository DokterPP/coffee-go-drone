class LeftHand_MazeSolver:
    def __init__(self, pos_x, pos_y, maze):
        self.start_x = pos_x
        self.start_y = pos_y
        self.maze = maze
        self.dx = [0, 1, 0, -1]  
        self.dy = [-1, 0, 1, 0]  
        self.direction = 0  
        self.path_stack = [(pos_x, pos_y)] 
        self.numbered_path_nodes = [] 

    def turn_left(self, direction):
        return (direction - 1) % 4

    def turn_right(self, direction):
        return (direction + 1) % 4

    def is_path(self, x, y, direction):
        nx, ny = x + self.dx[direction], y + self.dy[direction]
        if 0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0]):
            return self.maze[ny][nx] in ['.', 'e', 's']
        return False

    def solve(self):
        x, y = self.start_x, self.start_y

        while self.path_stack:
            x, y = self.path_stack[-1]  # Get the current position from the top of the stack

            if self.maze[y][x] == 'e':  # Check if the end has been reached
                self.numbered_path_nodes.append((x, y))
                break

            moved = False
            self.direction = self.turn_left(self.direction)  # Always try to turn left first
            for _ in range(4):  # Try all directions in priority order
                if self.is_path(x, y, self.direction):
                    self.maze[y][x] = '-'  # Mark the current path
                    self.numbered_path_nodes.append((x, y))
                    x += self.dx[self.direction]
                    y += self.dy[self.direction]
                    self.path_stack.append((x, y))  # Push the new position onto the stack
                    moved = True
                    break
                else:
                    self.direction = self.turn_right(self.direction)  # Turn right if the current direction is blocked

            if not moved:  # If stuck at a dead-end, backtrack
                self.maze[y][x] = ','  # Optional: Mark backtracked path differently
                self.path_stack.pop()  # Pop the current position off the stack
                if self.numbered_path_nodes:
                    self.numbered_path_nodes.pop()
                if self.path_stack:  # Ensure the stack is not empty before resetting direction
                    x, y = self.path_stack[-1]  # Reset to the previous position
                    self.direction = self.turn_right(self.turn_right(self.direction))  # Reset to the direction before last turn

        # Mark the start position with 's'
        self.maze[self.start_y][self.start_x] = 's'

        return self.maze, self.numbered_path_nodes

    def print_final_maze(self):
        print("Final maze:")
        for row in self.maze:
            print(''.join(row))

    def get_solution(self):
        return self.maze, self.numbered_path_nodes
