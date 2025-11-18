import unittest

from card_game import Card, Suit, SilverCard, GoldCard, WildCard, Joker, score


class CardTests(unittest.TestCase):
    def test_01_card_creation(self):
        # Arrange
        suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        ranks = [str(rank) for rank in range(2, 11)] + ["J", "Q", "K", "A"]

        # Act & Assert
        for suit in suits:
            for rank in ranks:
                try:
                    Card(rank, suit)
                except Exception:
                    self.fail(f"Card creation failed for rank {rank} and suit {suit}")

    def test_02_rank_property(self):
        # Arrange
        expected_rank = "Q"
        card = Card(expected_rank, Suit.SPADES)

        # Act
        actual_rank = card.rank

        # Assert
        self.assertEqual(actual_rank, expected_rank)

    def test_03_suit_property(self):
        # Arrange
        expected_suit = Suit.SPADES
        card = Card("A", expected_suit)

        # Act
        actual_suit = card.suit

        # Assert
        self.assertEqual(actual_suit, expected_suit)

    def test_04_read_only_rank(self):
        # Arrange
        card = Card("A", Suit.SPADES)

        # Act & Assert
        with self.assertRaises(AttributeError):
            card.rank = "2"

    def test_05_read_only_suit(self):
        # Arrange
        card = Card("A", Suit.SPADES)

        # Act & Assert
        with self.assertRaises(AttributeError):
            card.suit = Suit.HEARTS

    def test_06_str_method(self):
        # Arrange
        suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        ranks = [str(rank) for rank in range(2, 11)] + ["J", "Q", "K", "A"]

        suit_to_string = {
            Suit.CLUBS: "♣",
            Suit.DIAMONDS: "♦",
            Suit.HEARTS: "♥",
            Suit.SPADES: "♠",
        }

        # Act & Assert
        for suit in suits:
            for rank in ranks:
                card = Card(rank, suit)
                expected_str = f"{rank}{suit_to_string[suit]}"
                actual_str = str(card)
                self.assertEqual(actual_str, expected_str)

    def test_07_chips_method(self):
        # Arrange
        suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        ranks = [str(rank) for rank in range(2, 11)] + ["J", "Q", "K", "A"]
        expected_chips = (list(range(2, 11)) + [10] * 3 + [11]) * 4

        cards = [Card(rank, suit) for suit in suits for rank in ranks]

        # Act
        actual_chips = [card.chips for card in cards]

        # Assert
        self.assertEqual(actual_chips, expected_chips)


class SilverCardTests(unittest.TestCase):
    def test_01_card_creation(self):
        # Arrange
        suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        ranks = [str(rank) for rank in range(2, 11)] + ["J", "Q", "K", "A"]

        # Act & Assert
        for suit in suits:
            for rank in ranks:
                try:
                    SilverCard(rank, suit)
                except Exception:
                    self.fail(f"Card creation failed for rank {rank} and suit {suit}")

    def test_02_rank_property(self):
        # Arrange
        expected_rank = "Q"
        card = SilverCard(expected_rank, Suit.SPADES)

        # Act
        actual_rank = card.rank

        # Assert
        self.assertEqual(actual_rank, expected_rank)

    def test_03_suit_property(self):
        # Arrange
        expected_suit = Suit.SPADES
        card = SilverCard("A", expected_suit)

        # Act
        actual_suit = card.suit

        # Assert
        self.assertEqual(actual_suit, expected_suit)

    def test_04_read_only_rank(self):
        # Arrange
        card = SilverCard("A", Suit.SPADES)

        # Act & Assert
        with self.assertRaises(AttributeError):
            card.rank = "2"

    def test_05_read_only_suit(self):
        # Arrange
        card = SilverCard("A", Suit.SPADES)

        # Act & Assert
        with self.assertRaises(AttributeError):
            card.suit = Suit.HEARTS

    def test_06_str_method(self):
        # Arrange
        suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        ranks = [str(rank) for rank in range(2, 11)] + ["J", "Q", "K", "A"]

        suit_to_string = {
            Suit.CLUBS: "♣",
            Suit.DIAMONDS: "♦",
            Suit.HEARTS: "♥",
            Suit.SPADES: "♠",
        }

        # Act & Assert
        for suit in suits:
            for rank in ranks:
                card = SilverCard(rank, suit)
                expected_str = f"Silver {rank}{suit_to_string[suit]}"
                actual_str = str(card)
                self.assertEqual(actual_str, expected_str)

    def test_07_chips_method(self):
        # Arrange
        suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        ranks = [str(rank) for rank in range(2, 11)] + ["J", "Q", "K", "A"]
        expected_chips = (list(range(2, 11)) + [10] * 3 + [11]) * 4
        expected_chips = [chips * 2 for chips in expected_chips]

        cards = [SilverCard(rank, suit) for suit in suits for rank in ranks]

        # Act
        actual_chips = [card.chips for card in cards]

        # Assert
        self.assertEqual(actual_chips, expected_chips)


class GoldCardTests(unittest.TestCase):
    def test_01_card_creation(self):
        # Arrange
        suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        ranks = [str(rank) for rank in range(2, 11)] + ["J", "Q", "K", "A"]

        # Act & Assert
        for suit in suits:
            for rank in ranks:
                try:
                    GoldCard(rank, suit)
                except Exception:
                    self.fail(f"Card creation failed for rank {rank} and suit {suit}")

    def test_02_rank_property(self):
        # Arrange
        expected_rank = "Q"
        card = GoldCard(expected_rank, Suit.SPADES)

        # Act
        actual_rank = card.rank

        # Assert
        self.assertEqual(actual_rank, expected_rank)

    def test_03_suit_property(self):
        # Arrange
        expected_suit = Suit.SPADES
        card = GoldCard("A", expected_suit)

        # Act
        actual_suit = card.suit

        # Assert
        self.assertEqual(actual_suit, expected_suit)

    def test_04_read_only_rank(self):
        # Arrange
        card = GoldCard("A", Suit.SPADES)

        # Act & Assert
        with self.assertRaises(AttributeError):
            card.rank = "2"

    def test_05_read_only_suit(self):
        # Arrange
        card = GoldCard("A", Suit.SPADES)

        # Act & Assert
        with self.assertRaises(AttributeError):
            card.suit = Suit.HEARTS

    def test_06_str_method(self):
        # Arrange
        suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        ranks = [str(rank) for rank in range(2, 11)] + ["J", "Q", "K", "A"]

        suit_to_string = {
            Suit.CLUBS: "♣",
            Suit.DIAMONDS: "♦",
            Suit.HEARTS: "♥",
            Suit.SPADES: "♠",
        }

        # Act & Assert
        for suit in suits:
            for rank in ranks:
                card = GoldCard(rank, suit)
                expected_str = f"Gold {rank}{suit_to_string[suit]}"
                actual_str = str(card)
                self.assertEqual(actual_str, expected_str)

    def test_07_chips_method(self):
        # Arrange
        suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        ranks = [str(rank) for rank in range(2, 11)] + ["J", "Q", "K", "A"]
        expected_chips = (list(range(2, 11)) + [10] * 3 + [11]) * 4
        expected_chips = [chips * 4 for chips in expected_chips]
        cards = [GoldCard(rank, suit) for suit in suits for rank in ranks]

        # Act
        actual_chips = [card.chips for card in cards]

        # Assert
        self.assertEqual(actual_chips, expected_chips)


class WildCardTests(unittest.TestCase):
    def test_01_card_creation(self):
        # Arrange
        ranks = [str(rank) for rank in range(2, 11)] + ["J", "Q", "K", "A"]

        # Act & Assert
        for rank in ranks:
            try:
                WildCard(rank)
            except Exception:
                self.fail(f"Card creation failed for rank {rank}")

    def test_02_rank_property(self):
        # Arrange
        expected_rank = "Q"
        card = WildCard(expected_rank)

        # Act
        actual_rank = card.rank

        # Assert
        self.assertEqual(actual_rank, expected_rank)

    def test_03_suit_property(self):
        # Arrange
        expected_suit = Suit.WILD
        card = WildCard("A")

        # Act
        actual_suit = card.suit

        # Assert
        self.assertEqual(actual_suit, expected_suit)

    def test_04_read_only_rank(self):
        # Arrange
        card = WildCard("A")

        # Act & Assert
        with self.assertRaises(AttributeError):
            card.rank = "2"

    def test_05_read_only_suit(self):
        # Arrange
        card = WildCard("A")

        # Act & Assert
        with self.assertRaises(AttributeError):
            card.suit = Suit.HEARTS

    def test_06_str_method(self):
        # Arrange
        ranks = [str(rank) for rank in range(2, 11)] + ["J", "Q", "K", "A"]

        # Act & Assert
        for rank in ranks:
            card = WildCard(rank)
            expected_str = f"Wild {rank}W"
            actual_str = str(card)
            self.assertEqual(actual_str, expected_str)

    def test_07_chips_method(self):
        # Arrange
        ranks = [str(rank) for rank in range(2, 11)] + ["J", "Q", "K", "A"]
        expected_chips = list(range(2, 11)) + [10] * 3 + [11]

        cards = [WildCard(rank) for rank in ranks]

        # Act
        actual_chips = [card.chips for card in cards]

        # Assert
        self.assertEqual(actual_chips, expected_chips)


class JokerTests(unittest.TestCase):
    def test_01_card_creation(self):
        # Act & Assert
        try:
            Joker(10, 2)
        except Exception:
            self.fail("Joker creation failed")

    def test_02_chips_property(self):
        # Arrange
        expected_chips = 10
        card = Joker(expected_chips, 2)

        # Act
        actual_chips = card.chips

        # Assert
        self.assertEqual(actual_chips, expected_chips)

    def test_03_mult_property(self):
        # Arrange
        expected_mult = 2
        card = Joker(10, expected_mult)

        # Act
        actual_mult = card.mult

        # Assert
        self.assertEqual(actual_mult, expected_mult)

    def test_04_read_only_chips(self):
        # Arrange
        card = Joker(10, 2)

        # Act & Assert
        with self.assertRaises(AttributeError):
            card.chips = 5

    def test_05_read_only_mult(self):
        # Arrange
        card = Joker(10, 2)

        # Act & Assert
        with self.assertRaises(AttributeError):
            card.mult = 3

    def test_06_action_creation(self):
        # Arrange
        def expected_action(chips, mult):
            return (chips + 5, mult * 2)

        try:
            card = Joker(10, 2, expected_action)
        except Exception:
            self.fail("Joker creation failed")

    def test_07_action_property(self):
        # Arrange
        def expected_action(chips, mult):
            return (chips + 5, mult * 2)

        card = Joker(10, 2, expected_action)

        # Act
        actual_action = card.action

        # Assert
        self.assertEqual(actual_action, expected_action)

    def test_08_read_only_action(self):
        # Arrange
        def expected_action(chips, mult):
            return (chips + 5, mult * 2)

        card = Joker(10, 2, expected_action)

        # Act & Assert
        with self.assertRaises(AttributeError):
            card.action = lambda chips, mult: (chips, mult)


class JokerWithEffectsCalculationTests(unittest.TestCase):
    def test_01_single_effect(self):
        # Arrange
        cards = [
            Card("A", Suit.CLUBS),
            Card("3", Suit.DIAMONDS),
            Card("Q", Suit.HEARTS),
            Card("4", Suit.DIAMONDS),
            Card("J", Suit.SPADES),
        ]
        jokers = [Joker(5, 3, action=lambda c, m: (c * 2, m * 2)), Joker(10, 4)]

        expected_chips = (11 + 3 + 10 + 4 + 10) + (5 + 10)
        expected_mult = (1 + 2) + (3 + 4)

        expected_chips = expected_chips * 2
        expected_mult = expected_mult * 2

        expected_score = expected_chips * expected_mult

        # Act
        actual_score = score(cards, jokers)

        # Assert
        self.assertEqual(actual_score, expected_score)

    def test_02_single_effect_second_joker(self):
        # Arrange
        cards = [
            Card("A", Suit.CLUBS),
            Card("3", Suit.DIAMONDS),
            Card("Q", Suit.HEARTS),
            Card("4", Suit.DIAMONDS),
            Card("J", Suit.SPADES),
        ]
        jokers = [Joker(5, 3), Joker(10, 4, action=lambda c, m: (c * 2, m * 2))]

        expected_chips = (11 + 3 + 10 + 4 + 10) + (5 + 10)
        expected_mult = (1 + 2) + (3 + 4)

        expected_chips = expected_chips * 2
        expected_mult = expected_mult * 2

        expected_score = expected_chips * expected_mult

        # Act
        actual_score = score(cards, jokers)

        # Assert
        self.assertEqual(actual_score, expected_score)

    def test_03_two_effects_jokers(self):
        # Arrange
        cards = [
            Card("A", Suit.CLUBS),
            Card("3", Suit.DIAMONDS),
            Card("Q", Suit.HEARTS),
            Card("4", Suit.DIAMONDS),
            Card("J", Suit.SPADES),
        ]
        jokers = [Joker(5, 3, lambda c, m: (c * 2, m * 3)), Joker(10, 4, action=lambda c, m: (c + 5, m + 2))]

        expected_chips = (11 + 3 + 10 + 4 + 10) + (5 + 10)
        expected_mult = (1 + 2) + (3 + 4)

        expected_chips = expected_chips * 2  # First joker
        expected_chips = expected_chips + 5  # Second joker
        expected_mult = expected_mult * 3  # First joker
        expected_mult = expected_mult + 2  # Second joker

        expected_score = expected_chips * expected_mult

        # Act
        actual_score = score(cards, jokers)

        # Assert
        self.assertEqual(actual_score, expected_score)
