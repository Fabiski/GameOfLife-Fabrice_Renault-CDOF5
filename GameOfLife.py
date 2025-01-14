import tkinter as tk

class GameOfLife:
    def __init__(self, root, rows=20, cols=40, cell_size=20):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.running = False

        # Create canvas
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create grid
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.rects = [[None for _ in range(cols)] for _ in range(rows)]

        # Bind events
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.root.bind("<Configure>", self.resize_grid)

        # Create buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="Start", command=self.start).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Stop", command=self.stop).pack(side=tk.LEFT)

        # Draw initial grid
        self.draw_grid()

    def draw_grid(self):
        """Draw the grid based on current canvas size."""
        self.canvas.delete("all")  # Clear the canvas
        self.rects = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.cell_size = min(width // self.cols, height // self.rows)

        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "black" if self.grid[r][c] else "white"
                self.rects[r][c] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def resize_grid(self, event):
        """Handle resizing of the canvas."""
        if event.widget == self.canvas:
            self.draw_grid()

    def toggle_cell(self, event):
        """Toggle cell state on mouse click."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = 1 - self.grid[row][col]
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
            self.canvas.after(100, self.run)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conway's Game of Life")
    game = GameOfLife(root)
    root.mainloop()

