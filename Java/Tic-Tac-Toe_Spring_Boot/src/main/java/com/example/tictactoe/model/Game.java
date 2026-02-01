package com.example.tictactoe.model;

import com.example.tictactoe.controller.*;

import java.util.*;

import org.springframework.stereotype.Service;

// This is the model class for the game
@Service
public class Game {

    private Character[] board = new Character[9];
    private Character winner = ' ';

    public Game() {
        this.newBoard();
    }

    public void playerPlay(Character playerVal, int location) {
        if (this.board[location] == ' ') {
            this.board[location] = playerVal;
        }
//        System.out.println(Arrays.toString(this.board));
    }

    public void botPlay(Character playerVal, int difficulty) {
        char botVal = playerVal == 'X' ? 'O' : 'X';
        Bot bot = new Bot(this, botVal, difficulty);
        this.board[bot.botTurn()] = botVal;
    }

    // Checks if there are 3 in a row (winner)
    public Object[] threeInRow() {
        Object[] ans = new Object[2];
        ans[0] = false;
        // Diagonal
        if (board[4].equals(board[2]) && board[4].equals(board[6]) && !board[4].equals(' ')) {
            winner = board[4];
            ans[0] = true;
        } else if (board[4].equals(board[0]) && board[4].equals(board[8]) && !board[4].equals(' ')) {
            winner = board[4];
            ans[0] = true;
        }
        // Vertical
        else if (board[4].equals(board[1]) && board[4].equals(board[7]) && !board[4].equals(' ')) {
            winner = board[4];
            ans[0] = true;
        } else if (board[3].equals(board[0]) && board[3].equals(board[6]) && !board[3].equals(' ')) {
            winner = board[3];
            ans[0] = true;
        } else if (board[5].equals(board[2]) && board[5].equals(board[8]) && !board[5].equals(' ')) {
            winner = board[5];
            ans[0] = true;
        }
        // Horizontal
        else if (board[1].equals(board[0]) && board[1].equals(board[2]) && !board[1].equals(' ')) {
            winner = board[1];
            ans[0] = true;
        } else if (board[4].equals(board[3]) && board[4].equals(board[5]) && !board[4].equals(' ')) {
            winner = board[4];
            ans[0] = true;
        } else if (board[7].equals(board[6]) && board[7].equals(board[8]) && !board[7].equals(' ')) {
            winner = board[7];
            ans[0] = true;
        }
        // None
        ans[1] = winner;
        return ans;
    }

    public Character[] getBoard() {
        return board;
    }

    public Character getWinner() {
        return winner;
    }

    public void newBoard() {
        for (int i = 0; i < 9; i++) {
            this.board[i] = ' ';
        }
    }

    public void reset() {
        this.newBoard();
        this.winner = ' ';
    }
}

