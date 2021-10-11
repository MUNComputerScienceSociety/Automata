from dataclasses import dataclass
from typing import List

import httpx
from pydantic import BaseModel

API_BASE = "https://deckofcardsapi.com/api"


class NewDeckResponse(BaseModel):
    success: bool
    deck_id: str
    remaining: int
    shuffled: bool


class CardImagesResponse(BaseModel):
    svg: str
    png: str


class CardResponse(BaseModel):
    code: str
    image: str
    images: CardImagesResponse
    value: str
    suit: str


class DeckDrawResponse(BaseModel):
    success: bool
    deck_id: str
    remaining: int
    cards: List[CardResponse]


class DeckOfCardsApi(BaseModel):
    @staticmethod
    async def _fetch(api_path):
        async with httpx.AsyncClient() as client:
            return await client.get(f"{API_BASE}{api_path}")

    @staticmethod
    def _ensure_api_sucess(response_json):
        if not response_json["success"]:
            raise Exception("Deck of Cards API returned non-sucess")

    @staticmethod
    async def new_deck(shuffle=True, count=1) -> NewDeckResponse:
        api_path = "/deck/new"

        if shuffle:
            api_path += "/shuffle"

        api_path += f"?deck_count={count}"

        response = await DeckOfCardsApi._fetch(api_path)
        response_json = response.json()
        DeckOfCardsApi._ensure_api_sucess(response_json)

        return NewDeckResponse(**response_json)

    @staticmethod
    async def deck_draw(deck_id, count=1) -> DeckDrawResponse:
        api_path = f"/deck/{deck_id}/draw/?count={count}"

        response = await DeckOfCardsApi._fetch(api_path)
        response_json = response.json()
        DeckOfCardsApi._ensure_api_sucess(response_json)

        return DeckDrawResponse(**response_json)


if __name__ == "__main__":

    async def main():
        deck = await DeckOfCardsApi.new_deck()
        print(deck)
        card = await DeckOfCardsApi.deck_draw(deck.deck_id)
        print(card)

    __import__("asyncio").get_event_loop().run_until_complete(main())
