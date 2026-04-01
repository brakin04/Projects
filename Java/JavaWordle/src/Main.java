import java.util.Random;

public class Main {
    public static void main(String[] args) {
        WordChecker wc = new WordChecker();
        Random number = new Random();
        Game game = new Game();
        do {
            int value = number.nextInt(wc.getDict().size());
            game.play(wc.getDict().get(value), wc);
        } while (game.playAgain());
        game.showGameStats();
    }
}