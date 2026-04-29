# TextTicTacToe

## Description
A terminal-based Tic-Tac-Toe game written in Python, featuring a custom ANSI-based renderer for a visually asthetic terminal experience.

## Features

- **Custom ANSI Rendering**: The game uses ANSI escape codes to render a graphical-style board, including distinct colors for "X" (Red) and "O" (Green) and a stylized board grid.
- **Configurable Board Size**: Supports different board sizes (default is 3x3).
- **Win and Draw Detection**: Automatically detects rows, columns, and diagonals for wins, as well as draw states.

## Project Structure

- `main.py`: The entry point of the application. Manages the game loop, player input, and overall game state.
- `board.py`: Contains the `TicTacToe` logic, including board management, move validation, and win/draw checking.
- `board_render.py`: High-level rendering logic that translates the board state into renderable components.
- `board_renderables.py`: Low-level rendering primitives (lines, X shapes, O shapes) using ANSI escape sequences.

## How to Run Game: 

Ensure you have Python 3 installed. Run the game from your terminal:

```bash
python main.py
```

### Gameplay Instructions
1. The game will prompt "Player 1's Turn" or "Player 2's Turn".
2. Enter the Column (1 to board size) and Height (Row) (1 to board size) when prompted.
3. The board will refresh automatically after each move.
4. The game ends when a player wins or the board is full (draw).

## Requirements

- Python 3.x
- A terminal that supports ANSI escape codes (most modern terminals like PowerShell, CMD on Windows 10+, and Linux/macOS terminals). Some IDE terminals may not support ANSI escape codes.
