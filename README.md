# Python Chess Engine

A minimax-based chess engine with alpha-beta pruning written in Python.

## Features

- **Minimax Algorithm**: Recursively evaluates chess positions by considering all possible moves
- **Alpha-Beta Pruning**: Optimizes search by eliminating branches that won't affect the final decision
- **Position Evaluation**: Scores positions based on material count and piece activity
- **Interactive Game Mode**: Play against the engine in the terminal
- **Configurable Difficulty**: Adjust search depth for speed vs strength tradeoff

## Installation

```bash
pip install -r requirements.txt
```

Or manually install the dependency:

```bash
pip install python-chess
```

## Usage

### Basic Usage - Find Best Move

```python
import chess
from Basic_Chess_engine import ChessEngine

# Create engine with depth 3 (faster) or 4 (stronger)
engine = ChessEngine(max_depth=4)
board = chess.Board()
best_move = engine.get_best_move(board)
print(f"Best move: {best_move}")
```

### Interactive Game

```python
from Basic_Chess_engine import InteractiveChess

# Play against the engine
game = InteractiveChess(engine_depth=4)
game.play_game()
```

**Note:** Run interactive mode in terminal, not IDLE.

#### How to Play Interactively

1. You play as Black, the engine plays as White
2. Enter moves in algebraic notation (e.g., `e2e4`, `e7e5`)
3. Type `quit` to exit

Example game session:
```
Welcome to Chess Engine!
You are playing as Black. Engine plays as White.
Enter moves in algebraic notation (e.g., e2e4, e7e5)
Type 'quit' to exit.

Engine is thinking...
Engine plays: e2e4

Your move: e7e5
```

## How It Works

### Minimax Algorithm

The engine evaluates positions recursively:
- **Maximizing Player (White)**: Tries to find the highest-scoring move
- **Minimizing Player (Black)**: Tries to find the lowest-scoring move
- **Pruning**: Cuts off branches that can't affect the final decision

### Position Evaluation

Positions are scored based on:
- **Checkmate**: ±∞ (perfect win/loss)
- **Material Count**: Piece values (Pawn=1, Knight=3, Bishop=3, Rook=5, Queen=9)
- **Piece Activity**: Bonus for having more legal moves available
- **Stalemate/Insufficient Material**: 0 (draw)

### Performance

- Nodes evaluated and best value are printed after each move
- Adjust `max_depth` for speed vs strength tradeoff:
  - `max_depth=2`: Fast but weak
  - `max_depth=3`: Reasonable balance
  - `max_depth=4`: Stronger but slower
  - `max_depth=5+`: Very slow

## Example Output

```
==================================================
DEMO: Engine vs Engine (first 5 moves)
==================================================

Move 1: White
Nodes evaluated: 400, Best value: 0.0
Best move: e2e4

Move 2: Black
Nodes evaluated: 2150, Best value: 0.0
Best move: e7e5

...

r n b q k b n r
p p p p . p p p
. . . . . . . .
. . . . p . . .
. . . . P . . .
. . . . . . . .
P P P P . P P P
R N B Q K B N R
```

## Project Structure

```
Py_Chess_Engine/
├── Basic_Chess_engine.py    # Main engine implementation
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── LICENSE                 # CC0 License
└── test_chess_engine.py    # Unit tests
```

## Development

### Running Tests

```bash
pytest test_chess_engine.py -v
```

### Future Improvements

- [ ] Move ordering optimization (evaluate captures/checks first)
- [ ] Opening book support
- [ ] Endgame tablebases
- [ ] Piece-square tables for better position evaluation
- [ ] Time-based search instead of depth-based
- [ ] GUI interface (pygame or tkinter)
- [ ] UCI protocol support for compatibility with chess GUIs

## License

Creative Commons Zero v1.0 Universal (CC0)

This work is dedicated to the public domain. You can copy, modify, and distribute this software without any restrictions.

## Credits

- Built with [python-chess](https://python-chess.readthedocs.io/) library
- Minimax algorithm with alpha-beta pruning implementation

## Notes

- Still a work in progress with planned enhancements
- For best experience, use depth 3-4 for interactive games
- Performance depends on board complexity and search depth
