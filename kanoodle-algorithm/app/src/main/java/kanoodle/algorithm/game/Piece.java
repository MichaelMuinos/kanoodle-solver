package kanoodle.algorithm.game;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Piece {
    private char letter;
    private String color;
    private List<Shape> shapes;
    private int ballCount;

    public Piece(RawPiece rawPiece) {
        this.letter = rawPiece.letter;
        this.color = rawPiece.color;
        this.shapes = createShapes(rawPiece);
        this.ballCount = countBalls();
    }

    public char getLetter() {
        return letter;
    }

    public String getColor() {
        return color;
    }

    public List<Shape> getShapes() {
        return shapes;
    }

    public int getBallCount() {
        return ballCount;
    }

    private List<Shape> createShapes(RawPiece rawPiece) {
        Shape initialShape = new Shape(rawPiece.rows, rawPiece.cols, rawPiece.shape);
        List<Shape> shapes = new ArrayList<>(Arrays.asList(initialShape, initialShape.transpose()));
        // If we transpose and rotate 90 degrees 3 times each, we will have a total of 8 shapes
        // maximum. There definitely will be duplicate shapes, but we can de-duplicate in a later
        // step.
        for (int i = 0; i < 3; i++) {
            Shape flipped = shapes.get(shapes.size() - 1).flip();
            shapes.add(flipped);
            Shape transposed = flipped.transpose();
            shapes.add(transposed);
        }

        // De-duplicate the shapes by passing the generated shapes to a set.
        Set<Shape> uniqueShapes = new HashSet<>(shapes);

        // We need to return a list of shapes and not a set because our backtracking algorithm
        // will need to keep track of indices. Sets do not have indices, it has no inherent ordering,
        // so a list will have to do.
        return new ArrayList<>(uniqueShapes);
    }

    private int countBalls() {
        int count = 0;
        for (char c : shapes.get(0).getShape().toCharArray()) {
            if (c - '0' == 1) {
                ++count;
            }
        }

        return count;
    }
}
