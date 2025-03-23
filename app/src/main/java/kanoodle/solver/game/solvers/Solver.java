package kanoodle.solver.game.solvers;

import java.util.Map;

import kanoodle.solver.game.Level;
import kanoodle.solver.game.Piece;

public abstract class Solver {
    
        public Map<Character, Piece> pieces;

        public Solver(Map<Character, Piece> pieces) {
            this.pieces = pieces;
        }

        public abstract Level solve(Level level);
}
