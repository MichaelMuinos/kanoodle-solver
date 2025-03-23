package kanoodle.algorithm.game.solvers;

import java.util.Map;

import kanoodle.algorithm.game.Level;
import kanoodle.algorithm.game.Piece;

public abstract class Solver {
    
        public Map<Character, Piece> pieces;

        public Solver(Map<Character, Piece> pieces) {
            this.pieces = pieces;
        }

        public abstract Level solve(Level level);
}
