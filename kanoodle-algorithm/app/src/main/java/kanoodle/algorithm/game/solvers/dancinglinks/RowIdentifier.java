package kanoodle.algorithm.game.solvers.dancinglinks;

import java.util.List;

/**
 * A RowIdentifier is the information used to uniquely identify a row
 * in the 2D doubly linked list. This will be how we calculate the
 * partial solutions as we are performing dancing links.
 * 
 * Eventually when we find a solution, we can just pass each RowIdentifier
 * to the board to fill in the empty spots.
 */
public class RowIdentifier {
    public char letter;
    public List<Integer> positions;

    public RowIdentifier(char letter, List<Integer> positions) {
        this.letter = letter;
        this.positions = positions;
    }
}
