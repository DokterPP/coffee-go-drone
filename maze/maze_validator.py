# Check if both start and end points are present in the maze
# check if maze is solvable
# check if maze has walls on the edges
# check if maze has walls in the middle
# check if maze start and end points are on the corners

from Algorithms.astar import AStar_MazeSolver


class Validator:
    def __init__(self):
        pass
    
    def __check_file_empty(self, maze):
        if not maze:
            return False
        return True
    
    def __check_start_end_points(self, maze):
        start = False
        end = False
        for row in maze:
            for cell in row:
                if cell == 's':
                    start = True
                if cell == 'e':
                    end = True
        return start and end
    
    def __check_multiple_start_end_points(self, maze):
        start_count = 0
        end_count = 0
        for row in maze:
            for cell in row:
                if cell == 's':
                    start_count += 1
                if cell == 'e':
                    end_count += 1
        if start_count > 1 or end_count > 1:
            return False
        return True
        
    def __check_illegal_characters(self, maze):
        for row in maze:
            for cell in row:
                if cell not in ['s', 'e', 'X', '.']:
                    return False
        return True
    
    def __check_maze_solvable(self, maze):
        start_x, start_y = None, None
        for my, row in enumerate(maze):
            for mx, cell in enumerate(row):
                if cell == 's':
                    start_x, start_y = mx, my
                    break
            if start_x is not None:
                break
        
        astar = AStar_MazeSolver(start_x, start_y, maze)
        solved_maze, solved_path  = astar.solve_maze_astar()
        if solved_path:
            return True
        else:
            return False
        
    def __check_maze_edges(self, maze):
        # Ensure the maze is a rectangular grid with uniform rows and columns
        rows = len(maze)
        cols = len(maze[0])

        # Check if all rows have the same number of columns
        for row in maze:
            if len(row) != cols:
                return False

        # Check if the first and last rows are all walls ('X')
        if any(cell != 'X' for cell in maze[0]) or any(cell != 'X' for cell in maze[rows - 1]):
            return False

        # Check if the first and last columns in all rows are walls ('X')
        for row in maze:
            if row[0] != 'X' or row[cols - 1] != 'X':
                return False

        return True


    def run_all_checks(self,maze):

        if not self.__check_file_empty(maze):
            error = "Maze is empty"
            
            return False, error
        
        if not self.__check_start_end_points(maze):
            error = "Maze does not have either start or/and end points"
            
            return False, error
        
        if not self.__check_multiple_start_end_points(maze):
            error = "Maze has multiple start or/and end points"
            
            return False, error
        
        if not self.__check_illegal_characters(maze):
            error = "Maze contains illegal characters"
            
            return False, error
        
        if not self.__check_maze_edges(maze):
            error = "Maze does not have walls on the edges"
            
            return False, error
        
        if not self.__check_maze_solvable(maze):
            error = "Maze is not solvable"
            
            return False, error
        
        return True, None
    
