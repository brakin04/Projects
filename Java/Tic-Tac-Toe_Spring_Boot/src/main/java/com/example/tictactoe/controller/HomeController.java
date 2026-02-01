package com.example.tictactoe.controller;

import com.example.tictactoe.model.Game;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class HomeController {

    @Autowired
    private Game game = new Game();

    private String name = "";
    private String type = "";
    private int botDiff = 0;
    private Character playerVal = ' ';
    int playNumber = 0;


    @GetMapping("/")
    public String home() {
        this.playNumber = 0;
        this.reset();
        return "start"; // Maps to start.html
    }

    @GetMapping("/playGame")
    public String game(Model model) {
        model.addAttribute("name", name);
        model.addAttribute("type", type);
        model.addAttribute("botDiff", botDiff);
        model.addAttribute("playerVal", playerVal);
        model.addAttribute("board", game.getBoard());
        // checks for unassigned values
        if (type.isEmpty() || playerVal.equals(' ') || botDiff == 0) {
            model.addAttribute("mode", "none");
            model.addAttribute("message", "Please make sure you make a selection for each value");
            return "gameSetup";
        }
        // checks for win. if not, bot plays if it needs to
        Object[] win = this.game.threeInRow();
        if (this.game.getWinner() != ' ' || (Boolean) win[0]) {
            model.addAttribute("winner", win[1]);
        } else if (this.playNumber <= 8) {
            if (playerVal.equals('O') && playNumber % 2 == 0 && type.equals("bot")) {
                this.move("1");
            } else if (playerVal.equals('X') && playNumber % 2 == 1 && type.equals("bot")) {
                this.move("1");
            }
            Object[] botWin = this.game.threeInRow();
            if (this.game.getWinner() != ' ' || (Boolean) botWin[0]) {
                model.addAttribute("winner", botWin[1]);
            }
        } else {
            model.addAttribute("winner", "Cats game");
        }
        Character currentPlayer = playNumber % 2 == 0 ? 'X' : 'O';
        model.addAttribute("currentPlayer", currentPlayer);
        return "game";
    }

    @GetMapping("/gameSetup")
    public String gameSetup(@RequestParam(required = false) String value, Model model) {
        if (value == null) {
            model.addAttribute("mode", "none");
        } else if (value.equals("bot")) {
            model.addAttribute("mode", "bot");
        } else if (value.equals("friend")) {
            model.addAttribute("mode", "friend");
        }
        return "gameSetup";
    }

    @PostMapping("/reset")
    public String reset() {
        this.playNumber = 0;
        this.game.reset();
        return "redirect:/playGame";
    }

    @PostMapping("/gameSetup/setGameType")
    public String setPlayerName(@RequestParam String type) {
//        System.out.println(type);
        this.type = type;
        if (type.equals("bot")) {
            return "redirect:/gameSetup?value=bot";
        } else if (type.equals("friend")) {
            this.playerVal = 'X';
            this.botDiff = 1; // change value so it passes the playGame checks
            return "redirect:/gameSetup?value=friend";
        }
        return "redirect:/";
    }

    @PostMapping("/gameSetup/setDifficulty")
    public String setDifficulty(@RequestParam String difficulty) {
//        System.out.println(difficulty);
        switch (difficulty) {
            case "easy" -> this.botDiff = 1;
            case "medium" -> this.botDiff = 2;
            case "hard" -> this.botDiff = 3;
        }
        return "redirect:/gameSetup?value=bot";
    }

    @PostMapping("/gameSetup/setPlayerValue")
    public String setPlayerValue(@RequestParam String playerValue) {
//        System.out.println("Player value was set to: " + playerValue);
        this.playerVal = playerValue.charAt(0);

        return "redirect:/gameSetup?value=bot";
    }

    @PostMapping("/gameSetup/setName")
    public String setName(@RequestParam String name) {
        if (name.isEmpty()) {
            this.name = "Player";
        } else {
            this.name = name;
        }
        return "redirect:/gameSetup?value=" + this.type;
    }

    @PostMapping("/playGame/move")
    public String move(@RequestParam String move) {
        if (this.game.getWinner() == ' ' && this.playNumber <= 8) {
            if (this.type.equals("friend")) {
                if (this.playNumber % 2 == 0) {
                    this.game.playerPlay('X', Integer.parseInt(move));
                } else {
                    this.game.playerPlay('O', Integer.parseInt(move));
                }
            } else {
                if (this.playNumber % 2 == 0) {
                    if (playerVal == 'X') {
                        this.game.playerPlay(playerVal, Integer.parseInt(move));
                    } else {
                        this.game.botPlay(playerVal, this.botDiff);
                    }
                } else {
                    if (playerVal == 'O') {
                        this.game.playerPlay(playerVal, Integer.parseInt(move));

                    } else {
                        this.game.botPlay(playerVal, this.botDiff);
                    }
                }
            }
            this.playNumber++;
        }

        return "redirect:/playGame";
    }

}