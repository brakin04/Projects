import java.util.ArrayList;
import java.util.Iterator;
import java.util.Random;

public class Deck {
    private static final int MAX_NUM_CARDS = 52;
    private ArrayList<Card> cards;
    Deck() {
        this.cards = new ArrayList<>(MAX_NUM_CARDS);
        this.populateDeck();
    }
    private void populateDeck() {
        for (Iterator<Suit> it = Suit.iterator(); it.hasNext(); ) {
            Suit s = it.next();
            for (int i = 1; i <= 13; i++) {
                cards.add(new Card(s, i));
            }
        }
    }
    public void shuffleDeck() {
        Random r = new Random();
        ArrayList<Card> newCards = new ArrayList<>();
        for (int i = 0; i < cards.size(); i++) {
            newCards.add(cards.remove(r.nextInt(cards.size())));
        }
        cards = newCards;
    }
    public Card drawCard() {
        if (cards.isEmpty()) {
            this.cards = new ArrayList<>(MAX_NUM_CARDS);
            this.populateDeck();
        }
        return cards.remove(cards.size()-1);
    }
    public boolean isEmpty() {
        return cards.isEmpty();
    }
}
