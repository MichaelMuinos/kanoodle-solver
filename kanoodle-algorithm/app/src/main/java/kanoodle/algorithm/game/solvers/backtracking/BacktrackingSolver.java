package kanoodle.algorithm.game.solvers.backtracking;

import java.util.List;
import java.util.Map;

import kanoodle.algorithm.game.Board;
import kanoodle.algorithm.game.Level;
import kanoodle.algorithm.game.Piece;
import kanoodle.algorithm.game.Shape;
import kanoodle.algorithm.game.Stats;
import kanoodle.algorithm.game.solvers.Algorithm;
import kanoodle.algorithm.game.solvers.Solver;

public class BacktrackingSolver extends Solver {

    public BacktrackingSolver(Map<Character, Piece> pieces) {
        super(pieces);
    }

    @Override
    public Level solve(Level level) {
        long startTime = System.currentTimeMillis();
        boolean solved = solveHelper(level.getBoard(), 0, 0);
        level.setStats(new Stats(System.currentTimeMillis() - startTime));
        level.setIsSolved(solved);
        level.setAlgorithm(Algorithm.BACKTRACKING_NO_PRUNING);
        return level;
    }

    /*
     * This is our backtracking algorithm. We know we will have successfully solved the
     * board if our pieceIndex ends up being the size of our unusedPieces list.
     */
    private boolean solveHelper(Board board, int pieceIndex, int shapeIndex) {
        if (pieceIndex == board.getUnusedPieces().size()) return true;

        char letter = board.getUnusedPieces().get(pieceIndex);
        Piece piece = pieces.get(letter);
        List<Shape> shapes = piece.getShapes();
        if (shapeIndex == shapes.size()) return false;

        Shape shape = shapes.get(shapeIndex);
        for (int i = 0; i < Board.ROWS; i++) {
            for (int j = 0; j < Board.COLS; j++) {
                if (board.addPiece(letter, shape, i, j)) {
                    // We need to try to prune some of the paths to reduce the runtime.
                    // Count the number of sections on the board and see if it is even possible
                    // to place the remaining unused pieces there.
                    if (solveHelper(board, pieceIndex + 1, 0)) return true;
                    // This is where we backtrack. We previously added this piece onto the board
                    // successfully, but further pieces were not able to be added which means we
                    // are not on the correct path for the solution. We need to remove this piece
                    // from the board in order to backtrack.
                    board.removePiece(letter, shape, i, j);
                }
            }
        }

        return solveHelper(board, pieceIndex, shapeIndex + 1);
    }
}

