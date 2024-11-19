class URLBuilder:
    BASE_URL = "https://deckofcardsapi.com/api/deck"

    @staticmethod
    def new_deck(shuffle: bool = False, jokers_enabled: bool = False) -> str:
        """
        Constructs the URL for creating a new deck.
        Optionally includes parameters to shuffle the deck or add jokers.
        """
        url = f"{URLBuilder.BASE_URL}/new/"
        params = []
        if shuffle:
            params.append("shuffle=true")
        if jokers_enabled:
            params.append("jokers_enabled=true")
        if params:
            url += "?" + "&".join(params)
        return url

    @staticmethod
    def new_partial_deck(cards: str) -> str:
        """
        Constructs the URL for creating a partial deck with specified cards.
        Example cards string: "AS,2S,KH"
        """
        return f"{URLBuilder.BASE_URL}/new/?cards={cards}"

    @staticmethod
    def shuffle_deck(deck_id: str) -> str:
        """
        Constructs the URL to shuffle an existing deck.
        """
        if not deck_id:
            raise ValueError("deck_id is required to shuffle the deck")
        return f"{URLBuilder.BASE_URL}/{deck_id}/shuffle/"

    @staticmethod
    def reshuffle_deck(deck_id: str, remaining_only: bool = False) -> str:
        """
        Constructs the URL to reshuffle the deck.
        Optionally, reshuffle only remaining cards.
        """
        if not deck_id:
            raise ValueError("deck_id is required to reshuffle the deck")
        url = f"{URLBuilder.BASE_URL}/{deck_id}/shuffle/"
        if remaining_only:
            url += "?remaining=true"
        return url

    @staticmethod
    def draw_cards(deck_id: str, count: int = 1) -> str:
        """
        Constructs the URL to draw cards from the deck.
        """
        if not deck_id:
            raise ValueError("deck_id is required to draw cards")
        return f"{URLBuilder.BASE_URL}/{deck_id}/draw/?count={count}"

    @staticmethod
    def add_to_pile(deck_id: str, pile_name: str, cards: str) -> str:
        """
        Constructs the URL to add specific cards to a pile.
        """
        if not deck_id:
            raise ValueError("deck_id is required to add cards to a pile")
        return f"{URLBuilder.BASE_URL}/{deck_id}/pile/{pile_name}/add/?cards={cards}"

    @staticmethod
    def draw_from_pile(deck_id: str, pile_name: str, count: int = 1) -> str:
        """
        Constructs the URL to draw cards from a specified pile.
        """
        if not deck_id:
            raise ValueError("deck_id is required to draw from a pile")
        return f"{URLBuilder.BASE_URL}/{deck_id}/pile/{pile_name}/draw/?count={count}"

    @staticmethod
    def list_pile(deck_id: str, pile_name: str) -> str:
        """
        Constructs the URL to list all cards in a specified pile.
        """
        if not deck_id:
            raise ValueError("deck_id is required to list cards in a pile")
        return f"{URLBuilder.BASE_URL}/{deck_id}/pile/{pile_name}/list/"

    @staticmethod
    def shuffle_pile(deck_id: str, pile_name: str) -> str:
        """
        Constructs the URL to shuffle a specific pile within a deck.
        """
        if not deck_id:
            raise ValueError("deck_id is required to shuffle a pile")
        return f"{URLBuilder.BASE_URL}/{deck_id}/pile/{pile_name}/shuffle/"

    @staticmethod
    def return_to_deck(deck_id: str, cards: str) -> str:
        """
        Constructs the URL to return specific cards to the deck.
        """
        if not deck_id:
            raise ValueError("deck_id is required to return cards")
        return f"{URLBuilder.BASE_URL}/{deck_id}/return/?cards={cards}"
