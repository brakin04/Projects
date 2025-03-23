import java.io.*;
import java.util.ArrayList;
import java.nio.file.Path;
import java.nio.file.Paths;

public class WordChecker {

    private final String thisPath;
    private ArrayList<String> dictionary;

    public WordChecker() {
        this.thisPath = this.getPath();
        this.populateDictionary();
    }

    // Checks the word
    public boolean checkWord(String word) {
        return this.dictionary.contains(word);
    }

    // Initializes the dictionary based on a .txt file
    private void populateDictionary() {
        this.dictionary = new ArrayList<>();
        // Read the file and add all lines to the dictionary
        try (BufferedReader reader = new BufferedReader(new FileReader(this.thisPath))) {
            String line;
            // Write each line to the dictionary
            while ((line = reader.readLine()) != null) {
                line = line.strip();
                dictionary.add(line);
            }
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }
    }

    // Gets the file path
    private String getPath() {
        Path path = Paths.get("Words");
        return path.toAbsolutePath().toString();
    }

    public ArrayList<String> getDict() {
        return this.dictionary;
    }
}
