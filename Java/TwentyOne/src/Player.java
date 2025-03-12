import java.util.ArrayList;
import java.util.Scanner;

public class Player {
    private ArrayList<Card> hand;
    private int score;
    private int wins;

    Player() {
        this.hand = new ArrayList<>();
        this.score = 0;
    }
    public int addScore(int s) {
        return score += s;
    }
    public int getScore() {
        return this.score;
    }
    public String toString() {
        return this.hand.toString();
    }
    public void resetHand() {
        hand = new ArrayList<>();
    }
    public void addCard(Card c) {
        hand.add(c);
    }
    public void addWin() {
        wins += 1;
    }
    public int getWins() {
        return this.wins;
    }
    public int handValue() {
        int sum = 0;
        for (Card c : hand) {
            sum += c.getValue();
        }
        return sum;
    }
    public boolean keepPlaying(Scanner s) {
        System.out.println("Keep playing? : [Y/n]");
        String input = s.nextLine();
        return input.equalsIgnoreCase("y");
    }
    public boolean anotherCard(Scanner s) {
        System.out.println("Hit? : [Y/n]");
        String input = s.nextLine();
        return input.equalsIgnoreCase("y");
    }
}
