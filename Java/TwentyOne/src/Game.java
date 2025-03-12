import java.util.ArrayList;
import java.util.Scanner;

public class Game {
    private Player player;
    private Player player1;
    private ArrayList<AI> ai;

    private String[] m = {"Ace", "","","","","","","","","", "Jack", "Queen", "King"};

    Game() {
        this.player = new Player();
        this.player1 = new Player();
        this.ai = new ArrayList<AI>();
        ai.add(new AI("Dave"));
        ai.add(new AI("John"));
        ai.add(new AI("Trey"));
//        ai.add(new AI());
    }
    public void playHand(Deck deck, Scanner s) {
        boolean pcont = true;
//        boolean pcont1 = true;
        boolean cont1 = true;
        boolean cont2 = true;
        boolean cont3 = true;
//        boolean cont4 = true;
        int p = player.handValue();
//        int p2 = player1.handValue();
        int a1 = ai.get(0).getScore();
        int a2 = ai.get(1).getScore();
        int a3 = ai.get(2).getScore();
//        int a4 = ai.get(3).getScore();
        deck.shuffleDeck();
//        deck.shuffleDeck();
        player.addCard(deck.drawCard());
        player.addCard(deck.drawCard());
        for (AI a : ai) {
            a.addCard((deck.drawCard()));
            a.addCard((deck.drawCard()));
        }
        for (AI a : ai) {
            System.out.printf("%s's Hand: %s Value: %s \n", a.getName(), a, a.getScore());
        }
        while (pcont || cont1 || cont2 || cont3) { // when adding more players/ai add their cont to this
            p = player.handValue();
//            p1 = player1.handValue();
            a1 = ai.get(0).getScore();
            a2 = ai.get(1).getScore();
            a3 = ai.get(2).getScore();
//            a4 = ai.get(3).getScore();
            System.out.printf("Hand: %s Value: %s \n", player, player.handValue());
            if (pcont) {
                if (player.anotherCard(s)) {
                    if (deck.isEmpty()) {
                        deck = new Deck();
                        deck.shuffleDeck();
                    }
                    Card c = deck.drawCard();
                    player.addCard(c);
                    if (c.getValue() > 10 || c.getValue() == 1) {
                        String q = m[(c.getValue() - 1)];
                        System.out.printf("Card: %s \n", q);
                    } else {
                        System.out.printf("Card: %s \n", c);
                    }
                } else {
                    pcont = false;
                }
            }
//            if (pcont1) {
//                if (player1.anotherCard(s)) {
//                    if (deck.isEmpty()) {
//                        deck = new Deck();
//                        deck.shuffleDeck();
//                    }
//                    Card c = deck.drawCard();
//                    player1.addCard(c);
//                    if (c.getValue() > 10 || c.getValue() == 1) {
//                        String q = m[(c.getValue() - 1)];
//                        System.out.printf("Card: %s \n", q);
//                    } else {
//                        System.out.printf("Card: %s \n", c);
//                    }
//                } else {
//                    pcont1 = false;
//                }
//            }
            if (cont1 && ai.get(0).getScore() != 0) {
                if (ai.get(0).getScore() > 21 || ai.get(0).getScore() == 0) {
                    cont1 = false;
                    ai.get(0).resetValue();
                }
                if (!ai.get(0).play(deck)) {
                    cont1 = false;
//                    System.out.printf("AI Hand Value: %d \n", ai.get(0).getScore());
                }
            }
            if (cont2 && ai.get(1).getScore() != 0) {
                if (ai.get(1).getScore() > 21 || ai.get(1).getScore() == 0) {
                    cont2 = false;
                    ai.get(1).resetValue();
                }
                if (!ai.get(1).play(deck)) {
                    cont2 = false;
//                    System.out.printf("AI Hand Value: %d \n", ai.get(1).getScore());
                }
            }
            if (cont3 && ai.get(2).getScore() != 0) {
                if (ai.get(2).getScore() > 21 || ai.get(2).getScore() == 0) {
                    cont3 = false;
                    ai.get(2).resetValue();
                }
                if (!ai.get(2).play(deck)) {
                    cont3 = false;
//                    System.out.printf("AI Hand Value: %d \n", ai.get(2).getScore());
                }
            }
//            if (cont4) {
//                if (ai.get(3).getScore() > 21) {
//                    cont4 = false;
//                    ai.get(3).resetValue();
//                }
//                if (!ai.get(3).play(deck)) {
//                    cont4 = false;
////                    System.out.printf("AI Hand Value: %d \n", ai.get(2).getScore());
//                }
//            }
            if (player.handValue() > 21) {
                pcont = false;
            }
//            if (player1.handValue() > 21) {
//                pcont1 = false;
//            }
            for (AI a : ai) {
                if (a.getScore() <= 21 && a.getScore() != 0)
                    System.out.printf("%s Value: %s \n", a.getName(), a.getScore());
                else {
                    System.out.printf("%s Bust\n", a.getName());
                }
            }
            boolean bot21 = false;
            for (AI bot : ai) {
                if (bot.getScore() == 21)
                    bot21 = true;
            }
//            System.out.printf("Hand: %s Value: %s \n", player, player.handValue());
//            if ((p == 21 && a1 == 21) || (p == 21 && a2 == 21) || (p == 21 && a3 == 21)
//                    || (a1 == 21 && a2 == 21) || (a1 == 21 && a3 == 21) || (a2 == 21 && a3 == 21))
//                System.out.println("Tie. Nobody wins");
//            else if (player.handValue() == 21 && !bot21) {
//                player.addWin();
////                System.out.println("You win!");
//                System.out.println("-----------");
//                System.out.printf("Wins: %d \n", player.getWins());
//                player.addScore(21);
//                break;
//            }

//            If tie bt bots, it says both bots win
            for (AI a : ai) {
                if (pcont || cont1 || cont2 || cont3)
                    break;
                else if (a.getScore() == 21)
                    System.out.printf("%s wins! \n", a.getName());
            }
//            String winner = "";
//            AI winner1 = new AI("");
//            for (AI a : ai) {
//                if (a.getScore() > player.handValue() && a.getScore() > winner1.getScore()) { // && a.getScore() > player1.handValue()
//                    winner = a.getName();
//                    winner1 = a;
//                }
//            }
            if (pcont && !cont1 && !cont2 && !cont3 && player.handValue() <= 21
                    && ai.get(0).getScore() < player.handValue() && ai.get(1).getScore() < player.handValue()
                    && ai.get(2).getScore() < player.handValue()) {
                System.out.println("You win!");
                player.addScore(1);
                break;
            }
            System.out.println("-----------");
        }
        if (player.handValue() <= 21 && player.handValue() > ai.get(0).getScore()
                && player.handValue() > ai.get(1).getScore() && player.handValue() > ai.get(2).getScore()) {
            System.out.println("You win!");
            player.addScore(1);
        }
        else if (p <= 21 && a1 > 21 && a2 > 21 && a3 > 21) {
            System.out.println("You win!");
            player.addScore(1);
        }
        else if (p > a1 && p > a2 && p > a3 && p <= 21) {
            System.out.println("You win!");
            player.addScore(1);
        }
        else if (((p == a1) && p > a2 && p > a3) || ((p == a2) && p > a1 && p > a3)
                || ((p == a3) && p > a1 && p > a2) || ((a1 == a2) && a1 > p && a1 > a3)
                || ((a1 == a3) && a1 > p && a1 > a2) || ((a2 == a3) && a2 > a1 && a2 > p)) {
            System.out.println("Tie. Nobody wins");
        }
        else if (p > 21) {
            System.out.println("Bust! You lose!");
        }
        else {
            System.out.println("You lose!");
        }
    }
    public void playGame() {
        Scanner s = new Scanner(System.in);
        boolean cont = true;
        while (cont) {
            Deck deck = new Deck();
            deck.shuffleDeck();
            for (AI a : ai) {
                a.resetValue();
                a.resetHand();
            }
            player.resetHand();
            playHand(deck, s);
            if (!player.keepPlaying(s))
                cont = false;
            else
                System.out.println("Score is now: " + player.getScore());
        }
    }
    public static void main(String[] args) {
        new Game().playGame();
    }
}
