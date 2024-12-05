import pytest
from deck_provider import DeckProvider


def test_create_deck():
    """Test creating a new deck."""
    deck_id = DeckProvider.create_deck(shuffle=True, jokers_enabled=True)
    assert isinstance(deck_id, str) and len(deck_id) > 0


def test_shuffle_deck():
    """Test shuffling an existing deck."""
    deck_id = DeckProvider.create_deck()
    response = DeckProvider.shuffle_deck(deck_id)
    assert response["success"] is True
    assert response["shuffled"] is True


def test_draw_cards():
    """Test drawing cards from a deck."""
    deck_id = DeckProvider.create_deck(shuffle=True)
    response = DeckProvider.draw_cards(deck_id, count=5)
    assert len(response["cards"]) == 5
    assert response["remaining"] == 47


def test_add_to_pile_and_list_pile():
    """Test adding cards to a pile and listing them."""
    deck_id = DeckProvider.create_deck(shuffle=True)
    response = DeckProvider.draw_cards(deck_id, count=5)
    cards = ",".join(card["code"] for card in response["cards"])
    
    pile_name = "test_pile"
    add_response = DeckProvider.add_to_pile(deck_id, pile_name, cards)
    assert add_response["success"] is True

    list_response = DeckProvider.list_pile(deck_id, pile_name)
    assert pile_name in list_response["piles"]


def test_draw_from_pile():
    """Test drawing cards from a pile."""
    deck_id = DeckProvider.create_deck(shuffle=True)
    response = DeckProvider.draw_cards(deck_id, count=5)
    cards = ",".join(card["code"] for card in response["cards"])

    pile_name = "test_pile"
    DeckProvider.add_to_pile(deck_id, pile_name, cards)
    draw_response = DeckProvider.draw_from_pile(deck_id, pile_name, count=3)
    assert len(draw_response["cards"]) == 3


def test_return_to_deck():
    """Test returning cards to the deck."""
    deck_id = DeckProvider.create_deck(shuffle=True)
    response = DeckProvider.draw_cards(deck_id, count=5)
    cards = ",".join(card["code"] for card in response["cards"])

    return_response = DeckProvider.return_to_deck(deck_id, cards)
    assert return_response["success"] is True
