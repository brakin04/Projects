import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class goFishPlayer {

    private int score;
    public HashMap<Integer, Integer> hand;

    goFishPlayer() {
        this.hand = new HashMap<>();
        this.score = 0;
    }

    // Getter / setter / reset methods
    public HashMap<Integer, Integer> getHand() {
        return hand;
    }
    public int getScore() {
        return score;
    }
    public void addScore(int amnt) {
        this.score += amnt;
    }
    public void resetScore() {
        this.score = 0;
    }
    public void resetHand() {
        this.hand = new HashMap<>();
    }

    // Adds card(s) to hand
    public void addCard(int value, int amnt) {
        if (hand.containsKey(value)) {
            int j = hand.get(value);
            hand.replace(value, j + amnt);
        }
        else {
            hand.put(value, amnt);
        }
    }

    // Asks if player wants to play game again
    public boolean playAgain(Scanner s) {
        System.out.println("Do you want to play again? [y/n]");
        String input = s.nextLine().toLowerCase();
        while (!input.equals("y") && !input.equals("n")) {
            System.out.println(("Enter 'y' or 'n': "));
            input = s.nextLine().toLowerCase();
        }
        return input.equals("y");
    }

    // How the player asks an AI for a card
    public String[] ask(ArrayList<String> ais, Scanner s) {
        System.out.println("Who do you want to ask and for what? \n\tIn this form 'Name CardNumber'");
        String input = s.nextLine();
        String who = "";
        String[] str = input.split(" ");
        // Verifies it has both values
        if (str.length != 2) {
            System.out.println("Try again");
            return ask(ais, s);
        }
        String card = str[1];
        // Allows for either jack or 11 to be inputted
        switch (card.toLowerCase()) {
            case "ace" -> card = "1";
            case "jack" -> card = "11";
            case "queen" -> card = "12";
            case "king" -> card = "13";
        }
        // If no card, try again
        if (card.isEmpty()) {
            System.out.println("Try again");
            return ask(ais, s);
        }
        boolean someone = false;
        // Looks for an AI name matching the one entered
        for (String ai : ais) {
            if (ai.equalsIgnoreCase(str[0])) {
                who = ai;
                someone = true;
                System.out.printf("Asked: %s for %s\n", ai, card);
                break;
            }
        }
        // If none matched, try again
        if (!someone) {
            System.out.println("AI names are listed at the beginning. Try again");
            return ask(ais, s);
        }
        // Checks for card in player hand
        boolean hasIt = hand.containsKey(Integer.parseInt(card));
        if (!hasIt) {
            System.out.println("You don't have this card. Try again");
            return ask(ais, s);
        }
        return new String[]{who, card};
    }
}
