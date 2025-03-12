import java.util.HashMap;
import java.util.Random;
import java.util.Scanner;

public class Main {
    public static void play(String word) {
        Scanner scanner = new Scanner(System.in);
        String[][] table = new String[5][5];
        String[][] wordTable = new String[5][5];
        HashMap<String, Integer> keyboard = new HashMap<>();
        String[] alphabet = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"};
        for (String b : alphabet) {
            keyboard.putIfAbsent(b, -1);
        }
//        System.out.println("Keyboard: " + keyboard);
        for (int l = 0; l < 5; l++) {
            for (int m = 0; m < 5; m++) {
                table[l][m] = " ";
                wordTable[l][m] = " ";
            }
        }
        int attempt = 0;
        while (true) {
            if (attempt > 4) {
                System.out.print("\u001B[31m");
                System.out.print(word + "\n");
                System.out.print("\u001B[0m");
                break;
            }
            HashMap<String, Integer> theWord = new HashMap<>();
            HashMap<String, Integer> theGuess = new HashMap<>();
            System.out.println("Enter your guess");
            String input = scanner.nextLine().toLowerCase();
            while (input.length() != 5) {
                System.out.println("Enter a 5 character word");
                input = scanner.nextLine();
            }
            for (int r = 0; r < 5; r++) {
                String lette = input.substring(r, r + 1);
                if (!theGuess.containsKey(lette)) {
                    theGuess.put(lette, 1);
                } else {
                    int oldVal = theGuess.get(lette);
                    theGuess.replace(lette, oldVal+1);
                }
                String lett = word.substring(r,r+1);
                if (!theWord.containsKey(lett)) {
                    theWord.put(lett,1);
                } else {
                    int oldVal = theWord.get(lett);
                    theWord.replace(lett, oldVal+1);
                }
            }
            int correct = 0;
            for (int i = 0; i < 5; i++) {
                String letter = input.substring(i, i + 1);
                int theVal2;
                boolean hasLetter = word.contains(letter);
                if (hasLetter && input.charAt(i) == word.charAt(i)) {
                    keyboard.put(letter, 1);
                    theVal2 = theWord.get(letter);
                    if (theVal2 > 0) {
                        theWord.replace(letter, theVal2-1);
                        table[attempt][i] = "G";
                        correct++;
                    }
                } else if (hasLetter) {
                    keyboard.put(letter, 0);
                    theVal2 = theWord.get(letter);
                    if (theVal2 > 0) {
                        theWord.replace(letter, theVal2-1);
                        table[attempt][i] = "Y";
                    }
                } else {
                    keyboard.put(letter, 2);
                }
                wordTable[attempt][i] = letter;
            }
//            below prints out board if player won
            if (correct == 5) {
                for (int q = 0; q <= attempt; q++) {
                    for (int p = 0; p < 5; p++) {
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
//            below prints out the board
            for (int j = 0; j < 5; j++) {
                for (int k = 0; k < 5; k++) {
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
//            below shows the alphabet
            int qw = 0;
            for (String s : alphabet) {
                if (qw == 13) {
                    System.out.println();
                }
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
    public static boolean playAgain() {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Play again? Y/n");
        String input = scanner.nextLine().toLowerCase();
        while (!input.equals("y") && !input.equals("n")) {
            System.out.println("Try again. type Y or n");
            input = scanner.nextLine().toLowerCase();
        }
        if (input.equals("y"))
            return true;
        return false;
    }
    public static void main(String[] args) {
        String[] wordList = {"apple","seats","drive", "grave", "plots", "space", "break", "build", "files", "flies",
                "tried", "tries", "sloth", "cloth", "plays", "place", "exits", "words", "slate", "voids", "views", "helps",
                "calls", "super", "taste", "solar", "lunar", "timed", "timid", "wrath", "guild", "splay", "drill", "sells",
                "potts", "value", "boast", "waste", "paste", "light", "heavy", "drags", "putty", "extra", "eagle", "fuzzy",
                "pizza", "crazy", "quake", "chalk", "hippo", "fluffy", "hazel", "juicy", "joked", "judge", "jokes", "whiff",
                "zesty", "blaze", "check", "chuck", "fjord", "jerks", "kayak", "kinky", "maize", "puffy", "which", "witch",
                "waxes", "waxed", "boxed", "ducks", "foxes", "graze", "glaze", "hawks", "happy", "spook", "jolly", "knick"};
        Random number = new Random();
        do {
            int value = number.nextInt(wordList.length);
            play(wordList[value]);
        } while (playAgain());
    }
}