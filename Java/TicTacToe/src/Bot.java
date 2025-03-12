import java.util.ArrayList;
import java.util.HashMap;

public class Bot {
    int difficulty;
    Bot(int diff) {
        this.difficulty = diff;
    }
//        return number according to play instead of answer so randint(0,1) gives multiple possible plays to randomize
    String[][] go(String s, Board b) {
        String[][] nb = b.getBoard();
        String bot = "X";
        String player = "O";
        if (s.equals("O")) {
            bot = "O";
            player = "X";
        }
//        win
        if (nb[0][0].equals(bot) && nb[0][1].equals(bot) && nb[0][2].equals(" ")) {
            nb[0][2] = bot;
        } else if (nb[0][0].equals(bot) && nb[0][2].equals(bot) && nb[0][1].equals(" ")) {
            nb[0][1] = bot;
        } else if (nb[0][1].equals(bot) && nb[0][2].equals(bot) && nb[0][0].equals(" ")) {
            nb[0][0] = bot;
        } else if (nb[1][0].equals(bot) && nb[1][1].equals(bot) && nb[1][2].equals(" ")) {
            nb[1][2] = bot;
        } else if (nb[1][0].equals(bot) && nb[1][2].equals(bot) && nb[1][1].equals(" ")) {
            nb[1][1] = bot;
        } else if (nb[1][1].equals(bot) && nb[1][2].equals(bot) && nb[1][0].equals(" ")) {
            nb[1][0] = bot;
        } else if (nb[2][0].equals(bot) && nb[2][1].equals(bot) && nb[2][2].equals(" ")) {
            nb[2][2] = bot;
        } else if (nb[2][0].equals(bot) && nb[2][2].equals(bot) && nb[2][1].equals(" ")) {
            nb[2][1] = bot;
        } else if (nb[2][1].equals(bot) && nb[2][2].equals(bot) && nb[2][0].equals(" ")) {
            nb[2][0] = bot;
        }

//        horizontal
        else if (nb[0][0].equals(bot) && nb[1][0].equals(bot) && nb[2][0].equals(" ")) {
            nb[2][0] = bot;
        } else if (nb[0][0].equals(bot) && nb[2][0].equals(bot) && nb[1][0].equals(" ")) {
            nb[1][0] = bot;
        } else if (nb[2][0].equals(bot) && nb[1][0].equals(bot) && nb[0][0].equals(" ")) {
            nb[0][0] = bot;
        } else if (nb[0][1].equals(bot) && nb[1][1].equals(bot) && nb[2][1].equals(" ")) {
            nb[2][1] = bot;
        } else if (nb[0][1].equals(bot) && nb[2][1].equals(bot) && nb[1][1].equals(" ")) {
            nb[1][1] = bot;
        } else if (nb[2][1].equals(bot) && nb[1][1].equals(bot) && nb[0][1].equals(" ")) {
            nb[0][1] = bot;
        } else if (nb[0][2].equals(bot) && nb[1][2].equals(bot) && nb[2][2].equals(" ")) {
            nb[2][2] = bot;
        } else if (nb[0][2].equals(bot) && nb[2][2].equals(bot) && nb[1][2].equals(" ")) {
            nb[1][2] = bot;
        } else if (nb[2][2].equals(bot) && nb[1][2].equals(bot) && nb[0][2].equals(" ")) {
            nb[0][2] = bot;
        }

//        diagonal
        else if (nb[0][0].equals(bot) && nb[1][1].equals(bot) && nb[2][2].equals(" ")) {
            nb[2][2] = bot;
        } else if (nb[0][0].equals(bot) && nb[2][2].equals(bot) && nb[1][1].equals(" ")) {
            nb[1][1] = bot;
        } else if (nb[2][2].equals(bot) && nb[1][1].equals(bot) && nb[0][0].equals(" ")) {
            nb[0][0] = bot;
        } else if (nb[2][0].equals(bot) && nb[1][1].equals(bot) && nb[0][2].equals(" ")) {
            nb[0][2] = bot;
        } else if (nb[0][2].equals(bot) && nb[1][1].equals(bot) && nb[2][0].equals(" ")) {
            nb[2][0] = bot;
        } else if (nb[0][2].equals(bot) && nb[2][0].equals(bot) && nb[1][1].equals(" ")) {
            nb[1][1] = bot;
        }



//        play
//        vertical
        else if (nb[0][0].equals(player) && nb[0][1].equals(player) && nb[0][2].equals(" ")) {
            nb[0][2] = bot;
        } else if (nb[0][0].equals(player) && nb[0][2].equals(player) && nb[0][1].equals(" ")) {
            nb[0][1] = bot;
        } else if (nb[0][1].equals(player) && nb[0][2].equals(player) && nb[0][0].equals(" ")) {
            nb[0][0] = bot;
        } else if (nb[1][0].equals(player) && nb[1][1].equals(player) && nb[1][2].equals(" ")) {
            nb[1][2] = bot;
        } else if (nb[1][0].equals(player) && nb[1][2].equals(player) && nb[1][1].equals(" ")) {
            nb[1][1] = bot;
        } else if (nb[1][1].equals(player) && nb[1][2].equals(player) && nb[1][0].equals(" ")) {
            nb[1][0] = bot;
        } else if (nb[2][0].equals(player) && nb[2][1].equals(player) && nb[2][2].equals(" ")) {
            nb[2][2] = bot;
        } else if (nb[2][0].equals(player) && nb[2][2].equals(player) && nb[2][1].equals(" ")) {
            nb[2][1] = bot;
        } else if (nb[2][1].equals(player) && nb[2][2].equals(player) && nb[2][0].equals(" ")) {
            nb[2][0] = bot;
        }

//        horizontal
        else if (nb[0][0].equals(player) && nb[1][0].equals(player) && nb[2][0].equals(" ")) {
            nb[2][0] = bot;
        } else if (nb[0][0].equals(player) && nb[2][0].equals(player) && nb[1][0].equals(" ")) {
            nb[1][0] = bot;
        } else if (nb[2][0].equals(player) && nb[1][0].equals(player) && nb[0][0].equals(" ")) {
            nb[0][0] = bot;
        } else if (nb[0][1].equals(player) && nb[1][1].equals(player) && nb[2][1].equals(" ")) {
            nb[2][1] = bot;
        } else if (nb[0][1].equals(player) && nb[2][1].equals(player) && nb[1][1].equals(" ")) {
            nb[1][1] = bot;
        } else if (nb[2][1].equals(player) && nb[1][1].equals(player) && nb[0][1].equals(" ")) {
            nb[0][1] = bot;
        } else if (nb[0][2].equals(player) && nb[1][2].equals(player) && nb[2][2].equals(" ")) {
            nb[2][2] = bot;
        } else if (nb[0][2].equals(player) && nb[2][2].equals(player) && nb[1][2].equals(" ")) {
            nb[1][2] = bot;
        } else if (nb[2][2].equals(player) && nb[1][2].equals(player) && nb[0][2].equals(" ")) {
            nb[0][2] = bot;
        }

//        diagonal
        else if (nb[0][0].equals(player) && nb[1][1].equals(player) && nb[2][2].equals(" ")) {
            nb[2][2] = bot;
        } else if (nb[0][0].equals(player) && nb[2][2].equals(player) && nb[1][1].equals(" ")) {
            nb[1][1] = bot;
        } else if (nb[2][2].equals(player) && nb[1][1].equals(player) && nb[0][0].equals(" ")) {
            nb[0][0] = bot;
        } else if (nb[2][0].equals(player) && nb[1][1].equals(player) && nb[0][2].equals(" ")) {
            nb[0][2] = bot;
        } else if (nb[0][2].equals(player) && nb[1][1].equals(player) && nb[2][0].equals(" ")) {
            nb[2][0] = bot;
        } else if (nb[0][2].equals(player) && nb[2][0].equals(player) && nb[1][1].equals(" ")) {
            nb[1][1] = bot;
        }
//        difficulty strategy rules
//        else if (difficulty == 1 && nb[0][0].equals(player) && nb[2][2].equals(player) && nb[1][1].equals(bot)) {
//            if (nb[0][2].equals(" ")) {
//                nb[0][2] = bot;
//            } else if (nb[2][0].equals(" ")) {
//                nb[2][0] = bot;
//            } else if (nb[0][1].equals(" ")) {
//                nb[0][1] = bot;
//            } else if (nb[1][0].equals(" ")) {
//                nb[1][0] = bot;
//            } else {
//                boolean bk = false;
//                for (int i = 0; i < 3; i++) {
//                    for (int j = 0; j < 3; j++) {
//                        if (nb[i][j].equals(" ")) {
//                            nb[i][j] = bot;
//                            bk = true;
//                        }
//                        if (bk)
//                            break;
//                    }
//                    if (bk)
//                        break;
//                }
//            }
//        }
        else {
            int round = 0;
            int i;
            int j;
            while (true) {
                i = round / 3;
                j = round % 3;
                if (nb[1][1].equals(" ")) {
                    nb[1][1] = bot;
                    break;
                } else if (nb[i][j].equals(" ")) {
                    nb[i][j] = bot;
                    break;
                }
                round++;
                if (round == 9) {
                    System.out.println("Bot couldn't play");
                    break;
                }
            }
        }
        for (int k = 0; k < 9; k++) {
            if (!b.getBoard()[k/3][k%3].equals(nb[k/3][k%3])) {
                System.out.printf("Bot chose to play %s \n", k);
            }
        }
        return nb;
    }
}
