package kanoodle.solver.game.solvers.dancinglinks;

import java.util.Map;

import kanoodle.solver.game.Level;
import kanoodle.solver.game.Piece;
import kanoodle.solver.game.Stats;
import kanoodle.solver.game.solvers.Algorithm;
import kanoodle.solver.game.solvers.Solver;

public class DancingLinksSolver extends Solver {

    public DancingLinksSolver(Map<Character, Piece> pieces) {
        super(pieces);
    }

    @Override
    public Level solve(Level level) {
        long startTime = System.currentTimeMillis();

        // Create all of the node connections based on our board configuration
        DancingLinksDataStructure dl = new DancingLinksDataStructure(pieces);
        dl.createNodeConnections(level.getBoard());

        solveHelper(dl);
        level.setStats(new Stats(System.currentTimeMillis() - startTime));
        level.setIsSolved(dl.foundSolution());
        level.setAlgorithm(Algorithm.DANCING_LINKS);

        // We still need to update our board with the solution, assuming it was
        // successfully solved.
        if (dl.foundSolution()) {
            for (RowIdentifier identifier : dl.getFinalSolution()) {
                level.getBoard().addPiece(identifier.letter, identifier.positions);
            }
        }

        return level;
    }

    private void solveHelper(DancingLinksDataStructure dl) {
        // Check if we found a solution. Right now we only care about finding
        // one single solution, not all of them.
        if (dl.foundSolution()) return;

        if (dl.getRootNode().right == dl.getRootNode()) {
            dl.dumpSolution();
            return;
        }

        ColumnHeader header = dl.getShortestColumnHeader();
        dl.coverColumn(header);

        Node i = header.down;
        while (i != header) {
            // Cover the column
            dl.getPartialSolution().add(i.identifier);
            for (Node j = i.right; i != j; j = j.right) dl.coverColumn(j.header);

            if (!dl.foundSolution()) solveHelper(dl);

            // Uncover the column
            dl.getPartialSolution().remove(dl.getPartialSolution().size() - 1);
            for (Node j = i.left; i != j; j = j.left) dl.uncoverColumn(j.header);

            // Move to the next header and row
            header = i.header;
            i = i.down;
        }

        dl.uncoverColumn(header);
    }
}
