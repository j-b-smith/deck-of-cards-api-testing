import pytest
import requests
from url_builder import URLBuilder

def test_create_new_deck():
    """Test creating a new deck with default options."""
    url = URLBuilder.new_deck(shuffle=True)
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['success'] is True
    assert response_json['remaining'] == 52

def test_draw_cards():
    """Test drawing cards from a new deck."""
    url = URLBuilder.new_deck(shuffle=True)
    response = requests.get(url)
    deck_id = response.json()['deck_id']
    draw_url = URLBuilder.draw_cards(deck_id, count=5)
    draw_response = requests.get(draw_url)
    assert draw_response.status_code == 200
    draw_json = draw_response.json()
    assert len(draw_json['cards']) == 5
    assert draw_json['remaining'] == 47

def test_add_and_list_pile():
    """Test adding cards to a pile and listing them."""
    url = URLBuilder.new_deck(shuffle=True)
    response = requests.get(url)
    deck_id = response.json()['deck_id']
    draw_url = URLBuilder.draw_cards(deck_id, count=5)
    drawn_cards = requests.get(draw_url).json()['cards']
    codes = ",".join(card['code'] for card in drawn_cards)

    # Add to pile
    pile_name = "test_pile"
    add_url = URLBuilder.add_to_pile(deck_id, pile_name, codes)
    add_response = requests.get(add_url)
    assert add_response.status_code == 200
    add_json = add_response.json()
    assert add_json['success'] is True

    # List pile
    list_url = URLBuilder.list_pile(deck_id, pile_name)
    list_response = requests.get(list_url)
    assert list_response.status_code == 200
    list_json = list_response.json()
    assert 'cards' in list_json['piles'][pile_name]

def test_shuffle_pile():
    """Test shuffling a pile."""
    url = URLBuilder.new_deck(shuffle=True)
    response = requests.get(url)
    deck_id = response.json()['deck_id']
    draw_url = URLBuilder.draw_cards(deck_id, count=5)
    drawn_cards = requests.get(draw_url).json()['cards']
    codes = ",".join(card['code'] for card in drawn_cards)

    # Add to pile
    pile_name = "test_pile"
    add_url = URLBuilder.add_to_pile(deck_id, pile_name, codes)
    requests.get(add_url)

    # Shuffle pile
    shuffle_url = URLBuilder.shuffle_pile(deck_id, pile_name)
    shuffle_response = requests.get(shuffle_url)
    assert shuffle_response.status_code == 200
    shuffle_json = shuffle_response.json()
    assert shuffle_json['success'] is True

@pytest.mark.parametrize("count", [1, 5, 52, 0])
def test_drawing_varied_numbers_of_cards(count):
    """Test drawing varied numbers of cards."""
    url = URLBuilder.new_deck(shuffle=True)
    response = requests.get(url)
    deck_id = response.json()['deck_id']
    draw_url = URLBuilder.draw_cards(deck_id, count)
    draw_response = requests.get(draw_url)
    assert draw_response.status_code == 200
    draw_json = draw_response.json()

    if count == 0:
        assert draw_json['cards'] == []
    else:
        assert len(draw_json['cards']) == min(count, 52)

def test_draw_full_deck():
    """Test drawing all cards from a deck."""
    url = URLBuilder.new_deck(shuffle=True)
    response = requests.get(url)
    deck_id = response.json()['deck_id']
    draw_url = URLBuilder.draw_cards(deck_id, count=52)
    draw_response = requests.get(draw_url)
    assert draw_response.status_code == 200
    draw_json = draw_response.json()
    assert len(draw_json['cards']) == 52
    assert draw_json['remaining'] == 0

def test_return_cards_to_deck():
    """Test returning cards to the deck."""
    url = URLBuilder.new_deck(shuffle=True)
    response = requests.get(url)
    deck_id = response.json()['deck_id']
    draw_url = URLBuilder.draw_cards(deck_id, count=5)
    draw_response = requests.get(draw_url)
    drawn_cards = draw_response.json()['cards']
    codes = ",".join(card['code'] for card in drawn_cards)

    return_url = URLBuilder.return_to_deck(deck_id, codes)
    return_response = requests.get(return_url)
    assert return_response.status_code == 200
    return_json = return_response.json()
    assert return_json['success'] is True
    assert return_json['remaining'] == 52
