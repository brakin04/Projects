import java.util.ArrayList;
import java.util.Iterator;
import java.util.Random;

public class goFishDeck {

    public ArrayList<goFishCard> cards;

    goFishDeck() {
        this.cards = new ArrayList<>(104);
        this.populateDeck();
    }

    // Adds cards to the deck
    private void populateDeck() {
        for (int i = 1; i <= 52; i++) {
            int j = 0;
            switch (i) {
                case 1, 14, 27, 40 -> j = 1;
                case 2, 15, 28, 41 -> j = 2;
                case 3, 16, 29, 42 -> j = 3;
                case 4, 17, 30, 43 -> j = 4;
                case 5, 18, 31, 44 -> j = 5;
                case 6, 19, 32, 45 -> j = 6;
                case 7, 20, 33, 46 -> j = 7;
                case 8, 21, 34, 47 -> j = 8;
                case 9, 22, 35, 48 -> j = 9;
                case 10, 23, 36, 49 -> j = 10;
                case 11, 24, 37, 50 -> j = 11;
                case 12, 25, 38, 51 -> j = 12;
                case 13, 26, 39, 52 -> j = 13;
            }
            cards.add(new goFishCard(j));
        }
    }

    // Shuffles the deck
    public void shuffleDeck() {
        Random r = new Random();
        ArrayList<goFishCard> newCards = new ArrayList<>(52);
        for (int i = 0; i < 52; i++) {
            goFishCard j = cards.remove(r.nextInt(cards.size()));
            newCards.add(j);
        }
        this.cards = newCards;
    }

    // Returns top card in deck
    public goFishCard drawCard() {
        return this.cards.remove(cards.size()-1);
    }

    public boolean isEmpty() {
        return cards.isEmpty();
    }
}
