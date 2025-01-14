import tkinter as tk
import random

class GameOfLife:
    def __init__(self, root, cell_size=20):
        self.root = root
        self.cell_size = cell_size
        self.running = False
        self.speed = 100

        # Create canvas
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind events
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.canvas.bind("<B1-Motion>", self.paint_cell)
        self.root.bind("<Configure>", self.resize_grid)

        # Create buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="<", command=self.slow).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Start", command=self.start).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Stop", command=self.stop).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Clear", command=self.clear).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Random", command=self.randomize).pack(side=tk.LEFT)
        tk.Button(btn_frame, text=">", command=self.accelerate).pack(side=tk.LEFT)

        # Initialize grid
        self.rows = 0
        self.cols = 0
        self.grid = []
        self.rects = []

        # Draw initial grid
        self.resize_grid(None)

    def resize_grid(self, event):
        """Handle resizing of the canvas."""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Calculate rows and columns
        self.rows = height // self.cell_size
        self.cols = width // self.cell_size

        # Initialize grid
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.rects = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()

    def draw_grid(self):
        """Draw the grid on the canvas."""
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "black" if self.grid[r][c] else "white"
                self.rects[r][c] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def toggle_cell(self, event):
        """Toggle cell state on mouse click."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        self.change_cell_state(row, col)

    def paint_cell(self, event):
        """Change multiple cells state while dragging."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        self.change_cell_state(row, col)

    def change_cell_state(self, row, col):
        """Change the state of a cell if valid."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = 1
            self.update_cell(row, col)

    def update_cell(self, row, col):
        """Update cell color based on state."""
        color = "black" if self.grid[row][col] else "white"
        self.canvas.itemconfig(self.rects[row][col], fill=color)

    def count_neighbors(self, row, col):
        """Count live neighbors of a cell."""
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        count = 0
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == 1:
                count += 1
        return count

    def next_generation(self):
        """Compute the next generation of cells."""
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = self.count_neighbors(r, c)
                if self.grid[r][c] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[r][c] = 0  # Cell dies
                    else:
                        new_grid[r][c] = 1  # Cell survives
                else:
                    if neighbors == 3:
                        new_grid[r][c] = 1  # Cell becomes alive
        self.grid = new_grid
        self.update_display()

    def clear(self):
        """Clear the grid."""
        self.running = False
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.update_display()
        
    def randomize(self):
        """Randomize the grid."""
        self.grid = [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        self.update_display()
        
    def accelerate(self):
        """Randomize the grid."""
        self.speed = int(self.speed * 0.9)
    
    def slow(self):
        """Randomize the grid."""
        self.speed = int(self.speed * 1.1)

    def update_display(self):
        """Update the display based on the grid state."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.update_cell(r, c)

    def start(self):
        """Start the game loop."""
        self.running = True
        self.run()

    def stop(self):
        """Stop the game loop."""
        self.running = False

    def run(self):
        """Game loop."""
        if self.running:
            self.next_generation()
            self.canvas.after(self.speed, self.run)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conway's Game of Life")
    game = GameOfLife(root)
    root.mainloop()
