import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class DotsAndBoxesGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dots and Boxes Game")
        self.root.geometry("1200x1000")
        self.root.configure(bg='#f0f0f0')
        
        # Game settings
        self.grid_size = 10  # 4x4 grid of dots (3x3 boxes)
        self.dot_size = 8
        self.line_width = 4
        self.box_size = 80
        self.min_grid_size = 2
        self.max_grid_size = 8
        
        # Game state variables
        self.current_player = 1
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.player1_score = 0
        self.player2_score = 0
        self.game_over = False
        self.game_history = []
        
        # Line states: 0 = not drawn, 1 = player 1, 2 = player 2
        self.horizontal_lines = [[0 for _ in range(self.grid_size-1)] for _ in range(self.grid_size)]
        self.vertical_lines = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size-1)]
        
        # Box states: 0 = not completed, 1 = player 1, 2 = player 2
        self.boxes = [[0 for _ in range(self.grid_size-1)] for _ in range(self.grid_size-1)]
        
        # Create UI
        self.create_widgets()
        self.update_turn_display()
        self.update_score_display()
        self.draw_game_board()
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Game area
        left_frame = tk.Frame(main_frame, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(left_frame, text="Dots and Boxes", 
                              font=('Arial', 24, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Player controls frame
        controls_frame = tk.Frame(left_frame, bg='#f0f0f0')
        controls_frame.pack(pady=(0, 15))
        
        # Player name buttons
        self.player1_btn = tk.Button(controls_frame, text=f"Rename {self.player1_name}", 
                                    command=lambda: self.rename_player(1),
                                    bg='#3498db', fg='white', font=('Arial', 10),
                                    padx=10, pady=5)
        self.player1_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.player2_btn = tk.Button(controls_frame, text=f"Rename {self.player2_name}", 
                                    command=lambda: self.rename_player(2),
                                    bg='#e74c3c', fg='white', font=('Arial', 10),
                                    padx=10, pady=5)
        self.player2_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Grid size controls
        self.grid_size_btn = tk.Button(controls_frame, text=f"Grid Size: {self.grid_size-1}x{self.grid_size-1}", 
                                      command=self.change_grid_size,
                                      bg='#9b59b6', fg='white', font=('Arial', 10),
                                      padx=10, pady=5)
        self.grid_size_btn.pack(side=tk.LEFT)
        
        # Score and turn display
        info_frame = tk.Frame(left_frame, bg='#f0f0f0')
        info_frame.pack(pady=(0, 15))
        
        self.score_label = tk.Label(info_frame, text="", 
                                   font=('Arial', 14, 'bold'), 
                                   bg='#f0f0f0', fg='#2c3e50')
        self.score_label.pack()
        
        self.turn_label = tk.Label(info_frame, text="", 
                                  font=('Arial', 14, 'bold'), 
                                  bg='#f0f0f0', fg='#2c3e50')
        self.turn_label.pack(pady=(5, 0))
        
        # Game canvas - dynamic size
        canvas_size = max(400, (self.grid_size - 1) * self.box_size + 100)
        self.canvas = tk.Canvas(left_frame, width=canvas_size, height=canvas_size, 
                               bg='white', bd=2, relief=tk.SUNKEN)
        self.canvas.pack(pady=(0, 20))
        
        # Bind mouse clicks
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Control buttons
        control_frame = tk.Frame(left_frame, bg='#f0f0f0')
        control_frame.pack()
        
        new_game_btn = tk.Button(control_frame, text="New Game", 
                                command=self.new_game,
                                bg='#27ae60', fg='white', 
                                font=('Arial', 12, 'bold'),
                                padx=20, pady=8)
        new_game_btn.pack()
        
        # Right side - History panel
        right_frame = tk.Frame(main_frame, bg='#ecf0f1', bd=2, relief=tk.SUNKEN)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(20, 0))
        
        # History title
        history_title = tk.Label(right_frame, text="Game History", 
                                font=('Arial', 16, 'bold'), 
                                bg='#ecf0f1', fg='#2c3e50')
        history_title.pack(pady=(10, 5))
        
        # History listbox with scrollbar
        history_frame = tk.Frame(right_frame, bg='#ecf0f1')
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(history_frame, 
                                         yscrollcommand=scrollbar.set,
                                         font=('Arial', 10),
                                         bg='white', fg='#2c3e50',
                                         selectbackground='#3498db',
                                         width=30)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Clear history button
        clear_btn = tk.Button(right_frame, text="Clear History", 
                             command=self.clear_history,
                             bg='#e67e22', fg='white', 
                             font=('Arial', 10, 'bold'),
                             padx=10, pady=5)
        clear_btn.pack(pady=(5, 10))
    
    def draw_game_board(self):
        self.canvas.delete("all")
        
        # Calculate dynamic canvas size and offsets
        canvas_size = max(400, (self.grid_size - 1) * self.box_size + 100)
        self.canvas.config(width=canvas_size, height=canvas_size)
        
        board_width = (self.grid_size - 1) * self.box_size
        board_height = (self.grid_size - 1) * self.box_size
        offset_x = (canvas_size - board_width) // 2
        offset_y = (canvas_size - board_height) // 2
        
        # Draw dots
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = offset_x + j * self.box_size
                y = offset_y + i * self.box_size
                self.canvas.create_oval(x - self.dot_size//2, y - self.dot_size//2,
                                       x + self.dot_size//2, y + self.dot_size//2,
                                       fill='#2c3e50', outline='#2c3e50')
        
        # Draw horizontal lines
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                x1 = offset_x + j * self.box_size + self.dot_size//2
                y1 = offset_y + i * self.box_size
                x2 = offset_x + (j + 1) * self.box_size - self.dot_size//2
                y2 = y1
                
                if self.horizontal_lines[i][j] == 0:
                    # Draw clickable line area (invisible)
                    self.canvas.create_line(x1, y1, x2, y2, width=self.line_width * 3, 
                                          fill='', stipple='gray50', tags=f"h_line_{i}_{j}")
                else:
                    # Draw actual line
                    color = '#3498db' if self.horizontal_lines[i][j] == 1 else '#e74c3c'
                    self.canvas.create_line(x1, y1, x2, y2, width=self.line_width, 
                                          fill=color, capstyle=tk.ROUND)
        
        # Draw vertical lines
        for i in range(self.grid_size - 1):
            for j in range(self.grid_size):
                x1 = offset_x + j * self.box_size
                y1 = offset_y + i * self.box_size + self.dot_size//2
                x2 = x1
                y2 = offset_y + (i + 1) * self.box_size - self.dot_size//2
                
                if self.vertical_lines[i][j] == 0:
                    # Draw clickable line area (invisible)
                    self.canvas.create_line(x1, y1, x2, y2, width=self.line_width * 3, 
                                          fill='', stipple='gray50', tags=f"v_line_{i}_{j}")
                else:
                    # Draw actual line
                    color = '#3498db' if self.vertical_lines[i][j] == 1 else '#e74c3c'
                    self.canvas.create_line(x1, y1, x2, y2, width=self.line_width, 
                                          fill=color, capstyle=tk.ROUND)
        
        # Draw completed boxes
        for i in range(self.grid_size - 1):
            for j in range(self.grid_size - 1):
                if self.boxes[i][j] != 0:
                    x1 = offset_x + j * self.box_size + self.dot_size
                    y1 = offset_y + i * self.box_size + self.dot_size
                    x2 = offset_x + (j + 1) * self.box_size - self.dot_size
                    y2 = offset_y + (i + 1) * self.box_size - self.dot_size
                    
                    color = '#a8d8ff' if self.boxes[i][j] == 1 else '#ffb3b3'
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
                    
                    # Add player initial in the box
                    text = self.player1_name[0] if self.boxes[i][j] == 1 else self.player2_name[0]
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, 
                                          text=text, font=('Arial', 16, 'bold'),
                                          fill='#2c3e50')
    
    def on_canvas_click(self, event):
        if self.game_over:
            return
        
        # Find the closest line to the click
        closest_item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(closest_item)
        
        if not tags:
            return
        
        tag = tags[0]
        if tag.startswith('h_line_'):
            # Horizontal line clicked
            parts = tag.split('_')
            i, j = int(parts[2]), int(parts[3])
            if self.horizontal_lines[i][j] == 0:
                self.make_move('h', i, j)
        elif tag.startswith('v_line_'):
            # Vertical line clicked
            parts = tag.split('_')
            i, j = int(parts[2]), int(parts[3])
            if self.vertical_lines[i][j] == 0:
                self.make_move('v', i, j)
    
    def make_move(self, line_type, i, j):
        if self.game_over:
            return
        
        # Draw the line
        if line_type == 'h':
            self.horizontal_lines[i][j] = self.current_player
        else:
            self.vertical_lines[i][j] = self.current_player
        
        # Check for completed boxes
        boxes_completed = self.check_completed_boxes(line_type, i, j)
        
        # Update scores
        if self.current_player == 1:
            self.player1_score += boxes_completed
        else:
            self.player2_score += boxes_completed
        
        # Redraw the board
        self.draw_game_board()
        self.update_score_display()
        
        # Check if game is over
        if self.is_game_over():
            self.end_game()
        else:
            # Switch players only if no boxes were completed
            if boxes_completed == 0:
                self.current_player = 2 if self.current_player == 1 else 1
            self.update_turn_display()
    
    def check_completed_boxes(self, line_type, i, j):
        boxes_completed = 0
        
        if line_type == 'h':
            # Check boxes above and below the horizontal line
            if i > 0:  # Box above
                if self.is_box_complete(i-1, j):
                    self.boxes[i-1][j] = self.current_player
                    boxes_completed += 1
            if i < self.grid_size - 1:  # Box below
                if self.is_box_complete(i, j):
                    self.boxes[i][j] = self.current_player
                    boxes_completed += 1
        else:  # vertical line
            # Check boxes left and right of the vertical line
            if j > 0:  # Box to the left
                if self.is_box_complete(i, j-1):
                    self.boxes[i][j-1] = self.current_player
                    boxes_completed += 1
            if j < self.grid_size - 1:  # Box to the right
                if self.is_box_complete(i, j):
                    self.boxes[i][j] = self.current_player
                    boxes_completed += 1
        
        return boxes_completed
    
    def is_box_complete(self, box_i, box_j):
        # Check if all four lines around a box are drawn
        return (self.horizontal_lines[box_i][box_j] != 0 and  # top
                self.horizontal_lines[box_i + 1][box_j] != 0 and  # bottom
                self.vertical_lines[box_i][box_j] != 0 and  # left
                self.vertical_lines[box_i][box_j + 1] != 0)  # right
    
    def is_game_over(self):
        total_boxes = (self.grid_size - 1) * (self.grid_size - 1)
        return self.player1_score + self.player2_score == total_boxes
    
    def end_game(self):
        self.game_over = True
        
        if self.player1_score > self.player2_score:
            winner = self.player1_name
            self.turn_label.config(text=f"🎉 {winner} Wins!")
        elif self.player2_score > self.player1_score:
            winner = self.player2_name
            self.turn_label.config(text=f"🎉 {winner} Wins!")
        else:
            winner = "Draw"
            self.turn_label.config(text="It's a Draw!")
        
        # Add to history
        score_text = f"{self.player1_score}-{self.player2_score}"
        if winner == "Draw":
            self.add_to_history(f"Draw! ({score_text})")
        else:
            self.add_to_history(f"{winner} wins! ({score_text})")
        
        # Show message
        if winner == "Draw":
            messagebox.showinfo("Game Over", f"It's a draw!\nFinal Score: {self.player1_name} {self.player1_score} - {self.player2_score} {self.player2_name}")
        else:
            messagebox.showinfo("Game Over", f"Congratulations {winner}!\nFinal Score: {self.player1_name} {self.player1_score} - {self.player2_score} {self.player2_name}")
    
    def change_grid_size(self):
        """Allow user to change the grid size"""
        if not self.game_over and (self.player1_score > 0 or self.player2_score > 0 or 
                                   any(any(row) for row in self.horizontal_lines) or 
                                   any(any(row) for row in self.vertical_lines)):
            if not messagebox.askyesno("Change Grid Size", 
                                     "Changing grid size will start a new game. Continue?"):
                return
        
        # Create a dialog to select grid size
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Grid Size")
        dialog.geometry("300x200")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (300 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"300x200+{x}+{y}")
        
        tk.Label(dialog, text="Select Grid Size (Boxes)", 
                font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=20)
        
        # Current grid size display
        current_label = tk.Label(dialog, 
                               text=f"Current: {self.grid_size-1}x{self.grid_size-1} boxes", 
                               font=('Arial', 12), bg='#f0f0f0')
        current_label.pack(pady=5)
        
        # Scale for selecting grid size
        scale_var = tk.IntVar(value=self.grid_size-1)
        scale = tk.Scale(dialog, from_=self.min_grid_size-1, to=self.max_grid_size-1, 
                        orient=tk.HORIZONTAL, variable=scale_var,
                        font=('Arial', 10), bg='#f0f0f0',
                        label="Number of boxes per side:")
        scale.pack(pady=10, padx=20, fill=tk.X)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        def apply_change():
            new_size = scale_var.get() + 1
            if new_size != self.grid_size:
                self.grid_size = new_size
                self.reset_game_state()
                self.grid_size_btn.config(text=f"Grid Size: {self.grid_size-1}x{self.grid_size-1}")
                self.update_turn_display()
                self.update_score_display()
                self.draw_game_board()
            dialog.destroy()
        
        tk.Button(button_frame, text="Apply", command=apply_change,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(side=tk.LEFT)
    
    def reset_game_state(self):
        """Reset game state for new grid size"""
        self.current_player = 1
        self.player1_score = 0
        self.player2_score = 0
        self.game_over = False
        
        # Reset line and box states with new dimensions
        self.horizontal_lines = [[0 for _ in range(self.grid_size-1)] for _ in range(self.grid_size)]
        self.vertical_lines = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size-1)]
        self.boxes = [[0 for _ in range(self.grid_size-1)] for _ in range(self.grid_size-1)]
    
    def rename_player(self, player_num):
        current_name = self.player1_name if player_num == 1 else self.player2_name
        new_name = simpledialog.askstring("Rename Player", 
                                         f"Enter new name for {current_name}:",
                                         initialvalue=current_name)
        
        if new_name and new_name.strip():
            if player_num == 1:
                self.player1_name = new_name.strip()
                self.player1_btn.config(text=f"Rename {self.player1_name}")
            else:
                self.player2_name = new_name.strip()
                self.player2_btn.config(text=f"Rename {self.player2_name}")
            
            self.update_turn_display()
            self.update_score_display()
            self.draw_game_board()  # Redraw to update box labels
    
    def update_turn_display(self):
        if not self.game_over:
            current_name = self.player1_name if self.current_player == 1 else self.player2_name
            self.turn_label.config(text=f"Current Turn: {current_name}")
    
    def update_score_display(self):
        score_text = f"Score: {self.player1_name} {self.player1_score} - {self.player2_score} {self.player2_name}"
        self.score_label.config(text=score_text)
    
    def add_to_history(self, result):
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = f"[{timestamp}] {result}"
        self.game_history.append(history_entry)
        self.history_listbox.insert(tk.END, history_entry)
        self.history_listbox.see(tk.END)
    
    def clear_history(self):
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the game history?"):
            self.game_history.clear()
            self.history_listbox.delete(0, tk.END)
    
    def new_game(self):
        # Reset game state
        self.reset_game_state()
        
        # Update display
        self.update_turn_display()
        self.update_score_display()
        self.draw_game_board()
    
    def run(self):
        self.root.mainloop()

# Create and run the game
if __name__ == "__main__":
    game = DotsAndBoxesGame()
    game.run()