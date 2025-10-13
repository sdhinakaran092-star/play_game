import random
import tkinter as tk
from tkinter import messagebox

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.score = 0
        self.board = [[0]*size for _ in range(size)]
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == 0]
        if not empty_cells:
            return
        r, c = random.choice(empty_cells)
        self.board[r][c] = random.choice([2, 4])

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (self.size - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(self.size - 1):
            if row[i] == row[i+1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                row[i+1] = 0
        return row

    def move_left(self):
        changed = False
        new_board = []
        for row in self.board:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            final = self.compress(merged)
            new_board.append(final)
            if final != row:
                changed = True
        self.board = new_board
        return changed

    def move_right(self):
        self.board = [row[::-1] for row in self.board]
        changed = self.move_left()
        self.board = [row[::-1] for row in self.board]
        return changed

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def move_up(self):
        self.transpose()
        changed = self.move_left()
        self.transpose()
        return changed

    def move_down(self):
        self.transpose()
        changed = self.move_right()
        self.transpose()
        return changed

    def can_move(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return True
                if c < self.size-1 and self.board[r][c] == self.board[r][c+1]:
                    return True
                if r < self.size-1 and self.board[r][c] == self.board[r+1][c]:
                    return True
        return False

    def check_win(self):
        return any(2048 in row for row in self.board)


# ---------- GUI ----------
class GameGUI:
    def __init__(self, size=4):
        self.game = Game2048(size)
        self.size = size
        self.root = tk.Tk()
        self.root.title("2048 Game")
        self.root.configure(bg="#faf8ef")

        self.frame = tk.Frame(self.root, bg="#bbada0")
        self.frame.grid(padx=10, pady=10)

        self.cells = [[tk.Label(self.frame, text="", width=6, height=3,
                                font=("Helvetica", 24, "bold"),
                                bg="#cdc1b4", fg="#776e65", relief="ridge")
                       for _ in range(size)] for _ in range(size)]
        for r in range(size):
            for c in range(size):
                self.cells[r][c].grid(row=r, column=c, padx=5, pady=5)

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Helvetica", 16, "bold"))
        self.score_label.grid()

        restart_btn = tk.Button(self.root, text="Restart", font=("Helvetica", 14), command=self.restart)
        restart_btn.grid(pady=5)

        self.update_board()
        self.root.bind("<Key>", self.handle_key)
        self.root.mainloop()

    def restart(self):
        self.game = Game2048(self.size)
        self.update_board()

    def handle_key(self, event):
        key = event.keysym
        moved = False
        if key == 'Up':
            moved = self.game.move_up()
        elif key == 'Down':
            moved = self.game.move_down()
        elif key == 'Left':
            moved = self.game.move_left()
        elif key == 'Right':
            moved = self.game.move_right()

        if moved:
            self.game.add_new_tile()
            self.update_board()
            if self.game.check_win():
                messagebox.showinfo("2048", "You Win!")
            elif not self.game.can_move():
                messagebox.showinfo("2048", "Game Over!")

    def update_board(self):
        for r in range(self.size):
            for c in range(self.size):
                val = self.game.board[r][c]
                self.cells[r][c].config(text=str(val) if val != 0 else "", bg=self.get_color(val))
        self.score_label.config(text=f"Score: {self.game.score}")

    def get_color(self, value):
        colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#3c3a32")


if __name__ == "__main__":
    GameGUI(size=4)
