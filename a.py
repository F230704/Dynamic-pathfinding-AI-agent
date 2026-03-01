import tkinter as tk
from tkinter import ttk
import random
import heapq
import time
import math

CELL_SIZE = 25  

COLORS = {
    "empty": "#f0f8ff",
    "wall": "#212121",
    "start": "#ff9800",
    "goal": "#9c27b0",
    "path": "red",  
    "agent": "#f44336"
}

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Pathfinding Agent")
        self.root.configure(bg="#1e1e2f")

        self.rows = 20
        self.cols = 20
        self.grid = []
        self.start = (0,0)
        self.goal = (19,19)
        self.agent_pos = self.start
        self.nodes_visited = 0

        self.setup_styles()
        self.create_layout()
        self.create_grid()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=6,
                        background="#3a7bd5",
                        foreground="white")
        style.map("TButton",
                  background=[("active", "#2a5cad")])
        style.configure("TLabel",
                        background="#252540",
                        foreground="white",
                        font=("Segoe UI", 10))
        style.configure("Header.TLabel",
                        font=("Segoe UI", 18, "bold"),
                        background="#1e1e2f",
                        foreground="white")
    def create_layout(self):
        header = ttk.Label(self.root, text="Dynamic Pathfinding Agent",
                           style="Header.TLabel")
        header.pack(pady=10)

        main_frame = tk.Frame(self.root, bg="#1e1e2f")
        main_frame.pack()

        control_frame = tk.Frame(main_frame, bg="#252540", padx=15, pady=15)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)

        ttk.Label(control_frame, text="Rows").pack(anchor="w")
        self.row_entry = tk.Entry(control_frame)
        self.row_entry.insert(0, "20")
        self.row_entry.pack(fill="x", pady=3)

        ttk.Label(control_frame, text="Columns").pack(anchor="w")
        self.col_entry = tk.Entry(control_frame)
        self.col_entry.insert(0, "20")
        self.col_entry.pack(fill="x", pady=3)

        ttk.Label(control_frame, text="Obstacle Density").pack(anchor="w")
        self.density_entry = tk.Entry(control_frame)
        self.density_entry.insert(0, "0.3")
        self.density_entry.pack(fill="x", pady=3)

        ttk.Button(control_frame, text="Generate Map",
                   command=self.generate_map).pack(fill="x", pady=5)

        ttk.Button(control_frame, text="Start Search",
                   command=self.start_search).pack(fill="x", pady=5)

        self.algorithm_var = tk.StringVar(value="A*")
        ttk.Label(control_frame, text="Algorithm").pack(anchor="w", pady=(10,0))
        ttk.OptionMenu(control_frame, self.algorithm_var,
                       "A*", "A*", "GBFS").pack(fill="x")

        self.heuristic_var = tk.StringVar(value="Manhattan")
        ttk.Label(control_frame, text="Heuristic").pack(anchor="w", pady=(10,0))
        ttk.OptionMenu(control_frame, self.heuristic_var,
                       "Manhattan", "Manhattan", "Euclidean").pack(fill="x")

        self.metrics_label = tk.Label(control_frame,
                                      text="Nodes: 0\nCost: 0\nTime: 0 ms",
                                      bg="#2d2d44",
                                      fg="white",
                                      font=("Segoe UI", 10),
                                      pady=10)
        self.metrics_label.pack(fill="x", pady=10)

        # Canvas Area
        self.canvas = tk.Canvas(main_frame, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.toggle_wall)

    def create_grid(self):
        try:
            self.rows = int(self.row_entry.get())
            self.cols = int(self.col_entry.get())
        except ValueError:
            self.rows = 20
            self.cols = 20

        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = (0,0)
        self.goal = (self.rows-1, self.cols-1)
        self.agent_pos = self.start

        self.canvas.config(width=self.cols*CELL_SIZE, height=self.rows*CELL_SIZE)
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c*CELL_SIZE
                y1 = r*CELL_SIZE
                x2 = x1+CELL_SIZE
                y2 = y1+CELL_SIZE
                color = COLORS["empty"]
                if (r,c)==self.start:
                    color = COLORS["start"]
                elif (r,c)==self.goal:
                    color = COLORS["goal"]
                elif self.grid[r][c]==1:
                    color = COLORS["wall"]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#cccccc")

    def toggle_wall(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if (row,col) not in [self.start,self.goal]:
            self.grid[row][col] = 1 - self.grid[row][col]
        self.draw_grid()

    def generate_map(self):
        self.create_grid()
        density = float(self.density_entry.get())
        for r in range(self.rows):
            for c in range(self.cols):
                if (r,c) not in [self.start,self.goal]:
                    if random.random() < density:
                        self.grid[r][c] = 1
        self.draw_grid()

    def heuristic(self,a,b):
        if self.heuristic_var.get()=="Manhattan":
            return abs(a[0]-b[0])+abs(a[1]-b[1])
        else:
            return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def search(self, start):
        open_list=[]
        heapq.heappush(open_list,(0,start))
        came_from={}
        g_cost={start:0}
        visited=set()
        self.nodes_visited=0

        farthest_node = start
        max_g = 0

        while open_list:
            _, current = heapq.heappop(open_list)
            if current in visited:
                continue
            visited.add(current)
            self.nodes_visited +=1

            if current==self.goal:
                return self.reconstruct_path(came_from,current), True

            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                tentative_g = g_cost[current]+1
                if self.algorithm_var.get()=="A*":
                    f = tentative_g + self.heuristic(neighbor,self.goal)
                else:
                    f = self.heuristic(neighbor,self.goal)

                if neighbor not in g_cost or tentative_g<g_cost.get(neighbor,float("inf")):
                    came_from[neighbor]=current
                    g_cost[neighbor]=tentative_g
                    heapq.heappush(open_list,(f,neighbor))

                    if tentative_g>max_g:
                        max_g = tentative_g
                        farthest_node = neighbor

        partial_path = self.reconstruct_path(came_from, farthest_node)
        return partial_path, False

    def reconstruct_path(self,came_from,current):
        path=[]
        while current in came_from:
            path.append(current)
            current=came_from[current]
        path.reverse()
        return path

    def get_neighbors(self,node):
        r,c = node
        neighbors=[]
        for dr,dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            nr,nc = r+dr,c+dc
            if 0<=nr<self.rows and 0<=nc<self.cols:
                if self.grid[nr][nc]==0:
                    neighbors.append((nr,nc))
        return neighbors

    def color_cell(self, position, color):
        r,c = position
        x1=c*CELL_SIZE
        y1=r*CELL_SIZE
        x2=x1+CELL_SIZE
        y2=y1+CELL_SIZE
        self.canvas.create_rectangle(x1,y1,x2,y2,fill=color,outline="#cccccc")

    def start_search(self):
        self.draw_grid()
        start_time = time.time()
        path, success = self.search(self.start)
        end_time = time.time()

        for node in path:
            if node not in [self.start,self.goal]:
                self.color_cell(node, COLORS["path"])
            self.root.update()
            time.sleep(0.05)

        execution_time = (end_time-start_time)*1000
        msg = "Path Found" if success else "No Path Found"
        self.metrics_label.config(
            text=f"{msg}\nNodes: {self.nodes_visited}\nCost: {len(path)}\nTime: {execution_time:.2f} ms"
        )

root = tk.Tk()
app = PathfindingApp(root)
root.mainloop()