import java.util.HashMap;
import java.util.Random;
import java.util.Scanner;

public class Main {
    public static void play(String word, WordChecker wc) {
        Scanner scanner = new Scanner(System.in);
        // table holds the color value for the guesses
        String[][] table = new String[5][5];
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
                table[l][m] = " ";
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
            // theWord is ... and theGuess is ...
            HashMap<Character, Integer> theWord = new HashMap<>();
            HashMap<Character, Integer> theGuess = new HashMap<>();
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
            // for each letter
            for (int r = 0; r < 5; r++) {
                // if theGuess doesn't contain this letter as a key, add it, if it does inc value by 1
                char l1 = input.charAt(r);
                if (!theGuess.containsKey(l1)) {
                    theGuess.put(l1, 1);
                } else {
                    int oldVal = theGuess.get(l1);
                    theGuess.replace(l1, oldVal+1);
                }
                // If the word doesn't contain the char as a key, add it, if it does inc value by 1
                char l2 = word.charAt(r);
                if (!theWord.containsKey(l2)) {
                    theWord.put(l2,1);
                } else {
                    int oldVal = theWord.get(l2);
                    theWord.replace(l2, oldVal+1);
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
                        table[attempt][i] = "G";
                        correct++;
                    }
                } else if (hasLetter) {
                    // if it has the letter, but it's not in the right spot make it yellow
                    keyboard.put(letter, 0);
                    theVal2 = theWord.get(charLetter);
                    if (theVal2 > 0) {
                        theWord.replace(charLetter, theVal2-1);
                        table[attempt][i] = "Y";
                    }
                } else {
                    // if it doesn't contain it, add the letter to keyboard with color red
                    keyboard.put(letter, 2);
                }
                // add the letter to the appropriate spot in the word table
                wordTable[attempt][i] = letter;
            }
            // below prints out board if player won
            if (correct == 5) {
                for (int q = 0; q <= attempt; q++) {
                    for (int p = 0; p < 5; p++) {
                        // changes color based on table info
                        if (q == attempt || table[q][p].equals("G")) {
                            System.out.print("\u001B[32m");
                        } else if (table[q][p].equals("Y")) {
                            System.out.print("\u001B[33m");
                        }
                        System.out.print("[" + wordTable[q][p] + "]");
                        System.out.print("\u001B[0m");
                    }
                    System.out.println();
                }
                System.out.print("\u001B[0m");
                System.out.printf("You got it in %s tries!\n", attempt + 1);
                break;
            }
            // below prints out the board
            for (int j = 0; j < 5; j++) {
                for (int k = 0; k < 5; k++) {
                    // Looks at each spot and prints appropriate color
                    if (table[j][k].equals("Y")) {
                        System.out.print("\u001B[33m");
                    } else if (table[j][k].equals("G")) {
                        System.out.print("\u001B[32m");
                    }
                    System.out.print("[" + wordTable[j][k] + "]");
                    System.out.print("\u001B[0m");
                }
                System.out.println();
            }
            // below shows the alphabet (qw breaks it halfway through)
            int qw = 0;
            for (String s : alphabet) {
                if (qw == 13) {
                    System.out.println();
                }
                // -1 is gray, 0 is yellow, 1 is green, 2 is red
                if (keyboard.get(s) == -1) {
                    System.out.print("\u001B[0m");
                } else if (keyboard.get(s) == 0) {
                    System.out.print("\u001B[33m");
                } else if (keyboard.get(s) == 1) {
                    System.out.print("\u001B[32m");
                } else if (keyboard.get(s) == 2) {
                    System.out.print("\u001B[31m");
                }
                System.out.print("[" + s + "]");
                qw++;
            }
            System.out.println();
            attempt++;
        }

    }

    // Asks if user wants to play again
    public static boolean playAgain() {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Play again? Y/n");
        String input = scanner.nextLine().toLowerCase();
        while (true) {
            if (input.equals("y")) {
                return true;
            } else if (input.equals("n")) {
                return false;
            } else {
                System.out.println("Try again. type Y or n");
                input = scanner.nextLine().toLowerCase();
            }
        }
    }
    public static void main(String[] args) {
        WordChecker wc = new WordChecker();
        Random number = new Random();
        do {
            int value = number.nextInt(wc.getDict().size());
            play(wc.getDict().get(value), wc);
        } while (playAgain());
    }
}