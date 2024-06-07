import time
from abc import ABCMeta, abstractmethod
import random


class Card:  # [3]
    def __init__(self, num: int):
        self.__num: int = num

    @classmethod
    def create_random(cls):
        num = random.randint(1, 10)
        return Card(num)

    def get_value(self) -> int:
        return self.__num

    def __str__(self):
        return f"[{self.__num}]"


class Hand:
    def __init__(self, initial_cards: list[Card]):
        self.__cards: list[Card] = initial_cards

    def add_card(self, card: Card):
        self.__cards.append(card)

    def total(self) -> int:
        return sum(card.get_value() for card in self.__cards)

    def __str__(self):
        return " ".join(str(card) for card in self.__cards) + f" = {self.total()}"


class Player(metaclass=ABCMeta):  # 抽象クラス
    def __init__(self, name: str, hand: Hand):
        self._name = name
        self._hand = hand
        self._finished = False

    @abstractmethod  # 抽象メソッド
    def action(self) -> bool:  # つぎカードをひく場合はTrueを返す
        raise NotImplementedError()

    @abstractmethod  # 抽象メソッド
    def show_draw_result(self):
        raise NotImplementedError()

    # @property
    # def name(self) -> str:
    #     return self._name

    def get_name(self) -> str:
        return self._name

    def get_hand(self) -> Hand:
        return self._hand

    def draw_random(self):
        self._hand.add_card(Card.create_random())

    def set_finished(self):  # ひき終わらせる
        self._finished = True

    def get_finished(self):  # ひき終わったかどうかを返す
        return self._finished

    def get_score(self) -> int | None:  # int: 戦える合計値 None: バーストしたとき
        if self._hand.total() > 21:
            return None
        return self._hand.total()


class PlayerCOM(Player):
    def action(self) -> bool:
        return self._hand.total() <= 16

    def show_draw_result(self):
        pass


class PlayerHuman(Player):
    def action(self) -> bool:
        print("ひきますか？")
        return input("y/n > ") == "y"

    def show_draw_result(self):
        print(self._hand)


class Game:
    def __init__(self, players: list[Player]):
        self._players: list[Player] = players

    @classmethod
    def create_initial_hand(cls) -> Hand:
        cards = [Card.create_random() for _ in range(2)]
        return Hand(cards)

    @classmethod
    def create_from_player_names(cls, player_names: list[str]):
        players: list[Player] = []
        for player_name in player_names:
            if player_name.startswith("com"):
                players.append(PlayerCOM(
                    name=player_name,
                    hand=Game.create_initial_hand(),
                ))
            else:
                players.append(PlayerHuman(
                    name=player_name,
                    hand=Game.create_initial_hand(),
                ))
        return Game(players=players)

    def step(self):
        for player in self._players:
            print()
            print("あなたの番です:", player.get_name())
            print("手札：", player.get_hand())
            if not player.get_finished():
                if player.action():  # ひく
                    player.draw_random()
                    player.show_draw_result()
                    if player.get_score() is None:  # バースト
                        print("バースト！")
                        player.set_finished()
                else:  # ひかない
                    player.set_finished()
            time.sleep(1)

    def is_all_finished(self) -> bool:
        return all(player.get_finished() for player in self._players)

    def get_winners(self) -> list[Player]:
        valid_player_and_sore_lst: list[tuple[int, Player]] = []
        for player in self._players:
            score: int | None = player.get_score()
            if score is None:
                continue
            valid_player_and_sore_lst.append((score, player))

        max_score = max(score for score, player in valid_player_and_sore_lst)

        return [
            player
            for score, player in valid_player_and_sore_lst
            if score == max_score
        ]

    def show_player_info(self, i):
        print(f" ===== ターン {i + 1} =====")
        for player in self._players:
            print(player.get_name().ljust(10), " ",
                  "終わり" if player.get_finished() else "まだ")

    def show_winners(self):
        winners: list[Player] = self.get_winners()
        print("勝者！")
        for winner in winners:
            print(f" - {winner.get_name()}")

    def start(self):
        i = 0
        while True:
            self.show_player_info(i)
            if self.is_all_finished():
                break
            self.step()
            i += 1
        self.show_winners()


def main():
    game = Game.create_from_player_names(["p1", "p2", "com1", "com2"])
    game.start()


if __name__ == '__main__':
    main()
