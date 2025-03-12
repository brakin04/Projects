import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class DeckTest {

    @Test
    void testDrawCard() {
        Deck d1 = new Deck();
        assertAll(
                () -> assertEquals("10 of " + Suit.DIAMONDS, d1.drawCard().toString()),
                () -> assertEquals("10 of " + Suit.DIAMONDS, d1.drawCard().toString()),
                () -> assertEquals("10 of " + Suit.DIAMONDS, d1.drawCard().toString()),
                () -> assertEquals("10 of " + Suit.DIAMONDS, d1.drawCard().toString()),
                () -> assertEquals("9 of " + Suit.DIAMONDS, d1.drawCard().toString()),
                () -> assertEquals("8 of " + Suit.DIAMONDS, d1.drawCard().toString()),
                () -> assertEquals("7 of " + Suit.DIAMONDS, d1.drawCard().toString())
        );
    }

    @Test
    void testIsEmpty() {
        Deck d1 = new Deck();
        for (int i = 0; i < 52; i++) {
            assertFalse(d1.isEmpty());
            d1.drawCard();
        }
        assertTrue(d1.isEmpty());
    }
}