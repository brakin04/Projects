import java.util.HashMap;
import java.util.Scanner;

public class Game {

    private int wins;
    private int attempts;

    public Game() {
        wins = 0;
        attempts = 0;
    }

    /* 
        Takes inputs: word - the word to be guessed
                      wc - the WordChecker object to check if guesses are valid

        This function runs the game, allowing the user to input guesses and giving them feedback on them
        It returns nothing, but updates the wins and attempts variables based on the game outcome
    */
    public void play(String word, WordChecker wc) {
        this.attempts++;
        Scanner scanner = new Scanner(System.in);
        // colorTable holds the color value for the guesses
        String[][] colorTable = new String[5][5];
        // holds the letter value for each guess
        String[][] wordTable = new String[5][5];
        // holds the color value associated with each letter
        HashMap<String, Integer> keyboard = new HashMap<>();
        String[] alphabet = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"};
        // Adds each letter to the keyboard with -1 giving gray color
        for (String b : alphabet) {
            keyboard.putIfAbsent(b, -1);
        }
        // initializes each table spot as empty
        for (int l = 0; l < 5; l++) {
            for (int m = 0; m < 5; m++) {
                colorTable[l][m] = " ";
                wordTable[l][m] = " ";
            }
        }
        int attempt = 0;
        while (true) {
            // If they have done 5 tries, print the word and break
            if (attempt > 4) {
                System.out.print("\u001B[31m");
                System.out.print(word + "\n");
                System.out.print("\u001B[0m");
                break;
            }
            // theWord is a map that hold the number of times each letter appears in the word to be guessed
            HashMap<Character, Integer> theWord = new HashMap<>();
            // HashMap<Character, Integer> theGuess = new HashMap<>();
            System.out.println("Enter your guess: ");
            String input = scanner.nextLine().toLowerCase();
            while (true) {
                if (input.length() != 5) {
                    // Makes sure word has len 5
                    System.out.println("Enter a 5 character word: ");
                    input = scanner.nextLine().toLowerCase().strip();
                } else if (!wc.checkWord(input)) {
                    // Checks it against dictionary
                    System.out.println("Not a valid word. Try again: ");
                    input = scanner.nextLine().toLowerCase().strip();
                } else {
                    break;
                }
            }
            // record the number of times each letter appears in the word
            for (int r = 0; r < 5; r++) {
                char letter = word.charAt(r);
                if (!theWord.containsKey(letter)) {
                    theWord.put(letter,1);
                } else {
                    int oldVal = theWord.get(letter);
                    theWord.replace(letter, oldVal+1);
                }
            }
            int correct = 0;
            // for each letter
            for (int i = 0; i < 5; i++) {
                // check if the word contains it
                String letter = input.substring(i, i+1);
                boolean hasLetter = word.contains(letter);
                char charLetter = letter.charAt(0);
                int theVal2;
                if (hasLetter && input.charAt(i) == word.charAt(i)) {
                    // if it does, and they're at the same index, make its color in table green
                    keyboard.put(letter, 1);
                    theVal2 = theWord.get(charLetter);
                    if (theVal2 > 0) {
                        theWord.replace(charLetter, theVal2-1);
                        colorTable[attempt][i] = "G";
                        correct++;
                    }
                } else if (hasLetter) {
                    // if it has the letter, but it's not in the right spot make it yellow
                    keyboard.put(letter, 0);
                    theVal2 = theWord.get(charLetter);
                    if (theVal2 > 0) {
                        theWord.replace(charLetter, theVal2-1);
                        colorTable[attempt][i] = "Y";
                    }
                } else {
                    // if it doesn't contain it, add the letter to keyboard with color red
                    keyboard.put(letter, 2);
                }
                // add the letter to the appropriate spot in the word table
                wordTable[attempt][i] = letter;
            }
            // print out the board
            if (correct == 5) {
                printBoard(colorTable, wordTable);
                System.out.printf("You got it in %s tries!\n", attempt + 1);
                this.wins++;
                break;
            }
            printBoard(colorTable, wordTable);
            // below shows the alphabet (qw breaks it halfway through)
            int qw = 0;
            for (String s : alphabet) {
                if (qw == 13) {
                    System.out.println();
                }
                // -1 is gray, 0 is yellow, 1 is green, 2 is red
                switch (keyboard.get(s)) {
                    case -1 -> System.out.print("\u001B[0m");
                    case 0 -> System.out.print("\u001B[33m");
                    case 1 -> System.out.print("\u001B[32m");
                    case 2 -> System.out.print("\u001B[31m");
                }
                System.out.print("[" + s + "]");
                qw++;
            }
            System.out.println("\n");
            attempt++;
        }
        scanner.close();
    }

    // Asks if user wants to play again
    public boolean playAgain() {
        Scanner s = new Scanner(System.in);
        System.out.println("Play again? Y/n");
        String input = s.nextLine().toLowerCase();
        while (true) {
            if (input.equals("y")) {
                s.close();
                return true;
            } else if (input.equals("n")) {
                s.close();
                return false;
            } else {
                System.out.println("Try again. type Y or n");
                input = s.nextLine().toLowerCase();
            }
        }
    }

    // This function prints the board based on the color and word tables
    public void printBoard(String[][] colorTable, String[][] wordTable) {
        for (int i = 0; i < 5; i++) {
            System.out.print("            ");
            for (int j = 0; j < 5; j++) {
                // Looks at each spot and prints appropriate color
                if (colorTable[i][j].equals("G")) {
                    System.out.print("\u001B[32m");
                } else if (colorTable[i][j].equals("Y")) {
                    System.out.print("\u001B[33m");
                }
                System.out.print("[" + wordTable[i][j] + "]");
                System.out.print("\u001B[0m");
            }
            System.out.println();
        }
        System.out.println();
    }

    public void showGameStats() {
        System.out.printf("Wins: %d\n", wins);
        System.out.printf("Attempts: %d\n", attempts);
    }
}
