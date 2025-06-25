import tkinter as tk
from tkinter import ttk
import time
import random


board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]


def display_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))


def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


def is_valid_move(board, row, col, num):
    
    if num in board[row]:
        return False

   
    if num in [board[i][col] for i in range(9)]:
        return False

   
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True


def solve_sudoku_backtracking(board):
    start_time = time.perf_counter()
    empty_cell = find_empty_cell(board)
    if empty_cell is None:
        return True, time.perf_counter() - start_time

    row, col = empty_cell
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            solved, _ = solve_sudoku_backtracking(board)
            if solved:
                return True, time.perf_counter() - start_time
            board[row][col] = 0

    return False, time.perf_counter() - start_time


def solve_sudoku_forward_checking(board):
    start_time = time.perf_counter()
    empty_cell = find_empty_cell(board)
    if empty_cell is None:
        return True, time.perf_counter() - start_time

    row, col = empty_cell
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if forward_check(board, row, col, num):
                solved, _ = solve_sudoku_forward_checking(board)
                if solved:
                    return True, time.perf_counter() - start_time
            board[row][col] = 0

    return False, time.perf_counter() - start_time


def forward_check(board, row, col, num):
    for i in range(9):
        if i != col and board[row][i] == num:
            return False
        if i != row and board[i][col] == num:
            return False

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if (i != row or j != col) and board[i][j] == num:
                return False

    return True


def enforce_arc_consistency(board):
    queue = [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]

    while queue:
        row, col = queue.pop(0)
        domain = set(range(1, 10))

     
        for num in board[row]:
            domain.discard(num)

       
        for i in range(9):
            domain.discard(board[i][col])

     
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                domain.discard(board[i][j])

        if len(domain) == 1:
            board[row][col] = domain.pop()
            queue.extend((i, j) for i in range(9) for j in range(9) if board[i][j] == 0)


def solve_sudoku_arc_consistency(board):
    enforce_arc_consistency(board)
    empty_cell = find_empty_cell(board)
    if empty_cell is None:
        return True

    row, col = empty_cell
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if solve_sudoku_arc_consistency(board):
                return True
            board[row][col] = 0

    return False


def generate_random_sudoku():
    global board
    board = [[0] * 9 for _ in range(9)]
    solve_sudoku_backtracking(board)
    
    for _ in range(45):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        board[row][col] = 0


def solve_sudoku_gui(board, method):
    elapsed_time = 0
    if method == "backtracking":
        _, elapsed_time = solve_sudoku_backtracking(board)
    elif method == "forwardchecking":
        _, elapsed_time = solve_sudoku_forward_checking(board)
    elif method == "arcconsistency":
        start_time = time.perf_counter()
        solve_sudoku_arc_consistency(board)
        elapsed_time = time.perf_counter() - start_time
    return elapsed_time




class SudokuSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        self.board_frame = ttk.Frame(root)
        self.board_frame.pack(padx=10, pady=10)

        self.cells = [[None]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.cells[i][j] = tk.StringVar()
                entry = ttk.Entry(self.board_frame, textvariable=self.cells[i][j], width=2, justify="center")
                entry.grid(row=i, column=j, padx=1, pady=1)
                if board[i][j] != 0:
                    entry.insert(0, str(board[i][j]))
                    entry.config(state="readonly")

        self.method_frame = ttk.Frame(root)
        self.method_frame.pack(pady=5)

        self.method_label = ttk.Label(self.method_frame, text="Choose a method:")
        self.method_label.grid(row=0, column=0, padx=5)

        self.method_var = tk.StringVar(value="backtracking")

        self.backtracking_btn = ttk.Radiobutton(self.method_frame, text="Backtracking", variable=self.method_var, value="backtracking")
        self.backtracking_btn.grid(row=0, column=1, padx=5)

        self.forwardchecking_btn = ttk.Radiobutton(self.method_frame, text="Forward Checking", variable=self.method_var, value="forwardchecking")
        self.forwardchecking_btn.grid(row=0, column=2, padx=5)

        self.arcconsistency_btn = ttk.Radiobutton(self.method_frame, text="Arc Consistency", variable=self.method_var, value="arcconsistency")
        self.arcconsistency_btn.grid(row=0, column=3, padx=5)

        self.solve_btn = ttk.Button(root, text="Solve", command=self.solve_sudoku)
        self.solve_btn.pack(pady=5)

        self.generate_btn = ttk.Button(root, text="Generate Random Sudoku", command=self.generate_random_sudoku)
        self.generate_btn.pack(pady=5)

        self.time_label = ttk.Label(root, text="")
        self.time_label.pack(pady=5)

    def generate_random_sudoku(self):
        generate_random_sudoku()
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    self.cells[i][j].set(board[i][j])
                else:
                    self.cells[i][j].set("")

    def solve_sudoku(self):
        method = self.method_var.get()
        if method in ["backtracking", "forwardchecking", "arcconsistency"]:
          
            for i in range(9):
                for j in range(9):
                    if board[i][j] != 0:
                        self.cells[i][j].set(board[i][j])
                    else:
                        self.cells[i][j].set("")
        updated_board = [[int(cell.get() or 0) for cell in row] for row in self.cells]
        start_time = time.perf_counter()
        solving_time = solve_sudoku_gui(updated_board, method)
        solving_elapsed_time = time.perf_counter() - start_time
        self.time_label.config(text="Sudoku solved with {} in {:.6f} seconds".format(method, solving_elapsed_time))
        for i in range(9):
            for j in range(9):
                self.cells[i][j].set(updated_board[i][j])


def main():
    root = tk.Tk()
    app = SudokuSolverApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()