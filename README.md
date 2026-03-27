# Different_Engines

-- NOTE: Still a work in progress
-- Credits mainly go to Copilot

# How to properly use Basic_Chess_Engine.py
(Be sure to run this in Terminal, not IDLE)

1. Enter `pip install python-chess`

# Then,

#### Create engine with depth 4 (stronger) or depth 3 (faster)
engine = ChessEngine(max_depth=4)

#### Get best move for current position
board = chess.Board()
best_move = engine.get_best_move(board)
print(f"Best move: {best_move}")

#### Or play interactively
game = InteractiveChess(engine_depth=4)
game.play_game()
