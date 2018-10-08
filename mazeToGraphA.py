from heapq import heappop, heappush
from collections import deque
import numpy as np
solution = open('solution.txt', 'w')

maze = []
goal = None
cell = None
goal = None

choice = 0
while not choice == '1' and not choice == '2' and not choice == '3':
    choice = input('1 - medium maze\n2 - large maze\n3 - open maze\n')
    if choice == '1':
        file = open('medium maze.txt', 'r')
    elif choice == '2':
        file = open('large maze.txt', 'r')
    elif choice == '3':
        file = open('open maze.txt', 'r')

#reading in file to 2D array
for line in file:
    row = []
    for symbol in line:
        row += symbol
    maze.append(row)
    goal = [(ix,iy) for ix, row in enumerate(maze) for iy, i in enumerate(row) if i == '*']
    start = [(ix,iy) for ix, row in enumerate(maze) for iy, i in enumerate(row) if i == 'P']

for line in file:
    maze =[]
    row = []
    for symbol in line:
        row += symbol
        if (symbol == 'P'):
            #starting location
            symbol = ' '
        if (symbol == '*'):
            #goal
            symbol = ' '
    maze.append(row)


def maze2graph(maze):
    height = len(maze) - 1
    width = len(maze[0]) - 1 if height else 0
    graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j] == "%"}
    for row, col in graph.keys():
        if row < height - 1 and not maze[row+1][col] == '%':
            graph[(row, col)].append(("S", (row + 1, col)))
            graph[(row + 1, col)].append(("N", (row, col)))
        if col < width - 1 and not maze[row][col+1] == '%':
            graph[(row, col)].append(("E", (row, col + 1)))
            graph[(row, col + 1)].append(("W", (row, col)))
    return graph


def heuristic(cell, goal):
    if type(cell) == list:
        cellWant =  cell[0][0]
        goalWanted = goal[0][0]
        cellWanted = cell[0][1]
        goalWant = goal[0][1]
        return abs(cellWant - goalWanted) + abs(cellWant - goalWant)
    else:
        return abs(cell[0]-goal[0][0]) + abs(cell[1] - goal[0][1])


def find_path_astar(maze):
    pr_queue = []
    heappush(pr_queue, (0 + heuristic(start, goal), 0, "", start))
    visited = set()
    graph = maze2graph(maze)
    while pr_queue:
        _, cost, path, current = heappop(pr_queue)
        if type(current) == list:
            current = tuple(current[0])
        if current == goal[0]:
            output(path, maze)
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            heappush(pr_queue, (cost + heuristic(neighbour, goal), cost + 1, path + direction, neighbour))
    return "NO WAY!"



def find_path_bfs(maze):
    queue = deque([("", start)])
    visited = set()
    graph = maze2graph(maze)
    while queue:
        print('made it here')
        path, current = queue.popleft()
        if type(current) == list:
            current = tuple(current[0])
        if current == goal[0]:
            output(path, maze)
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            queue.append((path + direction, neighbour))
    return "NO WAY!"

def find_path_dfs(maze):
    stack = deque([("", start)])
    visited = set()
    graph = maze2graph(maze)
    while stack:
        path, current = stack.pop()
        if type(current) == list:
            current = tuple(current[0])
        if current == goal[0]:
            output(path,maze)
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current[0],current[1]]:
            stack.append((path + direction, neighbour))
    return "NO WAY!"

def find_path_greedy(maze):
    pr_queue = []
    heappush(pr_queue, (0 + heuristic(start, goal), 0, "", start))
    visited = set()
    graph = maze2graph(maze)
    while pr_queue:
        _, cost, path, current = heappop(pr_queue)
        if type(current) == list:
            current = tuple(current[0])
        if current == goal[0]:
            output(path, maze)
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            heappush(pr_queue, (heuristic(neighbour, goal), cost, path + direction, neighbour))
    return "NO WAY!"

def output(path, maze):
    pathArray = list(path)
    x = start[0][0]
    y = start[0][1]
    maze[x][y] = '.'
    for i in pathArray:
        if i == 'N':
            x -= 1
            maze[x][y] = '.'
        elif i == 'S':
            x += 1
            maze[x][y] = '.'
        elif i == 'E':
            y += 1
            maze[x][y] = '.'
        elif i == 'W':
            y -= 1
            maze[x][y] = '.'
        else:
            print('path string had an error')
    for row in maze:
        for i in row:
            solution.write(i)


choice = 0
while not choice == '1' and not choice == '2' and not choice == '3' and not choice =='4':
    choice = input('1 - Depth First\n2 - Breadth First\n3 - A*\n4 - Greedy\n5 - Clean Solution')
    if choice == '1':
        path = find_path_dfs(maze)
    elif choice == '2':
        path = find_path_bfs(maze)
    elif choice == '3':
        path = find_path_astar(maze)
    elif choice == '4':
        path = find_path_greedy(maze)
    elif choice == '5':
        for row in maze:
            for i in row:
                solution.write(i)
print(path)


