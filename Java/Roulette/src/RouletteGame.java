import java.util.Random;
import java.util.Scanner;
import static java.lang.Math.abs;

public class RouletteGame {

    private final Scanner s = new Scanner(System.in);
    private final Roulette roulette;

    RouletteGame() {
        this.roulette = new Roulette();
    }

    // This is the game
    public void play(Roulette r) {
        boolean cont = true;
        Random rand = new Random();
        // Loops while player wants to continue this round
        while (cont) {
            // Asks player to place bet
            r.placeBetOn();
            System.out.println("------------");
            // Decides random value (Spins the table)
            int k = rand.nextInt(0,38);
            int betOnSize = r.getBetOn().size();
            int sum = 0;
            int loss = 0;
            String color = "";
            // Loops for each bet
            for (int i = 0; i < betOnSize; i++) {
                // Sets what the bet was and how much was bet on it
                String betOn = r.getBetOn().get(i);
                int bet = r.getBetAmount().get(i);
                // Sets the value color
                if (k == 0 || k == 37)
                    color = "Green";
                else if (k % 2 == 0)
                    color = "Red";
                else
                    color = "Black";
                if (k == 37 && betOn.equals("00")) {
                    // Value and bet were 00
                    r.addCash(bet * 40);
                    sum += bet * 40;
                } else if (color.equals("Green") && (betOn.equals("G"))) {
                    // Value and bet were green
                    r.addCash(bet * 18);
                    sum += bet * 18;
                } else if (Integer.toString(k).equals(betOn)) {
                    // Value and bet were the same
                    r.addCash(bet * 36);
                    sum += bet * 36;
                } else if (k % 2 != 0 && betOn.equals("B")) {
                    // Both were black
                    r.addCash(bet * 2);
                    sum += bet * 2;
                } else if (k % 2 == 0 && betOn.equals("R")) {
                    // Both were red
                    r.addCash(bet * 2);
                    sum += bet * 2;
                } else if (k > 0 && k < 13 && betOn.equals("1-12")) {
                    // Bet and value were both first third
                    r.addCash(bet * 3);
                    sum += bet * 3;
                } else if (k > 12 && k < 25 && betOn.equals("13-24")) {
                    // Bet and value were both second third
                    r.addCash(bet * 3);
                    sum += bet * 3;
                } else if (k > 24 && k < 37 && betOn.equals("25-36")) {
                    // Bet and value were both final third
                    r.addCash(bet * 3);
                    sum += bet * 3;
                } else {
                    // Bet didn't land
                    loss += bet;
                }
                System.out.printf("You bet $%s on %s\n", bet, betOn);
            }
            // Displays what was spun and how much was made / lost
            System.out.printf("Value: %s Color: %s \n", k, color);
            System.out.printf("You lost $%s, and won $%s. You now have $%s \n", loss, sum, r.getCash());
            if (r.getCash() == 0) {
                // If out of cash, they're done
                cont = false;
                System.out.println("Out of money");
            } else if (!r.roll()) {
                // Asks if user wants to go again
                cont = false;
            }
            // Resets the bet arrays in roulette
            r.newBetAmount();
            r.newBetOn();
            System.out.println("------------");
        }
        // When done, determines if money was made or lost overall
        char sign;
        if (r.getCash() >= 200)
            sign = '+';
        else
            sign = '-';
        // Tells user final cash amount with gain / loss
        System.out.printf("You left with: $%s which is %s%s\n", r.getCash(), sign, (abs(r.getCash() - 200)));
    }

    public void playGame() {
        boolean cont = true;
        // Loops while the player wants to play a new game
        while (cont) {
            this.play(this.roulette);
            if (!this.roulette.keepPlaying()) {
                cont = false;
            }
        }
    }

    public static void main(String[] args) {
        new RouletteGame().playGame();
    }
}
