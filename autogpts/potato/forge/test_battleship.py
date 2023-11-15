import random

import openai
import asyncio
from forge.agent import ForgeAgent


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    task = ('Build a battleship game\n'
            '\n'
            'Specifications:\n'
            '\n'
            'Overview: Battleship is a two-player strategy game where each '
            'player places their fleet of ships on a grid and tries to sink '
            "the opponent's fleet by guessing their locations.\n"
            'Players take turns calling out a row and column, attempting to '
            "name a square containing one of the opponent's ships.\n"
            '\n'
            "The Grid: Each player's grid is a 10x10 grid, identified by rows "
            '(using numbers 1-10) and columns (using letters A-J).\n'
            '\n'
            'Ships:\n'
            '\n'
            'Carrier - 5 squares\n'
            'Battleship - 4 squares\n'
            'Cruiser - 3 squares\n'
            'Submarine - 3 squares\n'
            'Destroyer - 2 squares\n'
            'Each ship occupies contiguous squares on the grid, arranged '
            'either horizontally or vertically.\n'
            '\n'
            'Setup:\n'
            '\n'
            'At the start of the game, each player places their fleet on '
            'their grid. This setup is hidden from the opponent.\n'
            'The game begins with Player 1, followed by Player 2, and so on.\n'
            'Taking Turns:\n'
            '\n'
            'On a player\'s turn, they announce a grid square (e.g., "D5").\n'
            'The opponent announces whether that square is a "hit" (if '
            'there\'s a part of a ship on that square) or "miss" (if the '
            'square is empty).\n'
            'If a player hits a square occupied by a ship, they get another '
            'turn to guess. This continues until they make a miss, at which '
            'point their turn ends.\n'
            'If a player hits all the squares occupied by a ship, the '
            'opponent must announce the sinking of that specific ship, e.g., '
            '"You sank my Battleship!"\n'
            '\n'
            "Objective: The goal is to sink all of your opponent's ships "
            'before they sink yours.\n'
            '\n'
            'End of the Game: The game ends when one player has sunk all of '
            "the opponent's ships. The winner is the player who sinks all the "
            'opposing fleet first.\n'
            '\n'
            'Technical details:\n'
            'In your root folder you will find an abstract class that defines '
            'the public interface of the Battleship class you will have to '
            'build:\n'
            '```\n'
            'from abc import ABC, abstractmethod\n'
            'from typing import Optional\n'
            '\n'
            'from pydantic import BaseModel, validator\n'
            '\n'
            '\n'
            '# Models for the request and response payloads\n'
            'class ShipPlacement(BaseModel):\n'
            '    ship_type: str\n'
            '    start: dict  # {"row": int, "column": str}\n'
            '    direction: str\n'
            '\n'
            '    @validator("start")\n'
            '    def validate_start(cls, start):\n'
            '        row, column = start.get("row"), start.get("column")\n'
            '\n'
            '        if not (1 <= row <= 10):\n'
            '            raise ValueError("Row must be between 1 and 10 '
            'inclusive.")\n'
            '\n'
            '        if column not in list("ABCDEFGHIJ"):\n'
            '            raise ValueError("Column must be one of A, B, C, D, '
            'E, F, G, H, I, J.")\n'
            '\n'
            '        return start\n'
            '\n'
            '\n'
            'class Turn(BaseModel):\n'
            '    target: dict  # {"row": int, "column": str}\n'
            '\n'
            '\n'
            'class TurnResponse(BaseModel):\n'
            '    result: str\n'
            '    ship_type: Optional[str]  # This would be None if the result '
            'is a miss\n'
            '\n'
            '\n'
            'class GameStatus(BaseModel):\n'
            '    is_game_over: bool\n'
            '    winner: Optional[str]\n'
            '\n'
            '\n'
            'from typing import List\n'
            '\n'
            '\n'
            'class Game(BaseModel):\n'
            '    game_id: str\n'
            '    players: List[str]\n'
            '    board: dict  # This could represent the state of the game '
            'board, you might need to flesh this out further\n'
            '    ships: List[ShipPlacement]  # List of ship placements for '
            'this game\n'
            '    turns: List[Turn]  # List of turns that have been taken\n'
            '\n'
            '\n'
            'class AbstractBattleship(ABC):\n'
            '    SHIP_LENGTHS = {\n'
            '        "carrier": 5,\n'
            '        "battleship": 4,\n'
            '        "cruiser": 3,\n'
            '        "submarine": 3,\n'
            '        "destroyer": 2,\n'
            '    }\n'
            '\n'
            '    @abstractmethod\n'
            '    def create_ship_placement(self, game_id: str, placement: '
            'ShipPlacement) -> None:\n'
            '        """\n'
            '        Place a ship on the grid.\n'
            '        """\n'
            '        pass\n'
            '\n'
            '    @abstractmethod\n'
            '    def create_turn(self, game_id: str, turn: Turn) -> '
            'TurnResponse:\n'
            '        """\n'
            '        Players take turns to target a grid cell.\n'
            '        """\n'
            '        pass\n'
            '\n'
            '    @abstractmethod\n'
            '    def get_game_status(self, game_id: str) -> GameStatus:\n'
            '        """\n'
            "        Check if the game is over and get the winner if there's "
            'one.\n'
            '        """\n'
            '        pass\n'
            '\n'
            '    @abstractmethod\n'
            '    def get_winner(self, game_id: str) -> str:\n'
            '        """\n'
            '        Get the winner of the game.\n'
            '        """\n'
            '        pass\n'
            '\n'
            '    @abstractmethod\n'
            '    def get_game(self) -> Game:\n'
            '        """\n'
            '        Retrieve the state of the game.\n'
            '        """\n'
            '        pass\n'
            '\n'
            '    @abstractmethod\n'
            '    def delete_game(self, game_id: str) -> None:\n'
            '        """\n'
            '        Delete a game given its ID.\n'
            '        """\n'
            '        pass\n'
            '\n'
            '    @abstractmethod\n'
            '    def create_game(self) -> None:\n'
            '        """\n'
            '        Create a new game.\n'
            '        """\n'
            '        pass\n'
            '\n'
            '```\n'
            'At any moment you can run ```pytest``` to execute the tests.\n'
            'You have two types of test: \n'
            '- positive tests => test the battleship game being used in ideal '
            'conditions\n'
            '- negative tests => tests the battleship game behaviour when '
            'used incorrectly\n'
            '\n'
            'Success criteria:\n'
            '- you will need to write a file called battleship.py that '
            'implements the abstract Battleship class.\n'
            '- this class will have to pass all the tests.\n'
            "- you're not allowed to modify any other file than the "
            'battleship.py. You can add other files as long as the main '
            'entrypoint is the battleship class.')

    # read battleship.py as string
    with open("/home/serg-v/AutoGPT/autogpts/potato/forge/battleship2.py", "r") as f:
        file_content = f.read()

    print("#####")
    print("Task:")
    print(task)
    print("#####")
    print("File content:")
    print(file_content)

    model = "gpt-3.5-turbo-0613"
    model = "gpt-4-0613"

    messages = [
        {'content': 'Review following output and task', 'role': 'system'},
        {'content': "Task is:\n" + task, 'role': 'user'},
        {'content': 'battleship.py:\n' + file_content, 'role': 'user'},
        {'content': 'fix problems in battelship.py and print new version, '
                    'complete incomplete functions, '
                    'replace pass to actual content.'
                    'Implement all placeholders and do not leave new', 'role': 'user'}
    ]
    print('############')
    print("Model generate:")
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    response = response["choices"][0]["message"]
    print(response["content"])
    messages + [response, {'content': 'now rewrite file if changes required', 'role': 'system'}]

    print('############')
    print("Model runs function:")
    agent = ForgeAgent(None, None)
    functions = agent.abilities.list_abilities_functions()
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=functions,
        function_call={"name": "write_file"},
    )
    function_call = response["choices"][0]["message"].get("function_call")
    asyncio.run(agent.run_ability("test", function_call))



run_conversation()
