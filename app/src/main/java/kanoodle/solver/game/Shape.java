package kanoodle.solver.game;

import java.util.Arrays;

import kanoodle.solver.game.util.RotationUtil;

public class Shape {
    private int rows;
    private int cols;
    private String shape;
    private int[][] matrix;

    public Shape(int rows, int cols, String shape) {
        this.rows = rows;
        this.cols = cols;
        this.shape = shape;
        this.matrix = toMatrix();
    }

    public Shape(int[][] matrix) {
        this.rows = matrix.length;
        this.cols = matrix[0].length;
        this.matrix = matrix;
        this.shape = toShape();
    }

    public Shape flip() {
        return new Shape(RotationUtil.flip(matrix));
    }

    public Shape transpose() {
        return new Shape(RotationUtil.transpose(matrix));
    }

    public int getRows() {
        return rows;
    }

    public int getCols() {
        return cols;
    }

    public String getShape() {
        return shape;
    }

    public int[][] getMatrix() {
        return matrix;
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();
        result.append("Rows: " + rows + "\n");
        result.append("Cols: " + cols + "\n");
        result.append("Shape: " + shape + "\n");
        result.append("Matrix: \n");
        for (int[] row : matrix) result.append(Arrays.toString(row)).append("\n");
        result.append("\n");
        return result.toString();
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + rows;
        result = prime * result + cols;
        result = prime * result + ((shape == null) ? 0 : shape.hashCode());
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null) return false;
        if (getClass() != obj.getClass()) return false;
        
        Shape other = (Shape) obj;
        if (rows != other.rows) return false;
        if (cols != other.cols) return false;
        if (shape == null && other.shape != null) return false;
        if (shape != null && !shape.equals(other.shape)) return false;
        return true;
    }

    private int[][] toMatrix() {
        int[][] matrix = new int[rows][cols];
        for (int i = 0; i < shape.length(); i++) {
            int row = i / cols, col = i % cols;
            matrix[row][col] = shape.charAt(i) - '0';
        }

        return matrix;
    }

    private String toShape() {
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                result.append(Character.forDigit(matrix[i][j], 10));
            }
        }

        return result.toString();
    }
}
