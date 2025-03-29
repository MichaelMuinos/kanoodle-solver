package kanoodle.algorithm.game;

import java.util.Map;

import kanoodle.algorithm.game.solvers.Algorithm;

public class Level {
    
    private int level;
    private Board board;
    private Stats stats;
    private boolean solved;
    private Algorithm algorithm;

    public Level(Configuration configuration) {
        this.level = configuration.getLevel();
        this.board = new Board(configuration);
        this.solved = false;
    }

    public Board getBoard() {
        return board;
    }

    public void setStats(Stats stats) {
        this.stats = stats;
    }

    public void setIsSolved(boolean solved) {
        this.solved = solved;
    }

    public void setAlgorithm(Algorithm algorithm) {
        this.algorithm = algorithm;
    }

    public String toString(Map<Character, Piece> pieces, boolean isNormalMode) {
        if (isNormalMode) return getNormalModeString();

        StringBuilder result = new StringBuilder();
        String levelString = "Level " + String.valueOf(level) + " (" + algorithm.toString() + ")";
        result.append(levelString + "\n" + "-".repeat(levelString.length()) + "\n");
        result.append(board.toString(pieces));

        if (solved) result.append(stats);
        else result.append("No valid answer.\n");

        return result.toString();
    }

    private String getNormalModeString() {
        if (!solved) return "[NORMAL_MODE] No valid answer. [NORMAL_MODE]";

        StringBuilder result = new StringBuilder("[NORMAL_MODE] ");
        char[][] finalBoard = board.getFinalBoard();
        for (int i = 0; i < finalBoard.length; i++) {
            for (int j = 0; j < finalBoard[0].length; j++) result.append(finalBoard[i][j]);
            if (i != finalBoard.length - 1) result.append(",");
        }

        return result.append(" [NORMAL_MODE]").toString();
    }
}
