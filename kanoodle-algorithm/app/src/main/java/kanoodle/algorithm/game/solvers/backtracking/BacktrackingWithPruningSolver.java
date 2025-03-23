package kanoodle.algorithm.game.solvers.backtracking;

import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;

import kanoodle.algorithm.game.Board;
import kanoodle.algorithm.game.Level;
import kanoodle.algorithm.game.Piece;
import kanoodle.algorithm.game.Shape;
import kanoodle.algorithm.game.Stats;
import kanoodle.algorithm.game.solvers.Algorithm;
import kanoodle.algorithm.game.solvers.Solver;

public class BacktrackingWithPruningSolver extends Solver {

    private static final int[][] DIRECTIONS = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

    public BacktrackingWithPruningSolver(Map<Character, Piece> pieces) {
        super(pieces);
    }

    @Override
    public Level solve(Level level) {
        long startTime = System.currentTimeMillis();
        PriorityQueue<Integer> orderedBallCounts = getOrderedBallCounts(level.getBoard().getUnusedPieces());
        boolean solved = solveHelper(level.getBoard(), orderedBallCounts, 0, 0);
        level.setStats(new Stats(System.currentTimeMillis() - startTime));
        level.setIsSolved(solved);
        level.setAlgorithm(Algorithm.BACKTRACKING_WITH_PRUNING);
        return level;
    }

    private PriorityQueue<Integer> getOrderedBallCounts(List<Character> unusedPieces) {
        PriorityQueue<Integer> queue = new PriorityQueue<>();
        for (char letter : unusedPieces) queue.add(pieces.get(letter).getBallCount());
        return queue;
    }

    /*
     * This is our backtracking algorithm. We know we will have successfully solved the
     * board if our pieceIndex ends up being the size of our unusedPieces list.
     */
    private boolean solveHelper(Board board, PriorityQueue<Integer> orderedBallCounts, int pieceIndex, int shapeIndex) {
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
                    orderedBallCounts.remove(piece.getBallCount());
                    if (hasValidSections(orderedBallCounts, board.getFinalBoard()) && solveHelper(board, orderedBallCounts, pieceIndex + 1, 0)) return true;
                    // This is where we backtrack. We previously added this piece onto the board
                    // successfully, but further pieces were not able to be added which means we
                    // are not on the correct path for the solution. We need to remove this piece
                    // from the board in order to backtrack.
                    orderedBallCounts.add(piece.getBallCount());
                    board.removePiece(letter, shape, i, j);
                }
            }
        }

        return solveHelper(board, orderedBallCounts, pieceIndex, shapeIndex + 1);
    }

    /**
     * This is needed to try to squeeze some optimization in our backtracking algorithm.
     */
    private boolean hasValidSections(PriorityQueue<Integer> orderedBallCounts, char[][] board) {
        if (orderedBallCounts.isEmpty()) return true;

        boolean[][] visited = new boolean[Board.ROWS][Board.COLS];
        for (int i = 0; i < Board.ROWS; i++) {
            for (int j = 0; j < Board.COLS; j++) {
                if (!visited[i][j] && board[i][j] == Board.EMPTY) {
                    int count = countSection(board, visited, i, j);
                    if (!isValidSection(orderedBallCounts.peek(), count)) return false;
                }
            }
        }

        return true;
    }

    /*
     * Counts the size of a section of the board that does not have any pieces.
     */
    private int countSection(char[][] board, boolean[][] visited, int i, int j) {
        if (i < 0 || j < 0 || i >= Board.ROWS || j >= Board.COLS || board[i][j] != Board.EMPTY || visited[i][j]) return 0;

        // Mark this position as visited so that we don't count it multiple times
        visited[i][j] = true;

        int count = 0;
        for (int[] direction : DIRECTIONS) {
            int x = direction[0] + i, y = direction[1] + j;
            count += countSection(board, visited, x, y);
        }

        return count;
    }

    /**
     * A section can't be valid if:
     * 1. The section size is <= 2 because there are no pieces smaller than size 3.
     * 2. The section size is exactly equal to 6 because no pieces make up that size.
     * 3. The smallest unused piece is greater than the section size.
     */
    private boolean isValidSection(int minBallCount, int sectionCount) {
        return sectionCount <= 2 || sectionCount == 6 || sectionCount < minBallCount;
    } 
}
