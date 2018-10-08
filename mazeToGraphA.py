from heapq import heappop, heappush #heap used for greedy and a* to act as the queue
from collections import deque #works the same as a queue or a stack, allows appendleft and appends.
import numpy as np # dont think i used this
solution = open('solution.txt', 'w')#opens the solution file to write to

maze = [] #initialize the maze we will be using(file gets written to this list)
goal = None #goal location in the maze
cell = None #current cell used for heuristic

choice = 0
#choose your maze(could add more easily)
while not choice == '1' and not choice == '2' and not choice == '3':#will continue until you choose a valid choice, should have added a break out of this
    choice = input('1 - medium maze\n2 - large maze\n3 - open maze\n')
    if choice == '1':
        file = open('medium maze.txt', 'r')
    elif choice == '2':
        file = open('large maze.txt', 'r')
    elif choice == '3':
        file = open('open maze.txt', 'r')

#reading in file to 2D array
for line in file: #each row in the file
    row = []
    for symbol in line: #each symbol on the row gets added to row variable
        row += symbol
    maze.append(row)# appends the row list to the maze list(making a 2d array)
    #finds the goal location and start locations and saves them to use in the algorithms(helps with the graph)
    goal = [(ix,iy) for ix, row in enumerate(maze) for iy, i in enumerate(row) if i == '*']
    start = [(ix,iy) for ix, row in enumerate(maze) for iy, i in enumerate(row) if i == 'P']

#inefficient way to handle but changes goal and starting location again
for line in file:
    maze =[]
    row = []
    for symbol in line:
        row += symbol
        if (symbol == 'P'):
            #starting location needs to be converted back to being a blank for when the graph is made to put it into the graph
            symbol = ' '
        if (symbol == '*'):
            #goal locations needs to be converted back to being a blank for when the graph is made to put it inot the graph
            symbol = ' '
    maze.append(row)


def maze2graph(maze):
    height = len(maze) - 1 #height variable used
    width = len(maze[0]) - 1 if height else 0 #width variable
    graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j] == "%"} #creates the set of graph keys(graph is stored as a dictionary in this case and not using node objects
    for row, col in graph.keys(): #for each row and col number in the graph keys(because we stored tuples)
        if row < height - 1 and not maze[row+1][col] == '%': #if it isnt a wall we add the southern node as a neighbor, and to the southern guy we add this as the northern neighbor, and not the walls
            graph[(row, col)].append(("S", (row + 1, col)))
            graph[(row + 1, col)].append(("N", (row, col)))
        if col < width - 1 and not maze[row][col+1] == '%':#same as above but for eastern and western nodes
            graph[(row, col)].append(("E", (row, col + 1)))
            graph[(row, col + 1)].append(("W", (row, col)))
    return graph #returns the graph to our algorithms


def heuristic(cell, goal):#manhattan distance heuristic
    if type(cell) == list:#this section was built like trash because when i grabbed start, it was different format than when it gets sent again on 2nd loop through astar and greedy
        cellWant =  cell[0][0]
        goalWanted = goal[0][0]
        cellWanted = cell[0][1]#had to do this way because it was a list inside a tuple. should have fixed up top earlier when making the start and goal
        goalWant = goal[0][1]
        return abs(cellWant - goalWanted) + abs(cellWant - goalWant)
    else: #this is returned after the first runthrough of the loop, it sends current and current is formatted as a tuple, while goal is still a list
        return abs(cell[0]-goal[0][0]) + abs(cell[1] - goal[0][1])


def find_path_astar(maze):#Called to do the astar search, essentially the same as greedy with the cost so far added into the cost to decide if it should go back to an earlier spot
    pr_queue = [] #priority queue controlled using built in heap functions to auto sort and allows us to grab the min cost
    heappush(pr_queue, (0 + heuristic(start, goal), 0, "", start)) #push onto queue the heuristic, the so far cost, the path string(empty initially) and the location(start is the start)
    visited = set()
    graph = maze2graph(maze) #sends our 2d array off to be turned into a graph, could be more efficient and do this when the choice was made up top
    expanded = 0 #to keep count of how many nodes we looked at all together instead of just the path we took
    while pr_queue: #loops as long as something is in the queue, it starts with the start location in their and should push all neighbors onto it
        _, cost, path, current = heappop(pr_queue) #pop off of our queue
        if type(current) == list: #this was to fix the issue that start was a list of tuples(with only one tuple) should have been fixed at the top
            current = tuple(current[0]) #grabs the first thing in the list(a tuple) and makes sure it is in tuple format still and sets to current
        if current == goal[0]: #if the node we are looking at is the goal node, then we can be finished
            output(path, maze, expanded) #send the maze, path we took, and expanded count to be written into the solution
            return path #returns the path to be printed
        if current in visited: #if it is in visited thats fine, just go back to beginning of the loop
            continue
        visited.add(current) #adds the current to the visited list so we know where we have looked at
        for direction, neighbour in graph[current]: #for each direction and neighbor that is attached to the node in the graph(stores all the neighbors attached to each node)
            heappush(pr_queue, (cost + heuristic(neighbour, goal), cost + 1, path + direction, neighbour))#push each of those onto it with the costs + heuristic, cost to get their and path, plus directions and neighbors attached(essentially the node plus costs)
        expanded += 1 #one loop through this whole thing adds +1 to the things we have looked at
    return "NO WAY!" #if this happens it means it couldnt get to the goal



def find_path_bfs(maze): #opposite of dfs, searches every neighbor at each step, instead of trying to go deep first
    queue = deque([("", start)])#our queue is built as a deque which
    visited = set()#keep track of visited nodes
    graph = maze2graph(maze) #turn the maze into a graph
    expanded = 0#keep track of nodes looked at
    while queue: #while their are still things to look at it
        path, current = queue.popleft() #pop the path taken, and our current that we need to look at
        if type(current) == list: #to fix the start problem
            current = tuple(current[0]) #grab tuple out of the list
        if current == goal[0]: #end if we our at our goal
            output(path, maze, expanded) #go to make the solution file
            return path #send off to print our path
        if current in visited:# if its in the visited already, we just restart loop to look at next node
            continue #prevents looping in a cycle(biggest change from the tree version
        visited.add(current) #gets here because we hadnt visited, and we add to show that we touched this node
        for direction, neighbour in graph[current]: #for each seperate neighbor, push that onto the stack
            queue.append((path + direction, neighbour))
        expanded += 1 #one more node looked at
    return "NO WAY!"

def find_path_dfs(maze):#attempts to go deep first, and not search every neighbor
    stack = deque([("", start)])
    visited = set()
    graph = maze2graph(maze)#sends it turn into graph
    expanded = 0 #keep track of nodes looked at
    while stack: #while anything is in the stack
        path, current = stack.pop() #pop it off the stack to look at(this line is what allows it to be different than bfs
        if type(current) == list:#same as others
            current = tuple(current[0])#same as others
        if current == goal[0]:#same as others
            output(path,maze,expanded)#same as others
            return path#same as others
        if current in visited:#same
            continue
        visited.add(current)#same to keep track of where we have been already to prevent looping cycles
        for direction, neighbour in graph[current[0],current[1]]:
            stack.append((path + direction, neighbour))
        expanded += 1
    return "NO WAY!"

def find_path_greedy(maze): #works the same as the astar but does not store the cost so far, so is only the heuristic being stored which make its go faster and look at less overall nodes
    pr_queue = [] #which means it will only backtrack given that it goes into a deadend
    heappush(pr_queue, (0 + heuristic(start, goal), 0, "", start))
    visited = set()
    graph = maze2graph(maze)
    expanded = 0
    while pr_queue:
        _, cost, path, current = heappop(pr_queue)#return lowest cost still
        if type(current) == list:
            current = tuple(current[0])
        if current == goal[0]:
            output(path, maze, expanded)
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            heappush(pr_queue, (heuristic(neighbour, goal), cost, path + direction, neighbour)) #big change happens here, doesnt add to the cost so show we moved away, and stores just the heuristic, not cost + heuristic
        expanded += 1
    return "NO WAY!"

def output(path, maze, expanded): #used to write back to the file
    pathArray = list(path) #path given is in string format of each direction taken, we convert it to a character list to look at each direction individually
    x = start[0][0] #given in list format so pulls the first part of the list ([0]) then the first part of the tuple inside
    y = start[0][1] #same as above but second part of tbe tuple
    maze[x][y] = '.' #replaces our start with a .
    for i in pathArray: #for each character we loop and use the if statements to decide which direction our x and y go, and place a . their to indicate we were used that path
        if i == 'N': #check direction is N or north or up
            x -= 1
            maze[x][y] = '.' #drops the . to indicate we used this path
        elif i == 'S': #check direction for S = south = down
            x += 1
            maze[x][y] = '.' #drops the . to indicate we used this path
        elif i == 'E':# check direction for E =east= right
            y += 1
            maze[x][y] = '.' #drops the . to indicate we used this path
        elif i == 'W':# check direction for W=west=left
            y -= 1
            maze[x][y] = '.' #drops the . to indicate we used this path
        else:
            print('path string had an error') #this should never happen, would have error'd out well before this
    for row in maze: #now that we have changed all our parts of the path taken to .'s we can write the maze back to the solution file
        for i in row:
            solution.write(i)
    solution.write('\n' + str(expanded)) #adds at the bottom how many total moves were taken


choice = 0
while not choice == '1' and not choice == '2' and not choice == '3' and not choice =='4': #loops until a valid choice is made
    choice = input('1 - Depth First\n2 - Breadth First\n3 - A*\n4 - Greedy\n5 - Clean Solution')
    if choice == '1':
        path = find_path_dfs(maze)
    elif choice == '2':
        path = find_path_bfs(maze)
    elif choice == '3':
        path = find_path_astar(maze)
    elif choice == '4':
        path = find_path_greedy(maze)
    elif choice == '5':#this just cleans our solution file just in case something weird happens
        for row in maze:
            for i in row:
                solution.write(i)
print(path) #just to show the path given


