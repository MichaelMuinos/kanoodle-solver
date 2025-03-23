package kanoodle.solver;

import java.io.File;
import java.util.Arrays;
import java.util.Map;

import com.beust.jcommander.IParameterValidator;
import com.beust.jcommander.Parameter;
import com.beust.jcommander.ParameterException;

import kanoodle.solver.game.Board;
import kanoodle.solver.game.Configuration;
import kanoodle.solver.game.Piece;
import kanoodle.solver.game.solvers.Solver;
import kanoodle.solver.game.solvers.backtracking.BacktrackingSolver;
import kanoodle.solver.game.solvers.backtracking.BacktrackingWithPruningSolver;
import kanoodle.solver.game.solvers.dancinglinks.DancingLinksSolver;
import kanoodle.solver.game.util.ParserUtil;

public class Args {
    private static final String NORMAL_MODE = "normal";
    private static final String TEST_MODE = "test";

    @Parameter(
        names = {"--mode", "-m"},
        description = "Mode to run the program. Either \"normal\" or \"test\".",
        required = true,
        validateWith = ModeValidator.class)
    private String mode;

    @Parameter(
        names = {"--algorithm", "-a"},
        description = "Algorithm to use in test mode. " + 
            "[1] Backtracking (no pruning) " + 
            "[2] Backtracking (pruning)" + 
            "[3] Dancing Links",
        validateWith = AlgorithmValidator.class)
    private Integer algorithm;

    @Parameter(
        names = {"--config", "-c"},
        description = "Configuration number to solve in test mode.",
        validateWith = ConfigValidator.class)
    private Integer config;

    @Parameter(
        names = {"--image", "-i"},
        description = "Image data representing a board in normal mode.",
        validateWith = ImageValidator.class)
    private String image;

    public void validate() {
        if (mode == null) throw new ParameterException("--mode is a required field.");
        if (mode.equals(NORMAL_MODE) && image == null) throw new ParameterException("--image is required in normal mode.");
        if (mode.equals(TEST_MODE) && (algorithm == null || config == null)) throw new ParameterException("--algorithm and --config are required in test mode.");
    }

    public static class ModeValidator implements IParameterValidator {
        @Override
        public void validate(String name, String value) throws ParameterException {
            if (!value.equals(NORMAL_MODE) && !value.equals(TEST_MODE)) {
                throw new ParameterException(name + " should be either \"normal\" or \"test\".");
            }
        }
    }

    public static class AlgorithmValidator implements IParameterValidator {
        @Override
        public void validate(String name, String value) throws ParameterException {
            int num = Integer.parseInt(value);
            if (num < 1 || num > 3) {
                throw new ParameterException(name + " should be [1] Backtracking (no pruning), [2] Backtracking (pruning), or [3] Dancing Links.");
            }
        }
    }

    public static class ConfigValidator implements IParameterValidator {
        @Override
        public void validate(String name, String value) throws ParameterException {
            File directory = new File(ParserUtil.CONFIGS_PATH);
            int num = Integer.parseInt(value), size = directory.listFiles().length;
            if (num < 1 || num > size) {
                throw new ParameterException(name + " can be between 1 and " + size + ".");
            }
        }
    }

    public static class ImageValidator implements IParameterValidator {
        @Override
        public void validate(String name, String value) throws ParameterException {
            String[] rows = value.split(",");
            boolean invalid = false;
            if (rows.length != Board.ROWS) invalid = true;
            for (String row : rows) if (row.length() != Board.COLS) invalid = true;
            if (invalid) throw new ParameterException(name + " is an invalid board size.");
        }
    }

    public boolean isNormalMode() {
        return mode.equals(NORMAL_MODE);
    }

    public Solver getAlgorithm(Map<Character, Piece> pieces) {
        if (isNormalMode() || algorithm == 3) return new DancingLinksSolver(pieces);
        if (algorithm == 1) return new BacktrackingSolver(pieces);
        if (algorithm == 2) return new BacktrackingWithPruningSolver(pieces);
        throw new IllegalArgumentException("Invalid algorithm.");
    }

    public Configuration getConfig() throws Exception {
        if (isNormalMode()) return new Configuration(Arrays.asList(image.split(",")));
        return ParserUtil.parseConfiguration(config);
    }
}
