package kanoodle.algorithm.game;

public enum AnsiCode {
    RESET("\u001B[0m"),
    ORANGE("\u001B[38;5;208m"),
    RED("\u001B[91m"),
    DARK_BLUE("\u001B[94m"),
    LIGHT_PINK("\u001B[38;5;224m"),
    DARK_GREEN("\u001B[38;5;2m"),
    WHITE("\u001B[37m"),
    LIGHT_BLUE("\u001B[1;34m"),
    DARK_PINK("\u001B[38;5;205m"),
    YELLOW("\u001B[93m"),
    PURPLE("\u001B[95m"),
    LIGHT_GREEN("\u001B[38;5;47m"),
    GRAY("\u001B[38;5;248m");

    private String color;

    AnsiCode(String color) {
        this.color = color;
    }

    public String getAnsiCode() {
        return color;
    }
}
