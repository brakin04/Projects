import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class goFish {
    private static Map<Integer, String> m = new HashMap<>();
    public goFishPlayer player;
    public ArrayList<goFishAI> ais;
    goFish () {
        this.player = new goFishPlayer();
        this.ais = new ArrayList<>();
        ais.add(new goFishAI("Fry"));
        ais.add(new goFishAI("Leela"));
        ais.add(new goFishAI("Bender"));
        m.put(1, "Ace"); m.put(11, "Jack"); m.put(12, "Queen"); m.put(13, "King");
    }
    private ArrayList<String> getNames() {
        ArrayList<String> ans = new ArrayList<>();
        for (goFishAI ai : ais) {
            ans.add(ai.getName());
        }
        return ans;
    }
    public void round(Scanner s) {
        goFishDeck deck = new goFishDeck();
        deck.shuffleDeck();
        boolean cont = true;
        for (int i = 0; i < 4; i++) {
            goFishCard card = deck.drawCard();
            player.addCard(card.getValue(), 1);
        }
        for (goFishAI ai : ais) {
            for (int i = 0; i < 4; i++) {
                goFishCard card = deck.drawCard();
                ai.addCard(card.getValue());
            }
        }
        ArrayList<Integer> ppcards= new ArrayList<>();
        ArrayList<ArrayList<Integer>> aipcards= new ArrayList<>();
//        ArrayList<Integer> lpcards= new ArrayList<>();
//        ArrayList<Integer> bpcards= new ArrayList<>();
        String aiNames = "";
        for (goFishAI ai : ais) {
            aiNames = aiNames + ai.getName() + ", ";
            aipcards.add(new ArrayList<>());
        }
        if (aiNames.charAt(aiNames.length() - 1) == ' ') {
            aiNames = aiNames.substring(0, aiNames.length() - 2);
        }
        while (cont) {
//            for (goFishAI ai : ais) {
//                System.out.println(ai.getName() + " hand: " + ai.getHand());
//            }
            if (deck.isEmpty())
                System.out.println("Deck is out!");
            goFishAI who = new goFishAI("zoid");
            // player
            if (!player.getHand().isEmpty() || !deck.isEmpty()) {
                if (player.getHand().isEmpty() && !deck.isEmpty()) {
                    player.addCard(deck.drawCard().getValue(), 1);
                }
                System.out.printf("Your hand is {Card = amount} %s \n", player.hand.toString());
                System.out.printf("Player names are: %s\n", aiNames);
                String[] turn = player.ask(getNames(), s);
                int what = Integer.parseInt(turn[1]);
                for (goFishAI ai : ais) {
                    if (ai.getName().equals(turn[0])) {
                        who = ai;
                        break;
                    }
                }
                if (who.getHand().containsKey(what)) {
                    int value = who.getHand().get(what);
                    player.addCard(what, value);
                    System.out.printf("You got %s %s(s) from %s\n", value, what, who.getName());
                    who.removeCard(what);
                } else {
                    if (!deck.isEmpty()) {
                        System.out.printf("%s: Go fish!\n", who.getName());
                        int c = deck.drawCard().getValue();
                        System.out.printf("You drew a %s\n", c);
                        player.addCard(c, 1);
                    } else
                        System.out.printf("%s doesn't have the card\n", who.getName());
                }
                for (int i = 1; i <= 13; i++) {
                    if (player.hand.containsKey(i)) {
                        if (player.hand.get(i) == 4) {
                            System.out.printf("You got a set of %ss \n", i);
                            player.addScore(1);
                            ppcards.add(i);
                            player.hand.remove(i);
                        }
                    }
                }
            }
            // This is each AI's turn
            for (int i = 0; i < ais.size(); i++) {
                if (!ais.get(i).getHand().isEmpty() || !deck.isEmpty()) {
                    if (!ais.get(i).askWho(player, ais))
                        if (!deck.isEmpty()) {
                            System.out.printf("%s went fishing \n", ais.get(i).getName());
                            ais.get(i).addCard(deck.drawCard().getValue());
                        } else
                            System.out.println("They don't have the card");
                    for (int j = 1; j <= 13; j++) {
                        if (ais.get(i).getHand().containsKey(j)) {
                            if (ais.get(i).getHand().get(j) == 4) {
                                System.out.printf("%s got a set of %ss \n", ais.get(i).getName(), j);
                                ais.get(i).addScore(1);
                                aipcards.get(i).add(j);
                                ais.get(i).removeCard(j);
                            }
                        }
                    }
                }
            }
            // Says if deck is empty or not
            if (deck.isEmpty())
                System.out.println("Deck is out!");
            System.out.printf("You have %s sets: %s\n", player.getScore(), ppcards);
            for (int i = 0; i < ais.size(); i++) {
                System.out.printf("%s has %s sets: %s\n", ais.get(i).getName(), ais.get(i).getScore(), aipcards.get(i));
            }
            // conti counts if all hands are empty
            int conti = 0;
            for (goFishAI ai : ais) {
                if (ai.getHand().isEmpty() && deck.isEmpty()) {
                    System.out.println(ai.getName() + "'s hand is empty.");
                    conti += 1;
                }
            }
            if (player.getHand().isEmpty() && deck.isEmpty()) {
                System.out.println("Your hand is empty.");
                conti += 1;
            }
            if (conti == 4) {
                // Default winner set to player
                String winner = "Player";
                int winScore = player.getScore();
                for (goFishAI ai : ais) {
                    if (ai.getScore() > winScore) {
                        // If has more sets, sets winner to AI name
                        winner = ai.getName();
                        winScore = ai.getScore();
                    } else if (ai.getScore() == winScore) {
                        // If tie, adds ai name to winner string
                        winner += " and " + ai.getName();
                    }
                }
                if (winner.split(" ").length > 1) {
                    // How its printed if tie
                    System.out.println("\nTie between " + winner + " with " + winScore + " sets!");
                } else {
                    // Otherwise
                    System.out.println("\nWinner: " + winner + " with " + winScore + " sets!");
                }
                cont = false;
            }
            for (goFishAI ai : ais)
                // at the end of each round, if an ai's hand is empty and the deck isn't, draw a card
                if (ai.getHand().isEmpty())
                    if (!deck.isEmpty())
                        ai.addCard(deck.drawCard().getValue());
            System.out.println("----------");
        }
    }

    public void playGame() {
        Scanner s = new Scanner(System.in);
        boolean cont = true;
        // Plays the game while player wants to keep playing
        while (cont) {
            for (goFishAI a : ais) {
                a.resetHand();
            }
            player.resetHand();
            round(s);
            if (!player.playAgain(s))
                cont = false;
            else {
                for (goFishAI ai : ais) {
                    ai.resetScore();
                }
                player.resetScore();
            }
        }
    }
    public static void main(String[] args) {
        new goFish().playGame();
    }
}
