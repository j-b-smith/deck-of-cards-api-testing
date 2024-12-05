import pytest
from url_builder import URLBuilder

# Constants
BASE_URL = "https://deckofcardsapi.com/api/deck"
DECK_ID = "test123"
PILE_NAME = "test_pile"
CARDS = "AS,2S,KH"

def test_new_deck_url():
    """Test URL generation for creating a new deck."""
    url = URLBuilder.new_deck()
    assert url == f"{BASE_URL}/new/", f"Expected URL does not match: {url}"

    url_with_shuffle = URLBuilder.new_deck(shuffle=True)
    assert url_with_shuffle == f"{BASE_URL}/new/?shuffle=true", f"Expected URL does not match: {url_with_shuffle}"

    url_with_jokers = URLBuilder.new_deck(jokers_enabled=True)
    assert url_with_jokers == f"{BASE_URL}/new/?jokers_enabled=true", f"Expected URL does not match: {url_with_jokers}"

    url_with_both = URLBuilder.new_deck(shuffle=True, jokers_enabled=True)
    assert url_with_both == f"{BASE_URL}/new/?shuffle=true&jokers_enabled=true", f"Expected URL does not match: {url_with_both}"

def test_new_partial_deck_url():
    """Test URL generation for creating a partial deck."""
    url = URLBuilder.new_partial_deck(CARDS)
    assert url == f"{BASE_URL}/new/?cards={CARDS}", f"Expected URL does not match: {url}"

def test_shuffle_deck_url():
    """Test URL generation for shuffling a deck."""
    url = URLBuilder.shuffle_deck(DECK_ID)
    assert url == f"{BASE_URL}/{DECK_ID}/shuffle/", f"Expected URL does not match: {url}"

def test_reshuffle_deck_url():
    """Test URL generation for reshuffling a deck."""
    url = URLBuilder.reshuffle_deck(DECK_ID)
    assert url == f"{BASE_URL}/{DECK_ID}/shuffle/", f"Expected URL does not match: {url}"

    url_with_remaining = URLBuilder.reshuffle_deck(DECK_ID, remaining_only=True)
    assert url_with_remaining == f"{BASE_URL}/{DECK_ID}/shuffle/?remaining=true", f"Expected URL does not match: {url_with_remaining}"

def test_draw_cards_url():
    """Test URL generation for drawing cards."""
    url = URLBuilder.draw_cards(DECK_ID, count=5)
    assert url == f"{BASE_URL}/{DECK_ID}/draw/?count=5", f"Expected URL does not match: {url}"

def test_add_to_pile_url():
    """Test URL generation for adding cards to a pile."""
    url = URLBuilder.add_to_pile(DECK_ID, PILE_NAME, CARDS)
    assert url == f"{BASE_URL}/{DECK_ID}/pile/{PILE_NAME}/add/?cards={CARDS}", f"Expected URL does not match: {url}"

def test_draw_from_pile_url():
    """Test URL generation for drawing cards from a pile."""
    url = URLBuilder.draw_from_pile(DECK_ID, PILE_NAME, count=3)
    assert url == f"{BASE_URL}/{DECK_ID}/pile/{PILE_NAME}/draw/?count=3", f"Expected URL does not match: {url}"

def test_list_pile_url():
    """Test URL generation for listing cards in a pile."""
    url = URLBuilder.list_pile(DECK_ID, PILE_NAME)
    assert url == f"{BASE_URL}/{DECK_ID}/pile/{PILE_NAME}/list/", f"Expected URL does not match: {url}"

def test_shuffle_pile_url():
    """Test URL generation for shuffling a pile."""
    url = URLBuilder.shuffle_pile(DECK_ID, PILE_NAME)
    assert url == f"{BASE_URL}/{DECK_ID}/pile/{PILE_NAME}/shuffle/", f"Expected URL does not match: {url}"

def test_return_to_deck_url():
    """Test URL generation for returning cards to the deck."""
    url = URLBuilder.return_to_deck(DECK_ID, CARDS)
    assert url == f"{BASE_URL}/{DECK_ID}/return/?cards={CARDS}", f"Expected URL does not match: {url}"
