import java.util.Scanner;
public class PlayGame {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        System.out.println("Would you like to play a bot or friend? Please type alone or friend. ");
        String input = s.nextLine();
        while (!input.equalsIgnoreCase("alone") && !input.equalsIgnoreCase("friend") ) {
            System.out.println("Please enter 'alone' or 'friend'.");
            input = s.nextLine();
        }
        new Game(input);
    }
}
