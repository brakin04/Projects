import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

class Suit {

    public static final Suit CLUBS = new Suit("♣");
    public static final Suit DIAMONDS = new Suit("♦");
    public static final Suit HEARTS = new Suit("♥");
    public static final Suit SPADES = new Suit("♠");

    public static final int NUM_SUITS = 4;

    private String s;

    private Suit(String s) { this.s = s; }

    public static Iterator<Suit> iterator() {
        return new ArrayList<>(List.of(SPADES, CLUBS, HEARTS, DIAMONDS)).iterator();
    }

    @Override
    public String toString() { return this.s; }
}
