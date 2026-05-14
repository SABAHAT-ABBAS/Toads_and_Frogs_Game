# Toads and Frogs Puzzle Game

A Python-based GUI implementation of the classic Toads and Frogs puzzle, featuring manual play and automated solving using breadth-first search with priority logic.

## Description

This project is a Design and Analysis of Algorithms (DAA) assignment that implements the Toads and Frogs puzzle. The puzzle involves swapping positions of toads (purple) and frogs (green) on a board with an empty space. Toads can only move right, frogs left, either by sliding one space or jumping over an opponent.

The game includes:
- Interactive GUI built with Tkinter
- Adjustable puzzle sizes (2-5)
- Manual gameplay with move validation
- Automated solver using BFS algorithm
- Hint system
- Dead-end detection

## Features

- **Manual Play**: Click on pieces to move them according to the rules
- **Auto-Solve**: Uses BFS with priority moves to find and animate the solution
- **Hints**: Provides suggestions for the next move
- **Dead-End Detection**: Alerts when the current state is unsolvable
- **Responsive UI**: Clean interface with colors and animations

## Requirements

- Python 3.x
- Tkinter (usually included with Python)

## How to Run

1. Clone the repository:
   ```
   git clone https://github.com/SABAHAT-ABBAS/Toads_and_Frogs_Game.git
   cd Toads_and_Frogs_Game
   ```

2. Run the game:
   ```
   python Toads_Frog_Game.py
   ```

## Algorithm

The auto-solver implements a breadth-first search (BFS) algorithm with priority-based move ordering:
1. Prioritize jumps over slides
2. Toads prioritize rightward moves, frogs leftward
3. Explores all possible states until goal is reached

## Controls

- **Reset**: Start a new game
- **Hint**: Get a suggestion for the next move
- **Auto Solve**: Let the algorithm solve the puzzle automatically

## License

This project is for educational purposes as part of a DAA course.