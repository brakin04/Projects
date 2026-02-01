package com.example.tictactoe.controller;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import com.example.tictactoe.model.Game;
import org.springframework.stereotype.Service;

@Service
public class Bot {

    int difficulty;
    Game game;
    Character value;
    List<Integer> corners = List.of(0, 2, 6, 8);

    public Bot(Game game, Character value, int Difficulty) {
        this.game = game;
        this.value = value;
        this.difficulty = Difficulty;
    }

    public Bot() {

    }

    // Decides which spot bot plays
    public int botTurn() {
        // initialize valid spots
        List<Integer> valid = new ArrayList<>();
        for (int i = 0; i < 9; i++) {
            if (this.game.getBoard()[i].equals(' ')) {
                valid.add(i);
            }
        }

        // if there's only one valid spot, return it
        if (valid.size() == 1) { return valid.get(0); }

        // Uses appropriate method for difficulty
        return switch (this.difficulty) {
            case 1 -> this.easy(valid);
            case 2 -> this.medium(valid);
            case 3 -> this.hard(valid);
            default -> -1;
        };
    }

    public int easy(List<Integer> valid) {
        Random rand = new Random();

        // looks for defense and win
        int play = this.winOrBlock(valid);
        if (play != -1) {
            // 80% chance it defends / wins if it can
            if (rand.nextInt(0,10) < 8) { return play; }
        }
        // chooses random open spot if didn't defend or win
        return valid.get(rand.nextInt(0, valid.size()));
    }

    public int medium(List<Integer> valid) {
        // look for win & defense
        int play = this.winOrBlock(valid);
        if (play != -1) {
            return play;
        }

        // Tries middle
        if (valid.contains(4)) { return 4; }

        // Tries corner spots
        for (int c : corners) {
            if (valid.contains(c)) { return c; }
        }

        // Returns random open spot
        Random rand = new Random();
        return valid.get(rand.nextInt(0, valid.size()));
    }

    public int hard(List<Integer> valid) {
        Random rand = new Random();

        // look for win & defense
        int play = this.winOrBlock(valid);
        if (play != -1) {
            return play;
        }

        // sets opponent's value
        char opp;
        if (this.value.equals('X')) {
            opp = 'O';
        } else {
            opp = 'X';
        }

        // make it 50 50 between going opposite corner and how it does to block the corner trap
        // block corner trap
        if (this.game.getBoard()[0].equals(opp) || this.game.getBoard()[8].equals(opp) ||
                this.game.getBoard()[2].equals(opp) || this.game.getBoard()[6].equals(opp)) {
            // does opposite corner half the time if it can
            if (rand.nextBoolean()) {
                if (this.game.getBoard()[0].equals(opp) && valid.contains(8)) {
                    return 8;
                } else if (this.game.getBoard()[2].equals(opp) && valid.contains(6)) {
                    return 6;
                } else if (this.game.getBoard()[6].equals(opp) && valid.contains(2)) {
                    return 2;
                } else if (this.game.getBoard()[8].equals(opp) && valid.contains(0)) {
                    return 0;
                }
            }
            // try a random middle-edge play if available
            ArrayList<Integer> plays = new ArrayList<>(List.of(1, 3, 5, 7));
            while (!plays.isEmpty()) {
                int i = rand.nextInt(0, plays.size());
                if (valid.contains(plays.get(i))) {
                    return plays.get(i);
                }
                plays.remove(i);
            }
        }

        // Tries middle
        if (valid.contains(4)) { return 4; }

        // Tries to trap with corners
        if (valid.contains(2) && this.game.getBoard()[0].equals(value) && this.game.getBoard()[8].equals(value)) { return 2; }
        if (valid.contains(0) && this.game.getBoard()[2].equals(value) && this.game.getBoard()[6].equals(value)) { return 0; }
        if (valid.contains(6) && this.game.getBoard()[0].equals(value) && this.game.getBoard()[8].equals(value)) { return 6; }
        if (valid.contains(8) && this.game.getBoard()[6].equals(value) && this.game.getBoard()[2].equals(value)) { return 8; }

        // Tries to set up trap
        if (valid.contains(0) && valid.contains(8) && (valid.contains(2) || valid.contains(6))) { return 0; }
        if (valid.contains(2) && valid.contains(6) && (valid.contains(0) || valid.contains(8))) { return 2; }

        // Try random corner
        for (int c : corners) {
            if (valid.contains(c)) { return c; }
        }

        // If none are open, return random spot
        return valid.get(rand.nextInt(0,valid.size()));
    }


    public int winOrBlock(List<Integer> valid) {
        char opp;
        if (this.value.equals('X')) {
            opp = 'O';
        } else {
            opp = 'X';
        }
        for (char c : new Character[]{this.value, opp}) {
            // Horizontal
            if (this.game.getBoard()[0].equals(c) && this.game.getBoard()[1].equals(c) && valid.contains(2)) {
                return 2;
            }
            if (this.game.getBoard()[0].equals(c) && this.game.getBoard()[2].equals(c) && valid.contains(1)) {
                return 1;
            }
            if (this.game.getBoard()[1].equals(c) && this.game.getBoard()[2].equals(c) && valid.contains(0)) {
                return 0;
            }

            if (this.game.getBoard()[3].equals(c) && this.game.getBoard()[4].equals(c) && valid.contains(5)) {
                return 5;
            }
            if (this.game.getBoard()[3].equals(c) && this.game.getBoard()[5].equals(c) && valid.contains(4)) {
                return 4;
            }
            if (this.game.getBoard()[4].equals(c) && this.game.getBoard()[5].equals(c) && valid.contains(3)) {
                return 3;
            }

            if (this.game.getBoard()[6].equals(c) && this.game.getBoard()[7].equals(c) && valid.contains(8)) {
                return 8;
            }
            if (this.game.getBoard()[6].equals(c) && this.game.getBoard()[8].equals(c) && valid.contains(7)) {
                return 7;
            }
            if (this.game.getBoard()[7].equals(c) && this.game.getBoard()[8].equals(c) && valid.contains(6)) {
                return 6;
            }

            // Vertical
            if (this.game.getBoard()[0].equals(c) && this.game.getBoard()[3].equals(c) && valid.contains(6)) {
                return 6;
            }
            if (this.game.getBoard()[0].equals(c) && this.game.getBoard()[6].equals(c) && valid.contains(3)) {
                return 3;
            }
            if (this.game.getBoard()[3].equals(c) && this.game.getBoard()[6].equals(c) && valid.contains(0)) {
                return 0;
            }

            if (this.game.getBoard()[1].equals(c) && this.game.getBoard()[4].equals(c) && valid.contains(7)) {
                return 7;
            }
            if (this.game.getBoard()[1].equals(c) && this.game.getBoard()[7].equals(c) && valid.contains(4)) {
                return 4;
            }
            if (this.game.getBoard()[4].equals(c) && this.game.getBoard()[7].equals(c) && valid.contains(1)) {
                return 1;
            }

            if (this.game.getBoard()[2].equals(c) && this.game.getBoard()[5].equals(c) && valid.contains(8)) {
                return 8;
            }
            if (this.game.getBoard()[2].equals(c) && this.game.getBoard()[8].equals(c) && valid.contains(5)) {
                return 5;
            }
            if (this.game.getBoard()[5].equals(c) && this.game.getBoard()[8].equals(c) && valid.contains(2)) {
                return 2;
            }

            // Diagonal
            if (this.game.getBoard()[2].equals(c) && this.game.getBoard()[4].equals(c) && valid.contains(6)) {
                return 6;
            }
            if (this.game.getBoard()[2].equals(c) && this.game.getBoard()[6].equals(c) && valid.contains(4)) {
                return 4;
            }
            if (this.game.getBoard()[4].equals(c) && this.game.getBoard()[6].equals(c) && valid.contains(2)) {
                return 2;
            }

            if (this.game.getBoard()[0].equals(c) && this.game.getBoard()[4].equals(c) && valid.contains(8)) {
                return 8;
            }
            if (this.game.getBoard()[0].equals(c) && this.game.getBoard()[8].equals(c) && valid.contains(4)) {
                return 4;
            }
            if (this.game.getBoard()[4].equals(c) && this.game.getBoard()[8].equals(c) && valid.contains(0)) {
                return 0;
            }
        }
        // None will defend
        return -1;
    }

}
