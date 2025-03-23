package kanoodle.algorithm.game;

public class RawPiece {
    public char letter;
    public String color;
    public String shape;
    public int rows;
    public int cols;

    public RawPiece() {}

    public RawPiece(char letter, String color, String shape, int rows, int cols) {
        this.letter = letter;
        this.color = color;
        this.shape = shape;
        this.rows = rows;
        this.cols = cols;
    }

    public char getLetter() {
        return letter;
    }

    public void setLetter(char letter) {
        this.letter = letter;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public String getShape() {
        return shape;
    }

    public void setShape(String shape) {
        this.shape = shape;
    }

    public int getRows() {
        return rows;
    }

    public void setRows(int rows) {
        this.rows = rows;
    }

    public int getCols() {
        return cols;
    }

    public void setCols(int cols) {
        this.cols = cols;
    }
}
