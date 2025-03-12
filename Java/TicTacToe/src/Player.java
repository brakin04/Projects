import java.text.ParseException;
import java.util.Scanner;

public class Player {
    String name;
    Player(String Name) {
        this.name = Name;
    }
    public boolean playAgain() {
        Scanner s = new Scanner(System.in);
        System.out.println("Play again? y/n");
        while (true) {
            String input = s.nextLine();
            if (input.toLowerCase().contains("y")) {
                return true;
            } else if (input.toLowerCase().contains("n")) {
                return false;
            } System.out.println("Try again. y/n");
        }
    }
    public String[][] go(String team, Board b) {
        Scanner s = new Scanner(System.in);
        String[][] nb = b.getBoard();
        int play;
        System.out.println("Choose a play by entering the corresponding number");
        b.showBoard();
        b.showNumberBoard();
        while (true) {
            try {
                String input;
                while (true) {
                    input = s.nextLine();
                    play = Integer.parseInt(input);
                    if (play <= 8 && play >= 0)
                        break;
                    System.out.println("Type a number 0-8");
                }
                int i = play / 3;
                int j = play % 3;
                if (!nb[i][j].equals(" ")) {
                    System.out.println("You cannot play here");
                } else {
                    nb[i][j] = team;
                    break;
                }
            } catch (NumberFormatException e) {
                System.out.println("Type a number 0-8");
            }
        }
        return nb;
    }
}
