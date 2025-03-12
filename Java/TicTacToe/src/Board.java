import java.util.ArrayList;
import java.util.HashMap;
import java.util.logging.XMLFormatter;

public class Board {
    private String[][] board;
    Board() {
        this.newBoard();
    }
    Board(String[][] s) {
        this.board = s;
    }
    public void newBoard() {
        String[][] b = new String[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                b[i][j] = " ";
            }
        }
        this.board = b;
    }
    public String[][] getBoard() {
        return this.board;
    }
    public void showBoard() {
        for (int i = 0; i < 3; i++) {
            System.out.printf(board[i][0] + " | " + board[i][1] + " | " + board[i][2] + "\n");
            if (i != 2) {
                System.out.println("----------");
            }
        }
        System.out.println("\n");
    }
//    0 1 2
//    3 4 5
//    6 7 8
    public void showNumberBoard() {
        System.out.println("0 | 1 | 2\n----------\n3 | 4 | 5\n----------\n6 | 7 | 8");
    }
//    X O X      O O X      X O O
//    O O X  ->  X O O  ==  O O X
//    O X O      O X X      X X O
    public boolean threeInRow() {
//        System.out.println("tried 3 in a row");
        String[][] flipped = new String[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                flipped[i][j] = board[j][i];
            }
        }
//        Diagonal
        if (getBoard()[0][0].equals(getBoard()[1][1]) && getBoard()[0][0].equals(getBoard()[2][2]) && !getBoard()[0][0].equals(" ")) {
            return true;
        } else if (getBoard()[0][2].equals(getBoard()[1][1]) && getBoard()[0][2].equals(getBoard()[2][0]) && !getBoard()[0][2].equals(" ")) {
            return true;
        }
//        Horizontal
        for (String[] row : board) {
            HashMap<String, Integer> mapRow = new HashMap<>();
            for (String val : row) {
                if (mapRow.containsKey(val)) {
                    int curr = mapRow.get(val);
                    mapRow.replace(val, curr + 1);
                } else {
                    mapRow.put(val, 1);
                }
            }
            if (mapRow.containsValue(3) && !mapRow.containsKey(" "))
                return true;
//            System.out.println("Row: " + mapRow);
        }
//        Vertical
        for (String[] col : flipped) {
            HashMap<String, Integer> mapCol = new HashMap<>();
            for (String val : col) {
                if (mapCol.containsKey(val)) {
                    int curr = mapCol.get(val);
                    mapCol.replace(val, curr + 1);
                } else {
                    mapCol.put(val, 1);
                }
            }
            if (mapCol.containsValue(3) && !mapCol.containsKey(" "))
                return true;
//            System.out.println("Column: " + mapCol);
        }
        return false;
    }

}
