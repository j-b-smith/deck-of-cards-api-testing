import requests
from url_builder import URLBuilder


class DeckProvider:
    @staticmethod
    def _handle_response(response):
        """
        Handles the API response, raising exceptions for HTTP errors and logging API errors.
        """
        try:
            response.raise_for_status()  # Raises HTTPError for non-200 status codes
            response_json = response.json()
            if not response_json.get("success", True):  # Check for API-specific errors
                raise ValueError(f"API Error: {response_json}")
            return response_json
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"HTTP Error: {e}") from e
        except ValueError as e:
            raise RuntimeError(f"API Response Error: {e}") from e

    @staticmethod
    def create_deck(shuffle: bool = False, jokers_enabled: bool = False):
        url = URLBuilder.new_deck(shuffle=shuffle, jokers_enabled=jokers_enabled)
        response = requests.get(url)
        return DeckProvider._handle_response(response)["deck_id"]

    @staticmethod
    def shuffle_deck(deck_id: str):
        url = URLBuilder.shuffle_deck(deck_id)
        response = requests.get(url)
        return DeckProvider._handle_response(response)

    @staticmethod
    def draw_cards(deck_id: str, count: int = 1):
        url = URLBuilder.draw_cards(deck_id, count)
        response = requests.get(url)
        return DeckProvider._handle_response(response)

    @staticmethod
    def add_to_pile(deck_id: str, pile_name: str, cards: str):
        url = URLBuilder.add_to_pile(deck_id, pile_name, cards)
        response = requests.get(url)
        return DeckProvider._handle_response(response)

    @staticmethod
    def draw_from_pile(deck_id: str, pile_name: str, count: int = 1):
        url = URLBuilder.draw_from_pile(deck_id, pile_name, count)
        response = requests.get(url)
        return DeckProvider._handle_response(response)

    @staticmethod
    def list_pile(deck_id: str, pile_name: str):
        url = URLBuilder.list_pile(deck_id, pile_name)
        response = requests.get(url)
        return DeckProvider._handle_response(response)

    @staticmethod
    def return_to_deck(deck_id: str, cards: str):
        url = URLBuilder.return_to_deck(deck_id, cards)
        response = requests.get(url)
        return DeckProvider._handle_response(response)
