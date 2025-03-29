package kanoodle.algorithm.game.solvers.dancinglinks;

import javax.annotation.processing.Generated;

@Generated("com.google.auto.value.processor.AutoOneOfProcessor")
final class AutoOneOf_ColumnName {
  private AutoOneOf_ColumnName() {} // There are no instances of this type.

  static ColumnName letter(char letter) {
    return new Impl_letter(letter);
  }

  static ColumnName position(int position) {
    return new Impl_position(position);
  }

  // Parent class that each implementation will inherit from.
  private abstract static class Parent_ extends ColumnName {
    @Override
    public char letter() {
      throw new UnsupportedOperationException(kind().toString());
    }
    @Override
    public int position() {
      throw new UnsupportedOperationException(kind().toString());
    }
  }

  // Implementation when the contained property is "letter".
  private static final class Impl_letter extends Parent_ {
    private final char letter;
    Impl_letter(char letter) {
      this.letter = letter;
    }
    @Override
    public char letter() {
      return letter;
    }
    @Override
    public String toString() {
      return "ColumnName{letter=" + this.letter + "}";
    }
    @Override
    public ColumnName.Kind kind() {
      return ColumnName.Kind.LETTER;
    }
  }

  // Implementation when the contained property is "position".
  private static final class Impl_position extends Parent_ {
    private final int position;
    Impl_position(int position) {
      this.position = position;
    }
    @Override
    public int position() {
      return position;
    }
    @Override
    public String toString() {
      return "ColumnName{position=" + this.position + "}";
    }
    @Override
    public ColumnName.Kind kind() {
      return ColumnName.Kind.POSITION;
    }
  }

}
