Installation (Dependencies)

This project is built using Python 3 and only uses built-in libraries:

tkinter → For GUI interface

heapq → For priority queue (used in A* and GBFS)

random → For obstacle generation

math → For heuristic calculations

time → For performance measurement

No external packages are required.

Make sure Python 3.8 or higher is installed.

To verify Python installation:

python --version

If Tkinter is not installed (rare case on Linux), install it using:

sudo apt install python3-tk
How to Run

Navigate to the project folder:

cd dynamic-pathfinding-agent

Run the Python file:

python main.py

(Replace main.py with your actual filename if different.)

After running:

The GUI window will open.

Set rows, columns, and obstacle density.

Choose algorithm (A* or GBFS).

Choose heuristic (Manhattan or Euclidean).

Click Generate Map and then Start Search.

The system will display:

Path in red

Number of visited nodes

Path cost

Execution time
