# #Part1


with open('inp1a.txt', 'r') as file:
    n, m = map(int, file.readline().strip().split())
    a, b = map(int, file.readline().strip().split())
    c, d = map(int, file.readline().strip().split())
    grid = [file.readline().strip() for _ in range(n)]

def heuristic_f(x1, x2, y1, y2):
    return abs(x1-x2) + abs(y1-y2)

def maze_solver(grid, start_state, goal_state, n, m):
    actions = [("U", -1, 0), ("D", 1, 0), ("R", 0, 1), ("L", 0, -1)]
    lst = []
    lst.append((heuristic_f(a, b, c, d), 0, a, b, " "))
    visited = {}

    while lst:
        min = 0
        for i in range(1, len(lst)):
            if lst[i][0] < lst[0][0]:            #searching the best node 
                min = i

        f_n, g_n, curr_x, curr_y, path = lst.pop(min)                      #gn actual cost from initial state to node n

        if curr_x == c and curr_y == d:
            print(f"{' -> '.join(path)}\n Total Steps: {g_n}")
            return 

    for move, pos_x, pos_y in actions:
        new_posx = curr_x + pos_x
        new_posy = curr_y + pos_y
    
    if grid[new_posx][new_posy]!= "#" and 0 <= new_posx <= n and 0 <= new_posy < m:       #booundary
        new_gn = g_n + 1
        
        if (new_posx, new_posy) not in visited or new_gn < visited[(new_posx, new_posy)]:       
            h_n = heuristic_f(new_posx, new_posy, c, d)
            f_n = new_gn + h_n
            visited[(new_posx, new_posy)] = new_gn                        #update visited 
            lst.append((f_n, new_gn, new_posx, new_posy, path + move))
    
    print(f"No path found")


result = maze_solver(grid, (a, b), (c, d), n, m)

with open('output1a.txt', 'w') as file:
    file.write(result)






#Part2

from queue import PriorityQueue

def admissibility_checker():
    with open("inp1b.txt", "r") as file:
        n, m = map(int, file.readline().strip().split())
        a, b = map(int, file.readline().strip().split())
    
    h_n = {}
    for _ in range(n):
        x, y = map(int, input().split())
        h_n[x] = y
    
    graph = {i: [] for i in range(1, n+1)}
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append((v))
        graph[v].append((u))

    dist = {i: float('inf') for i in range(1, n+1)}
    dist[b] = 0
    pq = PriorityQueue()
    pq.put((0, b))
    
    while pq:
        dist, u = pq.get()
            
        for v in graph[u]:
            if dist[u] + 1 < dist[v]:
                dist[v] = dist[u] + 1
                pq.put((dist[v], v))
    
    lst = []
    for i in range(1, n+1):
        if dist[i] != float('inf') and h_n[i] > dist[i]:
            lst.append(i)
    
    with open('output.txt', 'w') as file:
        if lst:
            file.write(f"0 {' '.join(lst)}\n")
        else:
            file.write(f"1")

admissibility_checker()