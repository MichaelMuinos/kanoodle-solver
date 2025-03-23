package kanoodle.solver.game.solvers.dancinglinks;

import java.util.Objects;

import com.google.auto.value.AutoOneOf;

/**
 * A column can either be a letter representing a piece or
 * an empty position on the board between 0 to 54 inclusive
 * (since there are only 55 positions total on the board).
 */
@AutoOneOf(ColumnName.Kind.class)
public abstract class ColumnName {
    public enum Kind {
        LETTER,
        POSITION,
    }

    public abstract Kind kind();

    public abstract char letter();

    public abstract int position();

    public static ColumnName letter(char letter) {
        return AutoOneOf_ColumnName.letter(letter);
    }

    public static ColumnName position(int position) {
        return AutoOneOf_ColumnName.position(position);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;

        ColumnName columnName = (ColumnName) obj;
        if (!this.kind().equals(columnName.kind())) return false;
        if (isLetter() && this.letter() != columnName.letter()) return false;
        if (!isLetter() && this.position() != columnName.position()) return false;

        return true;
    }

    @Override
    public int hashCode() {
        return Objects.hash(this.kind(), isLetter() ? this.letter() : this.position());
    }

    public boolean isLetter() {
        return this.kind().equals(Kind.LETTER);
    }
}
