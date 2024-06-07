from dataclasses import dataclass

from main import Hand, Card


# from collections import namedtuple

@dataclass
class Player:
    name: str
    hand: Hand
    finished: bool = False


player = Player(
    name="com1",
    hand=Hand(initial_cards=[Card(1), Card(2)]),
)
print(player.name)
print(player.hand)
print(player.finished)
