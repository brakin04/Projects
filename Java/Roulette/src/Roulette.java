import java.util.ArrayList;
import java.util.Scanner;

public class Roulette {

    private int cash;
    private ArrayList<Integer> betAmount;
    private ArrayList<String> betOn;
    private final Scanner s = new Scanner(System.in);

    Roulette() {
        this.betAmount = new ArrayList<>();
        this.betOn = new ArrayList<>();
        this.cash = 200;
    }

    // Asks user if they want to place another bet
    public boolean anotherBet() {
        System.out.println("Place another bet? [y/n]");
        String input = this.s.nextLine();
        while (true) {
            if (input.equals("y") || input.equals("Y")) {
                return true;
            } else if (input.equals("n") || input.equals("N")) {
                return false;
            } else {
                System.out.println("Place another bet? Type 'y' or 'n'");
                input = this.s.nextLine();
            }
        }
    }

    // Asks user what they want to place a bet on
    public void placeBetOn() {
        System.out.println("Bet on Black (B) / Red (R) / Green (G), 00, \n A Specific number, 1-12, 13-24, or 25-36:");
        String input;
        boolean invalid = true;
        // Loops until the input is valid
        while (invalid) {
            input = this.s.nextLine();
            // Checks for a number input
            for (int i = 1; i <= 36; i++) {
                if (input.equals(Integer.toString(i))) {
                    System.out.printf("Input: %s \n", i);
                    this.betOn.add(Integer.toString(i));
                    invalid = false;
                    break;
                }
            }
            // Checks for a color / range / double 0 input
            switch (input) {
                case "B", "b" -> {
                    System.out.println("Input: Black");
                    this.betOn.add("B");
                    invalid = false;
                }
                case "R", "r" -> {
                    System.out.println("Input: Red");
                    this.betOn.add("R");
                    invalid = false;
                }
                case "G", "g" -> {
                    System.out.println("Input: Green");
                    this.betOn.add("G");
                    invalid = false;
                }
                case "00" -> {
                    System.out.println("Input: 00");
                    this.betOn.add("00");
                    invalid = false;
                }
                case "1-12" -> {
                    System.out.println("Input: 1-12");
                    this.betOn.add("1-12");
                    invalid = false;
                }
                case "13-24" -> {
                    System.out.println("Input: 13-24");
                    this.betOn.add("13-24");
                    invalid = false;
                }
                case "25-36" -> {
                    System.out.println("Input: 25-36");
                    this.betOn.add("25-36");
                    invalid = false;
                }
                default -> {
                    System.out.println("Try again");
                }
            }
        }
        // Has player place their bet amount
        this.placeMoneyBet();
        if (this.cash <= 0) {
            // Cash is out
            System.out.println("You have no money left to bet this round");
        } else if (this.anotherBet()) {
            // Asks if they want another bet
            this.placeBetOn();
        }
    }

    // Asks user how much they want to bet
    public void placeMoneyBet() {
        int amount;
        System.out.printf("Place a bet amount\nYou have $%s: ", this.cash);
        String input = this.s.nextLine();
        // Try to cast to int until it works
        while (true) {
            try {
                amount = Integer.parseInt(input);
                break;
            } catch (NumberFormatException e) {
                System.out.println("Enter a number: ");
                input = this.s.nextLine();
            }
        }
        if (amount > this.cash) {
            // The value was more than they had
            System.out.println("This is too large a bet.");
            this.placeMoneyBet();
        } else if (amount < 0) {
            System.out.println("You can't bet a negative number.");
            this.placeMoneyBet();
        } else if (amount % 5 != 0) {
            System.out.println("Increments of 5 only");
            this.placeMoneyBet();
        } else {
            this.betAmount.add(amount);
            this.cash -= amount;
        }
    }

    // Asks player if they want to go another round or leave
    public boolean roll() {
        if (cash <= 0) {
            // Player cant go if out of cash
            return false;
        }
        System.out.println("Go again? [y/n]");
        String input = this.s.nextLine();
        while (true) {
            if (input.equals("y") || input.equals("Y")) {
                return true;
            } else if (input.equals("n") || input.equals("N")) {
                return false;
            } else {
                System.out.println("Go again? Type 'y' or 'n'");
                input = this.s.nextLine();
            }
        }
    }

    // Asks player if they want to play another game
    public boolean keepPlaying() {
        System.out.println("Play again? [y/n]: ");
        String input = this.s.nextLine();
        while (true) {
            if (input.equals("y") || input.equals("Y")) {
                // Resets cash to 200
                this.cash = 200;
                return true;
            } else if (input.equals("n") || input.equals("N")) {
                return false;
            } else {
                System.out.println("Play again? Type 'y' or 'n': ");
                input = this.s.nextLine();
            }
        }
    }

    // Getter and initialization methods
    public ArrayList<Integer> getBetAmount() {
        return this.betAmount;
    }
    public void newBetAmount() {
        this.betAmount = new ArrayList<>();
    }
    public ArrayList<String> getBetOn() {
        return this.betOn;
    }
    public void newBetOn() {
        this.betOn = new ArrayList<>();
    }
    public int getCash() {
        return this.cash;
    }
    public void addCash(int amount) {
        this.cash += amount;
    }
}

