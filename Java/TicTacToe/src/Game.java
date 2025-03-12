import java.util.ArrayList;
import java.util.Scanner;

public class Game {
    static Player player;
    static Bot bot;
    static Board board;
    private
    Game() {
        player = new Player("John");
        bot = new Bot(1);
        board = new Board();
    }
    public static void playGame(Game game) {
        Scanner s = new Scanner(System.in);
        System.out.println("Choose: X or O");
        boolean playerIsX;
        while (true) {
            String input = s.nextLine();
            if (input.toLowerCase().contains("x")) {
                playerIsX = true;
                break;
            } else if (input.toLowerCase().contains("o")) {
                playerIsX = false;
                break;
            }
            System.out.println("Try again, Choose X or O");
        }
        int count = 1;
        while (true) {
            if (playerIsX) {
                board = new Board(player.go("X", board));
                if (board.threeInRow()) {
                    System.out.println("\n");
                    board.showBoard();
                    System.out.println("X's win!");
                    break;
                } else if (count == 5) {
                    System.out.println("\n");
                    board.showBoard();
                    System.out.println("Cat's game");
                    break;
                }
                board = new Board(bot.go("O", board));
            } else {
                board = new Board(bot.go("X", board));
                if (board.threeInRow()) {
                    System.out.println("\n");
                    board.showBoard();
                    System.out.println("X's win!");
                    break;
                } else if (count == 5) {
                    System.out.println("\n");
                    board.showBoard();
                    System.out.println("Cat's game");
                    break;
                }
                board = new Board(player.go("O", board));
            }
            if (board.threeInRow()) {
                System.out.println("\n");
                board.showBoard();
                System.out.println("O's win!");
                break;
            }
            count++;
        }
        if (player.playAgain()) {
            playGame(new Game());
        }
    }

    public static void main(String[] args) {
        playGame(new Game());
    }
}
