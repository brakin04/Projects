import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class CardTest {
    @Test
    void testCardToString() {
        assertAll(
                () -> assertEquals("1 of " + Suit.SPADES, new Card(Suit.SPADES, 1).toString()),
                () -> assertEquals("4 of " + Suit.CLUBS, new Card(Suit.CLUBS, 4).toString()),
                () -> assertEquals("8 of " + Suit.HEARTS, new Card(Suit.HEARTS, 8).toString()),
                () -> assertEquals("10 of " + Suit.DIAMONDS, new Card(Suit.DIAMONDS, 10).toString())
        );
    }

}