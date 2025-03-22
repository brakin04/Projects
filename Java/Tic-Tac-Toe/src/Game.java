import java.util.Arrays;
import java.util.Scanner;

// This is the model class for the game
public class Game {

    Scanner s = new Scanner(System.in);
    private Character[] board = new Character[9];
    private Character winner = ' ';

    public Game(String type) {
        this.newBoard();
        if (type.equals("alone")) {
            soloGame();
        } else {
            friendGame();
        }
    }

    public void soloGame() {
        // initialize the player and bot
        Player player = new Player(this);
        System.out.println("What difficulty would you like to play? 1-3");
        String input = s.nextLine();
        while (!input.equals("1") && !input.equals("2") && !input.equals("3")) {
            System.out.println("Please enter a number between 1 and 3");
            input = s.nextLine();
        }
        int diff = Integer.parseInt(input);
        Bot bot;
        if (player.value.equals('X')) {
            bot = new Bot(this, 'O', diff);
        } else {
            bot = new Bot(this, 'X', diff);
        }

        // play the game
        int turn = 0;
        while (Arrays.stream(board).toList().contains(' ')) {
            if (turn % 2 == 0) {
                if (player.value.equals('X')) {
                    board[player.playerTurn()] = 'X';
                } else {
                    board[bot.botTurn()] = 'X';
                }
            } else {
                if (player.value.equals('O')) {
                    board[player.playerTurn()] = 'O';
                } else {
                    board[bot.botTurn()] = 'O';
                }
            }
            // Check for win
            if (this.threeInRow()) {
                break;
            }
            turn++;
        }
        // If winner is still default, Tie else print winner
        if (winner.equals(' ')) {
            System.out.println("Tie Game!");
        } else {
            System.out.println("The winner is " + winner);
        }
        // If play again, start new solo game
        if (this.playAgain()) {
            this.newBoard();
            this.winner = ' ';
            this.soloGame();
        }
    }

    public void friendGame() {
        // Initialize players
        Player player1 = new Player(this);
        Player player2;
        if (player1.value.equals('X')) {
            player2 = new Player(this,'O');
        } else {
            player2 = new Player(this,'X');
        }

        // play the game
        int turn = 0;
        while (Arrays.stream(board).toList().contains(' ')) {
            if (turn % 2 == 0) {
                if (player1.value.equals('X')) {
                    this.board[player1.playerTurn()] = 'X';
                } else {
                    this.board[player2.playerTurn()] = 'X';
                }
            } else {
                if (player1.value.equals('O')) {
                    this.board[player1.playerTurn()] = 'O';
                } else {
                    this.board[player2.playerTurn()] = 'O';
                }
            }
            // Check for win
            if (this.threeInRow()) {
                break;
            }
            turn++;
        }
        // If winner is still default value, Tie else print winner
        if (winner.equals(' ')) {
            System.out.println("Cat's Game!");
        } else {
            System.out.println("The winner is " + winner);
        }
        // If play again, start new Friend Game
        if (this.playAgain()) {
            this.newBoard();
            this.winner = ' ';
            this.friendGame();
        }
    }

    // Checks if there are 3 in a row (winner)
    public boolean threeInRow() {
        // Diagonal
        if (board[4].equals(board[2]) && board[4].equals(board[6]) && !board[4].equals(' ')) {
            winner = board[4]; return true;
        } else if (board[4].equals(board[0]) && board[4].equals(board[8]) && !board[4].equals(' ')) {
            winner = board[4]; return true;
        }
        // Vertical
        else if (board[4].equals(board[1]) && board[4].equals(board[7]) && !board[4].equals(' ')) {
            winner = board[4]; return true;
        } else if (board[3].equals(board[0]) && board[3].equals(board[6]) && !board[3].equals(' ')) {
            winner = board[3]; return true;
        } else if (board[5].equals(board[2]) && board[5].equals(board[8]) && !board[5].equals(' ')) {
            winner = board[5]; return true;
        }
        // Horizontal
        else if (board[1].equals(board[0]) && board[1].equals(board[2]) && !board[1].equals(' ')) {
            winner = board[1]; return true;
        } else if (board[4].equals(board[3]) && board[4].equals(board[5]) && !board[4].equals(' ')) {
            winner = board[4]; return true;
        } else if (board[7].equals(board[6]) && board[7].equals(board[8]) && !board[7].equals(' ')) {
            winner = board[7]; return true;
        }
        // None
        else { return false; }
    }

    public boolean playAgain() {
        System.out.println("Would you like to play the same game again? Y/n");
        String input = s.nextLine();
        while (!input.equalsIgnoreCase("y") && !input.equalsIgnoreCase("n")) {
            System.out.println("Please enter either Y for yes or N for no");
            input = s.nextLine();
        }
        return input.equalsIgnoreCase("y");
    }

    public Character[] getBoard() {
        return board;
    }
    // 1 | 2 | 3
    //-----------
    // 4 | 5 | 6
    //-----------
    // 7 | 8 | 9
    public void printBoard() {
        for (int i = 0; i < 9; i++) {
            if (i == 0) {
                System.out.print(" " + this.board[i]);
            } else if (i % 3 == 0) {
                System.out.printf("    %s | %s | %s \n-----------   -----------\n " + this.board[i], i-2, i-1, i);
            } else if (i % 3 == 2) {
                System.out.print(this.board[i] + " ");
            } else {
                System.out.print(" | " + this.board[i] + " | ");
            } if (i == 8) {
                System.out.println("    7 | 8 | 9 ");
            }
        }
    }

    public void newBoard() {
        for (int i = 0; i < 9; i++) {
            this.board[i] = ' ';
        }
    }
}
