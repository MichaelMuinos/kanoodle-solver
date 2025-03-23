package kanoodle.solver.game.solvers.dancinglinks;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import kanoodle.solver.game.Board;
import kanoodle.solver.game.Piece;
import kanoodle.solver.game.Shape;

/**
 * I couldn't think of a better way to group this logic, so this class will
 * represent the 2D doubly linked list. The DancingLinksSolver will then be
 * responsible for performing operations on this class.
 */
public class DancingLinksDataStructure {
    
    private final Map<ColumnName, ColumnHeader> columnHeaders = new HashMap<>();
    private final ColumnHeader rootNode = new ColumnHeader();

    private Map<Character, Piece> pieces;
    private List<RowIdentifier> partialSolution;
    private List<RowIdentifier> finalSolution;

    public DancingLinksDataStructure(Map<Character, Piece> pieces) {
        this.pieces = pieces;
        this.partialSolution = new ArrayList<>();
    }

    public void createNodeConnections(Board board) {
        createColumnHeaders(board.getUnusedPieces(), board.getOpenSpotPositions());

        for (char letter : board.getUnusedPieces()) {
            List<Shape> shapes = pieces.get(letter).getShapes();
            for (int i = 0; i < shapes.size(); i++) {
                for (int j = 0; j < Board.ROWS; j++) {
                    for (int k = 0; k < Board.COLS; k++) {
                        List<Integer> positionsToFill = board.getPositionsToFill(letter, shapes.get(i), j, k);
                        // If the positionsToFill list is not empty, that means the shape can be successfully
                        // added to the board at this row and column index position. As a result, a new row
                        // should be created in the 2D doubly linked list.
                        if (!positionsToFill.isEmpty()) {
                            RowIdentifier identifier = new RowIdentifier(letter, positionsToFill);
                            createRow(identifier);
                        }
                    }
                }
            }
        }
    }

    /**
     * Knuth suggests executing the shortest columns first which will
     * drastically reduce the number of recursive calls required to find
     * a solution.
     */
    public ColumnHeader getShortestColumnHeader() {
        int shortest = Integer.MAX_VALUE;
        ColumnHeader header = (ColumnHeader) rootNode.right, shortestHeader = null;
        while (header != rootNode) {
            if (header.size < shortest) {
                shortest = header.size;
                shortestHeader = header;
            }

            header = (ColumnHeader) header.right;
        }

        return shortestHeader;
    }

    public void coverColumn(ColumnHeader header) {
        header.right.left = header.left;
        header.left.right = header.right;

        for (Node i = header.down; i != header; i = i.down) {
            for (Node j = i.right; i != j; j = j.right) {
                j.down.up = j.up;
                j.up.down = j.down;
                --j.header.size;
            }
        }
    }

    public void uncoverColumn(ColumnHeader header) {
        for (Node i = header.up; i != header; i = i.up) {
            for (Node j = i.left; i != j; j = j.left) {
                ++j.header.size;
                j.down.up = j;
                j.up.down = j;
            }
        }

        header.right.left = header;
        header.left.right = header;
    }

    public void dumpSolution() {
        finalSolution = new ArrayList<>();
        finalSolution.addAll(partialSolution);
    }

    public boolean foundSolution() {
        return finalSolution != null;
    }

    public List<RowIdentifier> getPartialSolution() {
        return partialSolution;
    }

    public List<RowIdentifier> getFinalSolution() {
        return finalSolution;
    }

    public ColumnHeader getRootNode() {
        return rootNode;
    }

    private void createColumnHeaders(List<Character> unusedPieces, List<Integer> openSpotPositions) {
        for (char letter : unusedPieces) {
            ColumnName letterColumn = ColumnName.letter(letter);
            createColumnHeaderConnection(letterColumn);
        }

        for (int position : openSpotPositions) {
            ColumnName positionColumn = ColumnName.position(position);
            createColumnHeaderConnection(positionColumn);
        }
    }

    private void createColumnHeaderConnection(ColumnName columnName) {
        ColumnHeader columnHeader = new ColumnHeader(columnName);
        columnHeader.left = rootNode.left;
        columnHeader.right = rootNode;
        rootNode.left.right = columnHeader;
        rootNode.left = columnHeader;
        columnHeaders.put(columnName, columnHeader);
    }
    
    private void createRow(RowIdentifier rowIdentifier) {
        // Create the key for fetching the unique column
        ColumnHeader letterColumn = columnHeaders.get(ColumnName.letter(rowIdentifier.letter));
        // Create the new row header using the letter column
        Node rowHeader = new Node(letterColumn, rowIdentifier, true);
        // Append the row header node to the letter column
        letterColumn.append(rowHeader);

        for (int position : rowIdentifier.positions) {
            ColumnHeader positionColumn = columnHeaders.get(ColumnName.position(position));
            Node node = new Node(positionColumn, rowIdentifier, false);

            // Create the connection for this node to the row
            node.left = rowHeader.left;
            node.right = rowHeader;
            rowHeader.left.right = node;
            rowHeader.left = node;

            // Create the connection for this node to its unique position column
            positionColumn.append(node);
        }
    }
}
