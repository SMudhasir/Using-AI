# AI-Prompt Engineering - Glaude AI

## Prompt

As a python expert can you write a code for below requirements.
TicTacToa game with UI for 2 players,
Should have feature to rename the players,
Should update the Ui on mouse interaction,
Once the winner is decided it can be stored to a list and display the info in the panel on right side, Also should have clear history button.

## Response

---

I'll create a comprehensive TicTacToe game in Python using tkinter with all the features you requested. This will be a complete, functional game with a clean UI.I've created a comprehensive TicTacToe game that meets all your requirements! Here's what the code includes:

## Features Implemented:

**🎮 Core Game Functionality:**

- Full 3x3 TicTacToe game board with mouse interaction
- Two-player gameplay (X and O)
- Win detection (rows, columns, diagonals) and draw detection
- Visual feedback with different colors for each player

**👥 Player Management:**

- Rename functionality for both players via dialog boxes
- Current turn display showing player name and symbol
- Default names "Player 1" and "Player 2" that can be customized

**🖱️ Mouse Interaction:**

- Click on any empty cell to make a move
- Visual feedback when buttons are clicked
- Buttons become unclickable after being used

**🏆 Game History Panel:**

- Right-side panel displaying all game results
- Timestamped entries showing who won each game
- Scrollable list to handle multiple games
- "Clear History" button with confirmation dialog

**🎨 User Interface:**

- Clean, modern design with color-coded elements
- Responsive layout with proper spacing
- Winner announcements via popup messages
- "New Game" button to reset the board

## Key Features:

- **Player Renaming**: Click the "Rename Player" buttons to set custom names
- **Real-time Updates**: UI updates immediately on mouse clicks
- **History Tracking**: Every completed game is stored and displayed
- **Visual Polish**: Different colors for X (blue) and O (red) players

To run the game, simply execute the Python script. The tkinter library is part of Python's standard library, so no additional installations are needed. The game provides a complete, professional-looking TicTacToe experience with all the features you requested!
