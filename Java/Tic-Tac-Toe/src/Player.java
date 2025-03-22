import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Player {

    Scanner s = new Scanner(System.in);
    Game game;
    Character value;

    public Player(Game game) {
        this.game = game;
        // determines X and O
        System.out.println("Would you like to be X or O?");
        String input = s.nextLine();
        while (!input.equalsIgnoreCase("X") && !input.equalsIgnoreCase("O")) {
            System.out.println("Please enter either 'X' or 'O'.");
            input = s.nextLine();
        }
        if (input.equalsIgnoreCase("X")) {
            value = 'X';
        } else {
            value = 'O';
        }
    }

    public Player(Game game, Character value) {
        this.game = game;
        this.value = value;
    }

    public int playerTurn() {
        this.game.printBoard();
        // make list of valid plays and print them
        List<Integer> valid = new ArrayList<>();
        for (int i = 0; i < 9; i++) {
            if (this.game.getBoard()[i].equals(' ')) {
                valid.add(i + 1);
            }
        }
        System.out.print("You can play: ");
        String validPlays = "";
        for (Integer i : valid) {
            validPlays += i + ", ";
        }
        System.out.println(validPlays.substring(0, validPlays.length() - 2));

        // Asks where player would like to play
        System.out.println("\nWhere would you like to go? You are: " + this.value);
        String input = s.nextLine();
        int inputNum;
        // Loops while it's not a valid input
        while (true) {
            try {
                // Tries to cast input to an int and checks if it's an open spot
                inputNum = Integer.parseInt(input);
                if (valid.contains(inputNum)) {
                    break;
                }
                System.out.println("Please enter the number of an open space");
                input = s.nextLine();
            } catch (NumberFormatException e) {
                // Makes player re-enter if input couldn't cast to a number
                System.out.println("Please enter a number");
                input = s.nextLine();
            }
        }
        return inputNum - 1;
    }
}
