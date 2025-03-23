package kanoodle.algorithm.game;

import java.time.Duration;

public class Stats {
    private int milliseconds;
    private int seconds;
    private int minutes;
    private int hours;
    private long days;

    public Stats(long totalMilliseconds) {
        Duration duration = Duration.ofMillis(totalMilliseconds);
        this.days = duration.toDaysPart();
        this.hours = duration.toHoursPart();
        this.minutes = duration.toMinutesPart();
        this.seconds = duration.toSecondsPart();
        this.milliseconds = duration.toMillisPart();
    }

    @Override
    public String toString() {
        return String.format("Finished in %d days, %d hours, %d minutes, %d seconds, %d milliseconds\n", days, hours, minutes, seconds, milliseconds);
    }
}
