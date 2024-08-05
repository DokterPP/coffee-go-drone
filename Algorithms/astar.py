import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_maze_astar(maze):
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    
    start = (1, len(maze) - 2)
    goal = None
    
    # Find goal position
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 'e':
                goal = (x, y)
                break
        if goal:
            break
    
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))
    came_from = {}
    cost_so_far = {start: 0}
    
    while open_set:
        _, current_cost, current = heapq.heappop(open_set)
        
        if current == goal:
            break
        
        x, y = current
        for direction in range(4):
            nx, ny = x + dx[direction], y + dy[direction]
            if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] in ['.', 'e']:
                new_cost = cost_so_far[current] + 1
                next_node = (nx, ny)
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    heapq.heappush(open_set, (priority, new_cost, next_node))
                    came_from[next_node] = current
    
    # Reconstruct path
    if goal in came_from:
        current = goal
        while current != start:
            x, y = current
            maze[y][x] = '-'
            current = came_from[current]
        
        # Mark the start and goal
        sx, sy = start
        ex, ey = goal
        maze[sy][sx] = 's'
        maze[ey][ex] = 'e'
    
    print("Final maze:")
    for row in maze:
        print(''.join(row))
    
    return maze
