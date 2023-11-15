from abc import ABC, abstractmethod
from typing import Optional, List
from pydantic import BaseModel, validator
import uuid
from game_engine import GameEngine

class ShipPlacement(BaseModel):
    ship_type: str
    start: dict  # {"row": int, "column": str}
    direction: str

    @validator("start")
    def validate_start(cls, start):
        row, column = start.get("row"), start.get("column")

        if not (1 <= row <= 10):
            raise ValueError("Row must be between 1 and 10 inclusive.")

        if column not in list("ABCDEFGHIJ"):
            raise ValueError("Column must be one of A, B, C, D, E, F, G, H, I, J.")

        return start

class Turn(BaseModel):
    target: dict  # {"row": int, "column": str}

class TurnResponse(BaseModel):
    result: str
    ship_type: Optional[str]  # This would be None if the result is a miss

class GameStatus(BaseModel):
    is_game_over: bool
    winner: Optional[str]

class Game(BaseModel):
    game_id: str
    players: List[str]
    board: dict  # This could represent the state of the game board, you might need to flesh this out further
    engine: any  # The game engine that handles the game logics
    turns: List[Turn]  # List of turns that have been taken

class AbstractBattleship(ABC):
    SHIP_LENGTHS = {
        "carrier": 5,
        "battleship": 4,
        "cruiser": 3,
        "submarine": 3,
        "destroyer": 2,
    }

    @abstractmethod
    def create_ship_placement(self, game_id: str, placement: ShipPlacement) -> None:
        pass

    @abstractmethod
    def create_turn(self, game_id: str, turn: Turn) -> TurnResponse:
        pass

    @abstractmethod
    def get_game_status(self, game_id: str) -> GameStatus:
        pass

    @abstractmethod
    def get_winner(self, game_id: str) -> str:
        pass

    @abstractmethod
    def get_game(self, game_id: str) -> Game:
        pass

    @abstractmethod
    def delete_game(self, game_id: str) -> None:
        pass

    @abstractmethod
    def create_game(self, players: List[str]) -> str:
        pass

class Battleship(AbstractBattleship):
    def __init__(self):
        self.games = {}  # Store the state of all games

    def create_game(self, players: List[str]) -> str:
        game_id = str(uuid.uuid4())
        self.games[game_id] = Game(
            game_id=game_id,
            players=players,
            board=self.init_board(),
            engine=self.create_engine(players),
            turns=[],
        )
        return game_id

    @staticmethod
    def init_board() -> dict:
        return {f"{i}{j}": None for i in range(1, 11) for j in "ABCDEFGHIJ"}

    @staticmethod
    def create_engine(players):
        return GameEngine(players)

    def get_game(self, game_id: str) -> Game:
        return self.games.get(game_id)

    def delete_game(self, game_id: str) -> None:
        try:
            del self.games[game_id]
            return "Game Deleted Successfully!"
        except KeyError:
            return "Invalid Game ID!"

    def create_ship_placement(self, game_id: str, placement: ShipPlacement) -> None:
        # Validate the placement
        placement = ShipPlacement(**placement.dict())
        game = self.get_game(game_id)
        game.engine.place_ship(game.board, placement)

    def create_turn(self, game_id:str, turn:Turn) -> TurnResponse:
        turn = Turn(**turn.dict())
        game = self.get_game(game_id)
        result = game.engine.take_turn(game.board, turn)
        game.turns.append(turn)
        return TurnResponse(**result)

    def get_game_status(self, game_id:str) -> GameStatus:
        game = self.get_game(game_id)
        return GameStatus(
            is_game_over=game.engine.is_game_over(game.board),
            winner=game.engine.get_winner()
        )

    def get_winner(self, game_id:str) -> str:
        game = self.get_game(game_id)
        if game:
            return game.engine.get_winner()
        else:
            return "Invalid Game ID!"

    def get_game_state(self, game_id: str) -> Game:
        game = self.get_game(game_id)
        if game:
            return game
        else:
            return "Invalid Game ID!"

    def reset_game(self, game_id:str) -> str:
        del self.games[game_id]
        return "Game reset Successful!"