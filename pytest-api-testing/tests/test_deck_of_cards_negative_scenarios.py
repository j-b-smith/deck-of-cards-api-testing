import pytest
from deck_provider import DeckProvider


def test_draw_more_than_available():
    """
    Test drawing more cards than available in a new deck.
    Expected behavior: The API should return only the available cards (52), and the remaining count should be 0.
    """
    # The API returns success as False even though it correctly returns the available cards.
    # This is inconsistent behavior—success should be True when the API correctly handles the request.
    deck_id = DeckProvider.create_deck(shuffle=True)
    draw_response = DeckProvider.draw_cards(deck_id, count=60)

    assert draw_response["remaining"] == 0, "Expected remaining cards to be 0 after drawing all available cards."
    assert len(draw_response["cards"]) == 52, "Expected to draw only the available 52 cards."


def test_add_invalid_cards_to_pile():
    """
    Test adding invalid card codes to a pile.
    Expected behavior: The API should fail with success=False and provide an error message.
    """

    # The API allows adding invalid card codes to a pile, but the API should fail with success=False and provide an error message
    deck_id = DeckProvider.create_deck(shuffle=True)
    invalid_cards = "ZZ,AA"
    pile_name = "invalid_pile"
    add_response = DeckProvider.add_to_pile(deck_id, pile_name, invalid_cards)

    assert add_response["success"] is False, "Expected adding invalid cards to fail."
    assert "error" in add_response, "Expected error message in response for invalid card addition."


def test_draw_from_nonexistent_pile():
    """
    Test drawing cards from a pile that does not exist.
    Expected behavior: The API should fail with a clear error message indicating the pile does not exist.
    """
    deck_id = DeckProvider.create_deck(shuffle=True)
    pile_name = "nonexistent_pile"
    with pytest.raises(Exception) as exc_info:
        DeckProvider.draw_from_pile(deck_id, pile_name, count=5)

    assert "Server Error" in str(exc_info.value), "Expected error message for drawing from a nonexistent pile."


def test_draw_negative_cards():
    """
    Test drawing a negative number of cards.
    Expected behavior: The API should fail with success=False and provide an error message.
    """
    # The API correctly returns all 52 available cards but sets "success": false in the response, which causes a failure 
    # The API should not accept a negative number of cards to draw
    deck_id = DeckProvider.create_deck(shuffle=True)
    draw_response = DeckProvider.draw_cards(deck_id, count=-5)

    assert draw_response["success"] is False, "Expected drawing a negative number of cards to fail."
    assert "error" in draw_response, "Expected error message in response for invalid draw count."


def test_shuffle_invalid_deck():
    """
    Test shuffling a non-existent deck.
    Expected behavior: The API should fail with a 404 status code and a descriptive error message.
    """
    invalid_deck_id = "invalid123"
    with pytest.raises(Exception) as exc_info:
        DeckProvider.shuffle_deck(invalid_deck_id)

    assert "Not Found" in str(exc_info.value), "Expected error message for shuffling a non-existent deck."
