public class Card {
    private Suit suit;
    private int value;

    Card(Suit suit, int value1) {
        this.suit = suit;
//        this.value = value1;
//        King queen and jack count as 10 in 21 so, Math.min is used.
        this.value = Math.min(value1, 10);
    }
    @Override
    public String toString() { return String.format("%d of %s", value, suit); }
    public int getValue() { return this.value; }
}
