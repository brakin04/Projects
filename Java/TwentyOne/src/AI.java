import java.util.ArrayList;
import java.util.Random;

public class AI {
    public String name;
    private int score;
    private ArrayList<Card> hand;
    AI(String Name) {
        this.name = Name;
        this.hand = new ArrayList<>();
        this.score = 0;
    }
    public String getName() {
        return this.name;
    }
    public int getScore() {
        return this.score;
    }
    public void addCard(Card c) {
        score += c.getValue();
        hand.add(c);
    }
    public void resetHand() {
        hand = new ArrayList<>();
    }
    public void resetValue() {
        score = 0;
    }
    public String toString() {
        return this.hand.toString();
    }

    boolean play(Deck d) {
        score = getScore();
//        System.out.println("TT");
        if (score < 16 && score != 0) {
            Card u = d.drawCard();
            addCard(u);
            System.out.printf("%s drew: %s \n", this.name, u);
            return true;
        }
        else if (score > 16 && score < 21) {
            Random random = new Random();
            int k = random.nextInt(3);
//            System.out.println("UU");
            if (k == 0) {
                Card w = d.drawCard();
                addCard(w);
                System.out.printf("%s drew: %s \n", this.name, w);
                return true;
            }
        }
        System.out.printf("%s did not draw a card\n", this.getName());
        return false;
    }
}
