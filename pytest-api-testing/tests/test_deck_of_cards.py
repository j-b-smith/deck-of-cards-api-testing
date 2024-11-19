import pytest
import requests
from url_builder import URLBuilder

def test_create_new_deck():
    """Test creating a new deck."""
    url = URLBuilder.new_deck(shuffle=True, jokers_enabled=True)
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['success'] is True
    assert 'deck_id' in response_json
    assert response_json['remaining'] == 54  # 52 cards + 2 jokers
    global deck_id
    deck_id = response_json['deck_id']

def test_shuffle_existing_deck():
    """Test shuffling an existing deck."""
    url = URLBuilder.shuffle_deck(deck_id)
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['success'] is True
    assert response_json['shuffled'] is True

def test_draw_cards():
    """Test drawing cards from the deck."""
    url = URLBuilder.draw_cards(deck_id, count=5)
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['success'] is True
    assert len(response_json['cards']) == 5
    global drawn_cards
    drawn_cards = [card['code'] for card in response_json['cards']]

def test_add_to_pile():
    """Test adding cards to a named pile."""
    pile_name = "testpile"
    cards = ",".join(drawn_cards)
    url = URLBuilder.add_to_pile(deck_id, pile_name, cards)
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['success'] is True
    assert pile_name in response_json['piles']

def test_list_pile():
    """Test listing cards in a named pile."""
    pile_name = "testpile"
    url = URLBuilder.list_pile(deck_id, pile_name)
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['success'] is True
    assert 'cards' in response_json['piles'][pile_name]

def test_shuffle_pile():
    """Test shuffling a named pile."""
    pile_name = "testpile"
    url = URLBuilder.shuffle_pile(deck_id, pile_name)
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['success'] is True

def test_draw_from_pile():
    """Test drawing cards from a named pile."""
    pile_name = "testpile"
    url = URLBuilder.draw_from_pile(deck_id, pile_name, count=2)
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['success'] is True
    assert len(response_json['cards']) == 2

def test_return_to_deck():
    """Test returning cards to the deck."""
    cards = ",".join(drawn_cards)
    url = URLBuilder.return_to_deck(deck_id, cards)
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['success'] is True

@pytest.mark.parametrize("count", [1, 5, 52, 0, 55])
def test_drawing_varied_numbers_of_cards_from_new_deck(count):
    """
    Test drawing different numbers of cards from a newly created deck.
    Covers edge cases for normal draws, zero draws, and excessive draws.
    """
    # Create a new shuffled deck
    url = URLBuilder.new_deck(shuffle=True)
    response = requests.get(url)
    assert response.status_code == 200
    deck_id = response.json()['deck_id']

    # Draw the specified number of cards
    draw_url = URLBuilder.draw_cards(deck_id, count)
    draw_response = requests.get(draw_url)
    assert draw_response.status_code == 200
    draw_json = draw_response.json()
    
    # Validation based on count
    if count == 0:
        assert draw_json['cards'] == []
    elif count > 52:
        assert draw_json['remaining'] == 0
    else:
        assert len(draw_json['cards']) == min(count, 52)

@pytest.mark.parametrize("shuffle, jokers_enabled", [
    (False, False),
    (True, False),
    (False, True),
    (True, True)
])
def test_creating_new_deck_with_shuffle_and_joker_options(shuffle, jokers_enabled):
    """
    Test creating a new deck with different combinations of shuffle and jokers_enabled options.
    Verifies deck creation and remaining cards count based on input options.
    """
    url = URLBuilder.new_deck(shuffle=shuffle, jokers_enabled=jokers_enabled)
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['success'] is True
    expected_cards = 54 if jokers_enabled else 52
    assert response_json['remaining'] == expected_cards

import pytest
import requests
from url_builder import URLBuilder

@pytest.mark.parametrize("count", [0, 3, 5, 1, 10])
def test_drawing_specified_number_of_cards_from_pile(count):
    """
    Test drawing different numbers of cards from a named pile.
    Includes tests for drawing zero cards and more cards than available.
    """
    # Step 1: Create and shuffle a new deck
    url = URLBuilder.new_deck(shuffle=True)
    response = requests.get(url)
    assert response.status_code == 200, f"Failed to create a new deck. Status code: {response.status_code}"
    response_json = response.json()
    deck_id = response_json['deck_id']

    # Step 2: Draw initial cards from the deck (defaults to the draw count plus 5)
    draw_url = URLBuilder.draw_cards(deck_id, count=20)
    draw_response = requests.get(draw_url)
    assert draw_response.status_code == 200, f"Failed to draw cards. Status code: {draw_response.status_code}"
    drawn_cards = draw_response.json().get('cards', [])
    assert drawn_cards, "No cards were drawn from the deck."

    # Prepare cards for adding to the pile
    card_codes = [card['code'] for card in drawn_cards]
    cards = ",".join(card_codes)
    pile_name = "test_pile"

    # Step 3: Add drawn cards to a named pile
    add_url = URLBuilder.add_to_pile(deck_id, pile_name, cards)
    add_response = requests.get(add_url)
    assert add_response.status_code == 200, f"Failed to add cards to the pile. Status code: {add_response.status_code}"
    add_json = add_response.json()
    assert add_json.get('success', False), "Failed to add cards to the pile."

    # Step 4: Draw specified number of cards from the pile
    draw_from_pile_url = URLBuilder.draw_from_pile(deck_id, pile_name, count)
    draw_from_pile_response = requests.get(draw_from_pile_url)
    assert draw_from_pile_response.status_code == 200, f"Failed to draw cards from the pile. Status code: {draw_from_pile_response.status_code}"
    draw_json = draw_from_pile_response.json()

    # Step 5: Validate the results based on the requested count
    cards_drawn = draw_json.get('cards', [])

    if count == 0:
        # Expect no cards to be drawn
        assert cards_drawn == [], "Expected no cards to be drawn when count is 0."
    
    elif count > len(card_codes):
        # Expect to draw all available cards if the requested count exceeds available cards
        assert len(cards_drawn) == len(card_codes), f"Expected to draw all available cards from the pile, but got {len(cards_drawn)} cards."
    
    else:
        # Expect to draw exactly the requested number of cards
        assert len(cards_drawn) == count, f"Expected to draw {count} cards from the pile, but got {len(cards_drawn)}."

    # Step 6: Additional validation to ensure unique card codes
    drawn_codes = [card['code'] for card in cards_drawn]
    assert len(drawn_codes) == len(set(drawn_codes)), "Duplicate cards were drawn from the pile."


