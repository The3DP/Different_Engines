import chess
import chess.pgn
from typing import Tuple, Optional

class ChessEngine:
    """A recursive chess engine using minimax algorithm with alpha-beta pruning."""
    
    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth
        self.nodes_evaluated = 0
    
    def get_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        """
        Find the best move for the current position.
        Uses recursive minimax with alpha-beta pruning.
        """
        self.nodes_evaluated = 0
        best_move = None
        best_value = float('-inf')
        
        for move in board.legal_moves:
            board.push(move)
            value = self._minimax(board, self.max_depth - 1, float('-inf'), float('inf'), False)
            board.pop()
            
            if value > best_value:
                best_value = value
                best_move = move
        
        print(f"Nodes evaluated: {self.nodes_evaluated}, Best value: {best_value}")
        return best_move
    
    def _minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
        """
        Recursive minimax algorithm with alpha-beta pruning.
        
        Args:
            board: Current chess board state
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: True if maximizing player's turn
        
        Returns:
            Evaluation score of the position
        """
        self.nodes_evaluated += 1
        
        # Base cases
        if depth == 0 or board.is_game_over():
            return self._evaluate_position(board)
        
        if is_maximizing:
            # Maximizing player (AI/White)
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score = self._minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
            
            return max_eval
        else:
            # Minimizing player (Opponent/Black)
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score = self._minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
            
            return min_eval
    
    def _evaluate_position(self, board: chess.Board) -> float:
        """
        Evaluate the current position.
        Returns a score from -infinity (black winning) to +infinity (white winning).
        """
        # Check terminal states
        if board.is_checkmate():
            return float('inf') if board.turn else float('-inf')
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        # Piece values
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0  # King value doesn't matter since it's protected
        }
        
        score = 0
        
        # Material count
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                if piece.color == chess.WHITE:
                    score += value
                else:
                    score -= value
        
        # Bonus for piece activity (simplified)
        score += len(list(board.legal_moves)) * 0.1 if board.turn else -len(list(board.legal_moves)) * 0.1
        
        return score


class InteractiveChess:
    """Interactive chess game interface."""
    
    def __init__(self, engine_depth: int = 4):
        self.board = chess.Board()
        self.engine = ChessEngine(max_depth=engine_depth)
    
    def display_board(self):
        """Display the current board state."""
        print("\n" + str(self.board))
        print(f"\nFEN: {self.board.fen()}")
    
    def play_game(self):
        """Main game loop for interactive play."""
        print("Welcome to Chess Engine!")
        print("You are playing as Black. Engine plays as White.")
        print("Enter moves in algebraic notation (e.g., e2e4, e7e5)")
        print("Type 'quit' to exit.\n")
        
        while not self.board.is_game_over():
            self.display_board()
            
            # Engine's move (White)
            if self.board.turn == chess.WHITE:
                print("\nEngine is thinking...")
                move = self.engine.get_best_move(self.board)
                if move:
                    self.board.push(move)
                    print(f"Engine plays: {move}")
                else:
                    print("No valid moves available!")
                    break
            
            # Human's move (Black)
            else:
                while True:
                    try:
                        move_input = input("\nYour move: ").strip()
                        
                        if move_input.lower() == 'quit':
                            print("Game ended.")
                            return
                        
                        move = chess.Move.from_uci(move_input)
                        if move in self.board.legal_moves:
                            self.board.push(move)
                            break
                        else:
                            print(f"Illegal move: {move_input}")
                    except ValueError:
                        print("Invalid input. Use format like 'e2e4'")
        
        # Game over
        self.display_board()
        print("\nGame Over!")
        
        if self.board.is_checkmate():
            print(f"Checkmate! {'White' if self.board.turn == chess.BLACK else 'Black'} wins!")
        elif self.board.is_stalemate():
            print("Stalemate! The game is a draw.")
        elif self.board.is_insufficient_material():
            print("Draw by insufficient material.")
        else:
            print("Game ended.")


if __name__ == "__main__":
    # Example 1: Automated game demonstration
    print("=" * 50)
    print("DEMO: Engine vs Engine (first 5 moves)")
    print("=" * 50)
    
    board = chess.Board()
    engine = ChessEngine(max_depth=3)
    move_count = 0
    
    while not board.is_game_over() and move_count < 10:
        print(f"\nMove {move_count // 2 + 1}: {'White' if board.turn == chess.WHITE else 'Black'}")
        move = engine.get_best_move(board)
        if move:
            print(f"Best move: {move}")
            board.push(move)
            move_count += 1
        else:
            break
    
    print("\n" + str(board))
    
    # Example 2: Interactive game (uncomment to play)
    # print("\n" + "=" * 50)
    # print("Starting interactive game...")
    # print("=" * 50)
    # game = InteractiveChess(engine_depth=4)
    # game.play_game()
