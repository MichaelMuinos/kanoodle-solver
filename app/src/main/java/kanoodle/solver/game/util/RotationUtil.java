package kanoodle.solver.game.util;

import java.util.Arrays;

public class RotationUtil {
    /*
     * Flip the shape along the y-axis.
     */
    public static int[][] flip(int[][] matrix) {
        int rows = matrix.length, cols = matrix[0].length;
        int[][] result = deepCopy(matrix);
        for (int i = 0; i < rows; i++) {
            int j = 0, k = cols - 1;
            while (j < k) swap(result, i, j++, k--);
        }

        return result;
    }

    /*
     * Swap the shape's rows and columns.
     */
    public static int[][] transpose(int[][] matrix) {
        int rows = matrix.length, cols = matrix[0].length;
        int[][] result = new int[cols][rows];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                result[j][i] = matrix[i][j];
            }
        }

        return result;
    }

    private static void swap(int[][] matrix, int row, int col1, int col2) {
        int temp = matrix[row][col1];
        matrix[row][col1] = matrix[row][col2];
        matrix[row][col2] = temp;
    }

    private static int[][] deepCopy(int[][] matrix) {
        int rows = matrix.length, cols = matrix[0].length;
        int[][] newMatrix = new int[rows][cols];
        for (int i = 0; i < rows; i++) newMatrix[i] = Arrays.copyOf(matrix[i], cols);
        return newMatrix;
    }
}
