package kanoodle.solver.game;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

public class Board {
    public static final int ROWS = 5;
    public static final int COLS = 11;
    public static final char EMPTY = '-';

    private static final char BALL = '●';
    // The order matters here. We want to try adding the larger pieces to the board
    // first because then there will be less open spots on the board for each
    // successfully placed piece.
    private static final String LETTERS = "EGIBCHDLJAKF";

    private List<Character> unusedPieces;
    private List<Integer> openSpotPositions;
    private char[][] initialBoard;
    private char[][] finalBoard;

    public Board(Configuration configuration) {
        this.unusedPieces = new ArrayList<>();
        this.openSpotPositions = new ArrayList<>();
        this.initialBoard = new char[ROWS][COLS];
        this.finalBoard = new char[ROWS][COLS];

        // Add all pieces to the unused list
        for (char c : LETTERS.toCharArray()) this.unusedPieces.add(c);

        // Fill both boards with empty character symbols
        for (char[] row : initialBoard) Arrays.fill(row, EMPTY);
        for (char[] row : finalBoard) Arrays.fill(row, EMPTY);

        // Overwrite both boards with the configuration state
        overwriteBoards(configuration.getRows());
    }

    public List<Integer> getPositionsToFill(char letter, Shape shape, int startRowPos, int startColPos) {
        if (startRowPos + shape.getRows() - 1 >= ROWS || startColPos + shape.getCols() - 1 >= COLS) return new ArrayList<>();
        
        List<Integer> positionsToFill = new ArrayList<>();
        for (int i = startRowPos; i < startRowPos + shape.getRows(); i++) {
            for (int j = startColPos; j < startColPos + shape.getCols(); j++) {
                if (shape.getMatrix()[i - startRowPos][j - startColPos] == 1) {
                    if (finalBoard[i][j] != EMPTY) return new ArrayList<>();
                    positionsToFill.add(i * COLS + j);
                }
            }
        }

        return positionsToFill;
    }

    public boolean addPiece(char letter, List<Integer> positionsToFill) {
        if (positionsToFill.isEmpty()) return false;

        for (int pos : positionsToFill) {
            int x = pos / COLS, y = pos % COLS;
            finalBoard[x][y] = letter;
        }

        // The piece did fit on the board, so we return true
        return true;
    }

    public boolean addPiece(char letter, Shape shape, int startRowPos, int startColPos) {
        List<Integer> positionsToFill = getPositionsToFill(letter, shape, startRowPos, startColPos);
        return addPiece(letter, positionsToFill);
    }

    public void removePiece(char letter, Shape shape, int startRowPos, int startColPos) {
        for (int i = startRowPos; i < startRowPos + shape.getRows(); i++) {
            for (int j = startColPos; j < startColPos + shape.getCols(); j++) {
                if (finalBoard[i][j] == letter) {
                    finalBoard[i][j] = EMPTY;
                }
            }
        }
    }

    public List<Character> getUnusedPieces() {
        return unusedPieces;
    }

    public List<Integer> getOpenSpotPositions() {
        return openSpotPositions;
    }

    public char[][] getFinalBoard() {
        return finalBoard;
    }

    public String toString(Map<Character, Piece> pieces) {
        StringBuilder result = new StringBuilder();
        result.append("Pieces: " + getPiecesString(pieces) + "\n");
        result.append("Initial Board: \n" + getBoardString(initialBoard, pieces) + "\n");
        result.append("Final Board: \n" + getBoardString(finalBoard, pieces) + "\n");
        return result.toString();
    }

    private void overwriteBoards(List<String> rows) {
        for (int i = 0; i < rows.size(); i++) {
            String row = rows.get(i);
            for (int j = 0; j < row.length(); j++) {
                char letter = row.charAt(j);
                initialBoard[i][j] = letter;
                finalBoard[i][j] = letter;
                if (letter != EMPTY) unusedPieces.remove((Character) letter);
                else openSpotPositions.add(i * COLS + j);
            }
        }
    }

    private String getBoardString(char[][] board, Map<Character, Piece> pieces) {
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < board.length; i++) {
            for (int j = 0; j < board[0].length; j++) {
                char letter = board[i][j];
                String str = letter == EMPTY ? String.valueOf(EMPTY) : getBallString(pieces.get(letter).getColor());
                result.append(" " + str + " ");
            }

            result.append("\n");
        }

        return result.toString();
    }

    private String getPiecesString(Map<Character, Piece> pieces) {
        StringBuilder result = new StringBuilder();
        for (char letter : unusedPieces) {
            String color = AnsiCode.valueOf(pieces.get(letter).getColor()).getAnsiCode();
            result.append(color).append(" " + BALL + " ").append(AnsiCode.RESET.getAnsiCode());
        }

        return result.toString();
    }

    private String getBallString(String color) {
        String ansiCodeColor = AnsiCode.valueOf(color).getAnsiCode();
        return ansiCodeColor + BALL + AnsiCode.RESET.getAnsiCode();
    }
}
