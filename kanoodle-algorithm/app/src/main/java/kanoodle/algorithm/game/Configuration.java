package kanoodle.algorithm.game;

import java.util.List;

public class Configuration {
    private int level;
    private List<String> rows;

    // This constructor will be used for normal mode, there is no
    // level number needed.
    public Configuration(List<String> rows) {
        this.rows = rows;
    }

    public Configuration(int level, List<String> rows) {
        this.level = level;
        this.rows = rows;
    }

    public int getLevel() {
        return level;
    }

    public List<String> getRows() {
        return rows;
    }
}
