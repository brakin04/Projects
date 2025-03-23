import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;
import java.util.Scanner;
public class goFishAI {

    public int score;
    private HashMap<Integer, Integer> hand;
    public String name;

    goFishAI(String name) {
        this.name = name;
        this.hand = new HashMap<>();
        this.score = 0;
    }

    // Getter / reset methods
    public HashMap<Integer, Integer> getHand() {
        return hand;
    }
    public int getScore() {
        return score;
    }
    public void addScore(int score) {
        this.score += 1;
    }
    public void resetHand() {
        this.hand = new HashMap<>();
    }
    public String getName() {
        return this.name;
    }
    public void resetScore() {
        this.score = 0;
    }

    // Adds a card to an ai's hand
    public void addCard(Integer c) {
        if (!this.hand.containsKey(c))
            this.hand.put(c, 1);
        else {
            int i = this.hand.get(c);
            this.hand.put(c, i + 1);
        }
    }

    // Randomly chooses who to ask for a card player or AI
    public boolean askWho(goFishPlayer pl, ArrayList<goFishAI> ais) {
        Random rand = new Random();
        int size = ais.size();
        int k = rand.nextInt(0,size + 1);
        if (k == size) {
            // Asks player
            if (!pl.getHand().isEmpty())
                return askPlayer(pl);
            else // Choose again if hand is empty
                return askWho(pl, ais);
        } else if (ais.get(k).getName().equals(this.name)) {
            // Chose itself
            return askWho(pl, ais);
        } else {
            // Chose another AI
            if (!ais.get(k).getHand().isEmpty())
                return askAI(ais.get(k));
            else // Choose again if their hand is empty
                return askWho(pl, ais);
        }
    }

    // How this AI asks another AI
    private boolean askAI(goFishAI ai) {
        Random rand = new Random();
        int key = -1;
        // Chooses a random card to ask for
        while (!hand.containsKey(key))
            key = rand.nextInt(1, 14);
        System.out.printf("%s asked %s for %s \n", this.name, ai.getName(), key);
        if (ai.hand.containsKey(key)) {
            // AI had the card so it takes all that they had and removes it from the hand
            int value = ai.getHand().get(key);
            int valueAI = this.hand.get(key);
            this.hand.replace(key, value + valueAI);
            ai.hand.remove(key);
            System.out.printf("%s got %s card(s) \n", this.name, value);
            return true;
        } else {
            // AI didn't have the card
            return false;
        }
    }

    // How an AI asks player for a card
    private boolean askPlayer(goFishPlayer pl) {
        Random rand = new Random();
        int key = -1;
        // Chooses random card to ask for
        while (!hand.containsKey(key))
            key = rand.nextInt(1, 14);
        System.out.printf("%s asked you for %s \n", this.name, key);
        if (pl.getHand().containsKey(key)) {
            // Player had the card so it takes all from it and removes it from hand
            int value = pl.getHand().get(key);
            int valueAI = this.hand.get(key);
            this.hand.replace(key, value + valueAI);
            pl.hand.remove(key);
            System.out.printf("%s got %s card(s) \n", this.name, value);
            return true;
        } else {
            // Player didn't have the card
            return false;
        }
    }

    // Removes the card from AI's hand
    public void removeCard(int card) {
        this.hand.remove(card);
    }

}
