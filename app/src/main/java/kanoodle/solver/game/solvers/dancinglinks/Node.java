package kanoodle.solver.game.solvers.dancinglinks;

public class Node {
    public ColumnHeader header;
    public RowIdentifier identifier;
    public boolean isRowHeader;
    public Node left = this;
    public Node right = this;
    public Node up = this;
    public Node down = this;

    // This constructor will be used for the ColumnHeaders.
    public Node() {
        this.header = null;
        this.identifier = null;
        this.isRowHeader = false;
    }

    public Node(ColumnHeader header, RowIdentifier identifier, boolean isRowHeader) {
        this.header = header;
        this.identifier = identifier;
        this.isRowHeader = isRowHeader;
    }
}
