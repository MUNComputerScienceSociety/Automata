from typing import List

from .deck_of_cards_api import DeckOfCardsApi, CardResponse


class Deck:
    @classmethod
    async def create(self, *args):
        api_deck = await DeckOfCardsApi.new_deck(*args)
        return Deck(api_deck)

    def __init__(self, api_deck):
        self.deck_id = api_deck.deck_id
        self.shuffled = api_deck.shuffled
        self.remaining = api_deck.remaining

    async def draw(self, *args) -> List[CardResponse]:
        api_deck_draw = await DeckOfCardsApi.deck_draw(self.deck_id, *args)
        self.remaining = api_deck_draw.remaining
        return api_deck_draw.cards


if __name__ == "__main__":

    async def main():
        deck = await Deck.create()
        cards = await deck.draw()
        print(cards)

    __import__("asyncio").get_event_loop().run_until_complete(main())
