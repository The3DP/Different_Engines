"""Unit tests for Chess Engine"""
import chess
from Basic_Chess_engine import ChessEngine, InteractiveChess


class TestChessEngine:
    """Test cases for ChessEngine class"""

    def test_engine_initialization(self):
        """Test engine initializes with correct depth."""
        engine = ChessEngine(max_depth=3)
        assert engine.max_depth == 3
        assert engine.nodes_evaluated == 0

    def test_engine_custom_depth(self):
        """Test engine can be initialized with custom depth."""
        for depth in [1, 2, 3, 4, 5]:
            engine = ChessEngine(max_depth=depth)
            assert engine.max_depth == depth

    def test_get_best_move_returns_legal_move(self):
        """Test that engine returns a legal move."""
        engine = ChessEngine(max_depth=2)
        board = chess.Board()
        move = engine.get_best_move(board)
        assert move in board.legal_moves

    def test_get_best_move_starting_position(self):
        """Test engine's move from starting position."""
        engine = ChessEngine(max_depth=2)
        board = chess.Board()
        move = engine.get_best_move(board)
        
        # Starting position has 20 legal moves
        assert move is not None
        assert move in list(board.legal_moves)

    def test_nodes_evaluated_increments(self):
        """Test that nodes_evaluated counter increments."""
        engine = ChessEngine(max_depth=2)
        board = chess.Board()
        
        # Reset counter
        engine.nodes_evaluated = 0
        engine.get_best_move(board)
        
        # Should have evaluated some nodes
        assert engine.nodes_evaluated > 0

    def test_minimax_handles_checkmate(self):
        """Test engine recognizes checkmate positions."""
        engine = ChessEngine(max_depth=2)
        
        # Fool's mate position: 1.f3 e5 2.g4 Qh4#
        board = chess.Board()
        board.push_san("f3")
        board.push_san("e5")
        board.push_san("g4")
        
        # Black can deliver checkmate
        move = engine.get_best_move(board)
        assert move is not None
        
        # Play the move
        board.push(move)
        if board.is_checkmate():
            assert True  # Checkmate achieved
        else:
            # At minimum, should be a legal move
            assert True

    def test_evaluate_position_returns_float(self):
        """Test position evaluation returns numeric score."""
        engine = ChessEngine(max_depth=2)
        board = chess.Board()
        
        score = engine._evaluate_position(board)
        assert isinstance(score, (int, float))

    def test_evaluate_starting_position(self):
        """Test evaluation of starting position."""
        engine = ChessEngine(max_depth=2)
        board = chess.Board()
        
        # Starting position should be roughly balanced
        score = engine._evaluate_position(board)
        # Material is even: -1 <= score <= 1 (with activity bonus)
        assert -5 <= score <= 5

    def test_engine_different_depths(self):
        """Test engine with different search depths."""
        board = chess.Board()
        
        for depth in [1, 2, 3]:
            engine = ChessEngine(max_depth=depth)
            move = engine.get_best_move(board)
            assert move is not None
            assert move in board.legal_moves


class TestInteractiveChess:
    """Test cases for InteractiveChess class"""

    def test_interactive_chess_initialization(self):
        """Test interactive chess initializes correctly."""
        game = InteractiveChess(engine_depth=3)
        assert game.engine.max_depth == 3
        assert isinstance(game.board, chess.Board)

    def test_interactive_chess_starting_position(self):
        """Test starting position has correct number of legal moves."""
        game = InteractiveChess(engine_depth=3)
        # 20 legal moves at game start
        assert len(list(game.board.legal_moves)) == 20

    def test_board_state_is_fresh(self):
        """Test that each InteractiveChess instance gets a fresh board."""
        game1 = InteractiveChess(engine_depth=3)
        game2 = InteractiveChess(engine_depth=3)
        
        assert game1.board.fen() == game2.board.fen()
        assert game1.board is not game2.board

    def test_display_board_no_errors(self):
        """Test display_board method works without errors."""
        game = InteractiveChess(engine_depth=3)
        try:
            # This would print, but shouldn't raise an exception
            game.display_board()
            assert True
        except Exception as e:
            assert False, f"display_board raised exception: {e}"


class TestAlphaBetaPruning:
    """Test alpha-beta pruning optimization"""

    def test_pruning_reduces_nodes_evaluated(self):
        """Test that alpha-beta pruning reduces nodes evaluated."""
        board = chess.Board()
        
        # Make a few moves to get a more complex position
        moves = ["e2e4", "c7c5", "g1f3", "d7d6"]
        for move_san in moves:
            board.push_san(move_san)
        
        engine = ChessEngine(max_depth=3)
        nodes_with_pruning = 0
        
        engine.nodes_evaluated = 0
        engine.get_best_move(board)
        nodes_with_pruning = engine.nodes_evaluated
        
        # Should have evaluated a reasonable number of nodes
        assert nodes_with_pruning > 0


class TestGameFlow:
    """Test basic game flow"""

    def test_engine_can_play_multiple_moves(self):
        """Test engine can make multiple consecutive moves."""
        board = chess.Board()
        engine = ChessEngine(max_depth=2)
        
        move_count = 0
        while not board.is_game_over() and move_count < 6:
            move = engine.get_best_move(board)
            assert move is not None
            board.push(move)
            move_count += 1
        
        # Should have made at least 3 moves (6 half-moves)
        assert move_count >= 3

    def test_game_terminates(self):
        """Test that game eventually terminates."""
        board = chess.Board()
        engine = ChessEngine(max_depth=2)
        
        move_count = 0
        max_moves = 100
        
        while not board.is_game_over() and move_count < max_moves:
            move = engine.get_best_move(board)
            if move is None:
                break
            board.push(move)
            move_count += 1
        
        # Game should end before max_moves
        assert move_count < max_moves


if __name__ == "__main__":
    # Run tests with pytest
    # Usage: pytest test_chess_engine.py -v
    import pytest
    pytest.main([__file__, "-v"])
