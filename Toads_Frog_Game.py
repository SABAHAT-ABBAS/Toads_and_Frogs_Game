import tkinter as tk
from tkinter import messagebox

class ToadsFrogsPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Toads & Frogs Puzzle")
        self.root.resizable(False, False)
        
        self.bg_color = "lightSky blue1"
        self.toad_color = "orchid"
        self.frog_color = "light green"
        self.empty_color = "#f0f0f0"
        self.text_color = "black"
        self.title_color = "Dark slate gray"
        
        self.root.configure(bg=self.bg_color)
    
        self.n = 3
        self.state = None
        self.goal = None
        self.animating = False
        self.move_count = 0
        
        self.setup_ui()
        self.reset_puzzle()
    
    def setup_ui(self):
        """Setup the user interface with instructions and responsive grid."""
        self.main_frame = tk.Frame(self.root, bg=self.bg_color, padx=30, pady=30)
        self.main_frame.pack()
        
        # Row 0: Title
        title = tk.Label(self.main_frame, text="🐸 TOADS & FROGS PUZZLE 🐸", 
                        font=("Arial", 24, "bold"),
                        bg=self.bg_color, fg=self.title_color)
        title.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        instructions = tk.Label(self.main_frame, 
                               text="Goal: Swap all toads and frogs positions\n"
                                    "• Toads (Purple) move RIGHT →\n"
                                    "• Frogs (Green) move LEFT ←\n"
                                    "• Can slide 1 space or jump over 1 opponent",
                               font=("Arial", 11 , "bold"),
                               bg=self.bg_color, fg="black",
                               justify=tk.LEFT)
        instructions.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Row 2: Puzzle size selector
        size_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        size_frame.grid(row=2, column=0, columnspan=3, pady=(0, 15))
        
        tk.Label(size_frame, text="Puzzle Size:", 
                font=("Arial", 12, "bold"),
                bg=self.bg_color, fg=self.text_color).pack(side=tk.LEFT, padx=5)
        
        self.size_var = tk.IntVar(value=3)
        for size in range(2, 6):
            tk.Radiobutton(size_frame, text=str(size), 
                          variable=self.size_var, value=size,
                          font=("Arial", 11),
                          bg=self.bg_color, fg=self.text_color,
                          selectcolor=self.bg_color,
                          activebackground=self.bg_color,
                          command=self.change_size).pack(side=tk.LEFT, padx=5)
        
        # Row 3: Game board frame
        self.board_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.board_frame.grid(row=3, column=0, columnspan=3, pady=(0, 20))
        
        # Row 4: Status label
        self.status_label = tk.Label(self.main_frame, text="", 
                                     font=("Arial", 13, "bold"),
                                     bg=self.bg_color, fg="black")
        self.status_label.grid(row=4, column=0, columnspan=3, pady=(0, 15))
        
        # Row 5: Move counter
        self.move_label = tk.Label(self.main_frame, text="Moves: 0", 
                                   font=("Arial", 13, "bold"),
                                   bg=self.bg_color, fg=self.text_color)
        self.move_label.grid(row=5, column=0, columnspan=3, pady=(0, 15))
        
        # Row 6: Control buttons
        btn_style = {"font": ("Arial", 12, "bold"), "fg": "#ffffff", "width": 12, "pady": 10, "bd": 3}
        tk.Button(self.main_frame, text="🔄 Reset", bg="medium purple3", command=self.reset_puzzle, **btn_style).grid(row=6, column=0, padx=5, pady=5)
        tk.Button(self.main_frame, text="💡 Hint", bg="violet red", command=self.show_hint, **btn_style).grid(row=6, column=1, padx=5, pady=5)
        tk.Button(self.main_frame, text="🤖 Auto Solve", bg="Sky Blue4", command=self.auto_solve, **btn_style).grid(row=6, column=2, padx=5, pady=5)

    def change_size(self):
        """Update n and reset the board."""
        self.n = self.size_var.get()
        self.reset_puzzle()

    def reset_puzzle(self):
        """Reset puzzle to starting state [cite: 212-215]."""
        self.state = list('T' * self.n + '_' + 'F' * self.n)
        self.goal = list('F' * self.n + '_' + 'T' * self.n)
        self.move_count = 0
        self.animating = False
        self.move_label.config(text="Moves: 0")
        self.status_label.config(text="Click a piece to move it!", fg="black",font=("Arial", 13, "bold"))
        self.create_board()

    def create_board(self):
        """Dynamically adjusts cell width and padding to fit in the UI window."""
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        self.cells = []
        total_cells = 2 * self.n + 1
        
        dynamic_width = max(4, 11 - self.n * 1.5)
        dynamic_font_size = max(12, 22 - self.n * 2)
        dynamic_padx = max(1, 4 - (self.n // 2))

        for i, char in enumerate(self.state):
            btn_text = "🐢" if char == 'T' else "🐸" if char == 'F' else ""
            btn_bg = self.toad_color if char == 'T' else self.frog_color if char == 'F' else self.empty_color
            
            btn = tk.Button(self.board_frame, text=btn_text, 
                           width=int(dynamic_width), height=int(dynamic_width/2),
                           font=("Arial", int(dynamic_font_size), "bold"), 
                           bg=btn_bg,
                           command=lambda idx=i: self.make_manual_move(idx))
            btn.grid(row=0, column=i, padx=dynamic_padx, pady=3)
            self.cells.append(btn)

    def solve_priority_logic(self, start_state):
        """Algorithm 1: Brute-Force Priority Logic."""
        start_str = ''.join(start_state)
        goal_str = 'F' * self.n + '_' + 'T' * self.n
        
        from collections import deque
        queue = deque([[start_str]])
        visited = {start_str}
        
        while queue:
            path = queue.popleft()
            curr = path[-1]
            if curr == goal_str:
                return path
            
            s = list(curr); posE = s.index('_'); n_len = len(s)
            priority_moves = []
            
            # Priorities based on assignment logic
            if posE >= 2 and s[posE-2] == 'T':
                t = list(s); t[posE], t[posE-2] = t[posE-2], t[posE]; priority_moves.append(''.join(t))
            if posE <= n_len-3 and s[posE+2] == 'F':
                t = list(s); t[posE], t[posE+2] = t[posE+2], t[posE]; priority_moves.append(''.join(t))
            if posE >= 1 and s[posE-1] == 'T':
                t = list(s); t[posE], t[posE-1] = t[posE-1], t[posE]; priority_moves.append(''.join(t))
            if posE <= n_len-2 and s[posE+1] == 'F':
                t = list(s); t[posE], t[posE+1] = t[posE+1], t[posE]; priority_moves.append(''.join(t))
                
            for m in priority_moves:
                if m not in visited:
                    visited.add(m)
                    new_path = list(path)
                    new_path.append(m)
                    queue.append(new_path)
        return None

    def make_manual_move(self, idx):
        """Handles manual moves and checks for Dead Ends immediately."""
        if self.animating: return
        posE = self.state.index('_')
        # Movement rules validation
        if (self.state[idx] == 'T' and (idx == posE-1 or (idx == posE-2 and self.state[idx+1] == 'F'))) or \
           (self.state[idx] == 'F' and (idx == posE+1 or (idx == posE+2 and self.state[idx-1] == 'T'))):
            
            # Execute move
            self.state[idx], self.state[posE] = self.state[posE], self.state[idx]
            self.move_count += 1
            self.move_label.config(text=f"Moves: {self.move_count}")
            self.create_board()
            
            # Check for win condition
            if self.state == list(self.goal): 
                self.status_label.config(text="🎉 PUZZLE SOLVED! 🎉 ", fg="green")
            else:
                # DEAD END LOGIC: If algorithm returns None, the puzzle is unsolveable from here 
                if not self.solve_priority_logic(self.state):
                    self.status_label.config(text="❌ DEAD END! ❌", fg="red")
                    messagebox.showerror("Game Over", "💀💀 Dead End! 💀💀")

    def auto_solve(self):
        """Auto-solve using priority sequence."""
        if self.animating: return
        solution = self.solve_priority_logic(self.state)
        if solution:
            self.animating = True
            self.status_label.config(text="🤖 Auto-solving...", fg="black")
            self.animate(solution, 0)
        else:
            messagebox.showwarning("No Solution", "No path via priority logic from current state. Please Reset.")

    def animate(self, path, step):
        if step < len(path):
            self.state = list(path[step])
            self.move_label.config(text=f"Step: {step}")
            self.create_board()
            self.root.after(500, lambda: self.animate(path, step + 1))
        else:
            self.animating = False
            self.status_label.config(text="🎉 SOLVED 🎉 ", fg="green")

    def show_hint(self):
        sol = self.solve_priority_logic(self.state)
        if sol and len(sol) > 1:
            next_s = list(sol[1])
            for i in range(len(self.state)):
                if self.state[i] != next_s[i] and self.state[i] != '_':
                    messagebox.showinfo("Hint", f"Try moving cell {i+1}")
                    return
        messagebox.showinfo("Dead End", "No priority move possible! Reset the puzzle.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToadsFrogsPuzzle(root)
    root.mainloop()