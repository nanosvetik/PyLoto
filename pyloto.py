import random


class Barrel:
    def __init__(self):
        self.numbers = list(range(1, 91))
        random.shuffle(self.numbers)

    def draw(self):
        return self.numbers.pop()


class Card:
    def __init__(self):
        self.grid = [[None for _ in range(9)] for _ in range(3)]
        numbers = random.sample(range(1, 91), 15)
        for row in self.grid:
            row_numbers = sorted(numbers[:5])
            numbers = numbers[5:]
            for i in random.sample(range(9), 5):
                row[i] = row_numbers.pop(0)

    def mark_number(self, number):
        for row in self.grid:
            if number in row:
                row[row.index(number)] = '-'
                return True
        return False

    def is_complete(self):
        return all(cell == '-' for row in self.grid for cell in row if cell is not None)

    def __str__(self):
        result = '--------------------------\n'
        for row in self.grid:
            result += ' '.join(f'{cell:2}' if cell is not None else '  ' for cell in row) + '\n'
        result += '--------------------------'
        return result


class Player:
    def __init__(self, name, card):
        self.name = name
        self.card = card

    def make_move(self, barrel_number):
        raise NotImplementedError("This method should be implemented by subclasses")


class HumanPlayer(Player):
    def make_move(self, barrel_number):
        print(f"\n------ {self.name} ------")
        print(self.card)
        while True:
            move = input(f"Зачеркнуть цифру {barrel_number}? (y/n): ").strip().lower()
            if move not in ['y', 'n']:
                print("Неправильный ввод! Пожалуйста, введите 'y' для зачёркивания или 'n' для продолжения.")
                continue
            break
        if move == 'y':
            if not self.card.mark_number(barrel_number):
                print("Неправильный ход! Вы проиграли.")
                return False
        else:
            if self.card.mark_number(barrel_number):
                print("Неправильный ход! Вы проиграли.")
                return False
        return True


class ComputerPlayer(Player):
    def make_move(self, barrel_number):
        print(f"\n------ {self.name} ------")
        print(self.card)
        if self.card.mark_number(barrel_number):
            print(f"{self.name} зачеркнул цифру {barrel_number}.")
        else:
            print(f"{self.name} пропустил цифру {barrel_number}.")
        return True


def play_game(players):
    barrel = Barrel()
    while True:
        barrel_number = barrel.draw()
        print(f"\nНовый бочонок: {barrel_number} (осталось {len(barrel.numbers)})")
        for player in players:
            if not player.make_move(barrel_number):
                print(f"\n{player.name} проиграл!")
                return
            if player.card.is_complete():
                print(f"\n{player.name} победил!")
                return


def main():
    print("Добро пожаловать в игру Лото!")
    player_type = input(
        "Выберите тип игры (1: Человек против компьютера, 2: Человек против человека, 3: Компьютер против компьютера): ").strip()

    if player_type == '1':
        players = [HumanPlayer("Ваш ход", Card()), ComputerPlayer("Ход компьютера", Card())]
    elif player_type == '2':
        players = [HumanPlayer("Игрок 1", Card()), HumanPlayer("Игрок 2", Card())]
    elif player_type == '3':
        players = [ComputerPlayer("Компьютер 1", Card()), ComputerPlayer("Компьютер 2", Card())]
    else:
        print("Неправильный ввод!")
        return

    play_game(players)


if __name__ == "__main__":
    main()
