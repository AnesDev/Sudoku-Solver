# Sudoku Solver

A Python Sudoku solver implemented as part of the OpenMindsClub AI sub-team project. The repository provides two solving approaches (plain backtracking and a Constraint Satisfaction Problem (CSP) formulation), plus tools to compare their performance across difficulty levels.

Features
- Fast backtracking solver with simple heuristics
- CSP-based solver with constraint propagation
- Utilities to load puzzles from text files and run benchmarks
- (Optional) Command-line interface and example puzzles

Demo
- Add a screenshot or GIF of the solver running in `images/` (e.g., `images/demo.png`).
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
- pip (if there are dependencies)

Clone the repo:
```bash
git clone https://github.com/AnesDev/Sudoku-Solver.git
cd Sudoku-Solver
```

Install dependencies (if a requirements file exists):
```bash
pip install -r requirements.txt
```

Usage

- CLI (if a script like `solve.py` or `main.py` exists):
```bash
python solve.py puzzles/example.txt
```

- As a Python module:
```python
from solver import SudokuSolver  # adjust import path to your package layout

puzzle = [
  [5,3,0, 0,7,0, 0,0,0],
  [6,0,0, 1,9,5, 0,0,0],
  # ...
]

solver = SudokuSolver(puzzle)
solution = solver.solve()
print(solution)
```

Project structure
- `solver/` or `src/` — solver implementation (adjust if different)
- `puzzles/` — example puzzles and test inputs
- `tests/` — unit tests
- `README.md` — this file

Testing

If tests exist (pytest/unittest), run:
```bash
pytest
# or
python -m unittest discover
```

Contributing

Contributions are welcome. Please open an issue to discuss major changes before submitting a pull request. Suggested workflow:
- Fork the repo
- Create a branch: `git checkout -b feature/your-feature`
- Write tests for new functionality
- Keep commits focused and documented
- Submit a pull request describing the change

Contributors
- Anes (project lead) — https://github.com/AnesDev
- Dima Djema — collaborator
- Inel Aouali — collaborator

Please confirm with Dima and Inel before adding GitHub handles or additional role descriptions.

License

This repository has no license file at the moment. If you want a permissive license, consider adding an MIT License (create a `LICENSE` file with the MIT text).

Acknowledgements
- Thanks to everyone who helped test and improve the solver.
- References: Sudoku solving strategies, CSP tutorials, and related resources.

Contact
For questions or help, open an issue or contact: Anes (https://github.com/AnesDev)
