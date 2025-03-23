public class goFishCard {

    public int value;

    goFishCard(int value1) {
        this.value = value1;
    }

    @Override
    public String toString() { return String.format("%d", value); }

    // Returns value of card
    public int getValue() { return this.value; }
}
