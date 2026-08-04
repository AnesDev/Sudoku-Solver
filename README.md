# Sudoku Solver

A Python Sudoku solver implemented as part of the OpenMindsClub AI sub-team project. The repository provides two solving approaches (plain backtracking and a Constraint Satisfaction Problem (CSP) formulation), plus tools to compare their performance across difficulty levels.

Features
- Fast backtracking solver with simple heuristics
- CSP-based solver with constraint propagation
  
Demo
- Example input format (one line per row, use `0` or `.` for empty cells):
```
530070000
600195000
098000060
800060003
400803001
700020006
060000280
000419005
000080079
```

Quickstart

Prerequisites
- Python 3.8+ (3.10 recommended)

Clone the repo:
```bash
git clone https://github.com/AnesDev/Sudoku-Solver.git
cd Sudoku-Solver
```

Usage
```bash
python solve.py puzzles/example.txt
```
Contributors
- Anεs Khelif
- Dima Djema
- Inel Aouali
