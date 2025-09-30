import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class TicTacToeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TicTacToe Game")
        self.root.geometry("1200x1000")
        self.root.configure(bg='#f0f0f0')
        
        # Game state variables
        self.board = [[''] * 3 for _ in range(3)]
        self.current_player = 'X'
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.game_over = False
        self.game_history = []
        
        # Create UI
        self.create_widgets()
        self.update_turn_display()
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Game area
        left_frame = tk.Frame(main_frame, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(left_frame, text="TicTacToe Game", 
                              font=('Arial', 24, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Player controls frame
        controls_frame = tk.Frame(left_frame, bg='#f0f0f0')
        controls_frame.pack(pady=(0, 20))
        
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
        self.player2_btn.pack(side=tk.LEFT)
        
        # Current turn display
        self.turn_label = tk.Label(left_frame, text="", 
                                  font=('Arial', 16, 'bold'), 
                                  bg='#f0f0f0', fg='#2c3e50')
        self.turn_label.pack(pady=(0, 20))
        
        # Game board frame
        board_frame = tk.Frame(left_frame, bg='#34495e', bd=2, relief=tk.RAISED)
        board_frame.pack()
        
        # Create 3x3 grid of buttons
        self.buttons = []
        for i in range(3):
            button_row = []
            for j in range(3):
                btn = tk.Button(board_frame, text='', 
                               width=8, height=4,
                               font=('Arial', 20, 'bold'),
                               bg='#ecf0f1', fg='#2c3e50',
                               command=lambda r=i, c=j: self.make_move(r, c),
                               bd=2, relief=tk.RAISED)
                btn.grid(row=i, column=j, padx=2, pady=2)
                button_row.append(btn)
            self.buttons.append(button_row)
        
        # Control buttons
        control_frame = tk.Frame(left_frame, bg='#f0f0f0')
        control_frame.pack(pady=20)
        
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
                                         width=25)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Clear history button
        clear_btn = tk.Button(right_frame, text="Clear History", 
                             command=self.clear_history,
                             bg='#e67e22', fg='white', 
                             font=('Arial', 10, 'bold'),
                             padx=10, pady=5)
        clear_btn.pack(pady=(5, 10))
        
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
    
    def update_turn_display(self):
        if not self.game_over:
            current_name = self.player1_name if self.current_player == 'X' else self.player2_name
            self.turn_label.config(text=f"Current Turn: {current_name} ({self.current_player})")
    
    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != '':
            return
        
        # Make the move
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(text=self.current_player)
        
        # Update button color based on player
        if self.current_player == 'X':
            self.buttons[row][col].config(fg='#3498db')
        else:
            self.buttons[row][col].config(fg='#e74c3c')
        
        # Check for winner
        winner = self.check_winner()
        if winner:
            self.game_over = True
            winner_name = self.player1_name if winner == 'X' else self.player2_name
            self.turn_label.config(text=f"🎉 {winner_name} Wins!")
            self.add_to_history(f"{winner_name} ({winner}) wins!")
            messagebox.showinfo("Game Over", f"Congratulations {winner_name}!\nYou won!")
        elif self.is_board_full():
            self.game_over = True
            self.turn_label.config(text="It's a Draw!")
            self.add_to_history("Draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
        else:
            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.update_turn_display()
    
    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        
        return None
    
    def is_board_full(self):
        for row in self.board:
            if '' in row:
                return False
        return True
    
    def add_to_history(self, result):
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = f"[{timestamp}] {result}"
        self.game_history.append(history_entry)
        self.history_listbox.insert(tk.END, history_entry)
        self.history_listbox.see(tk.END)  # Auto-scroll to bottom
    
    def clear_history(self):
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the game history?"):
            self.game_history.clear()
            self.history_listbox.delete(0, tk.END)
    
    def new_game(self):
        # Reset game state
        self.board = [[''] * 3 for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        
        # Reset button display
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', fg='#2c3e50', bg='#ecf0f1')
        
        # Update turn display
        self.update_turn_display()
    
    def run(self):
        self.root.mainloop()

# Create and run the game
if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()