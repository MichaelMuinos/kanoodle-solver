package kanoodle.solver.game.solvers.dancinglinks;

/*
 * The ColumnHeader represents the constraint for the problem. At least for
 * Kanoodle, there should be a maximum of 67 total constraints. 12 columns
 * for all of the pieces and 55 columns for each empty position of the board.
 * 
 * Assuming the board is not empty, there would be less constraints since
 * less pieces would need to be placed on the board + there would be less
 * open spots.
 */
public class ColumnHeader extends Node {
    // Size of the entire column (i.e. the number of nodes)
    public int size;
    // The unique name of the column (i.e. piece or position)
    public ColumnName name;
    // Determines if this header is the root node of the entire sparse matrix
    public boolean isRoot;

    public ColumnHeader() {
        // This constructor should only be used for the root node.
        this.name = null;
        this.isRoot = true;
    }

    public ColumnHeader(ColumnName name) {
        this.name = name;
        this.isRoot = false;
    }

    public void append(Node node) {
        node.down = this;
        node.up = this.up;
        up.down = node;
        up = node;

        ++size;
    }
}
