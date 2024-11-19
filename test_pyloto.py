import unittest
from unittest.mock import patch
from pyloto import Barrel, Card, HumanPlayer, ComputerPlayer
from pyloto import Player, play_game, main


class TestBarrel(unittest.TestCase):
    def test_draw(self):
        barrel = Barrel()
        drawn_numbers = set()
        for _ in range(90):
            number = barrel.draw()
            self.assertNotIn(number, drawn_numbers)  # Проверяем, что номер не повторяется
            drawn_numbers.add(number)
        self.assertEqual(len(drawn_numbers), 90)  # Проверяем, что 90 уникальных номеров


class TestCard(unittest.TestCase):
    def test_card_initialization(self):
        card = Card()
        numbers = [cell for row in card.grid for cell in row if cell is not None]
        self.assertEqual(len(numbers), 15)  # В карточке ровно 15 номеров

    def test_mark_number(self):
        card = Card()
        # Найдем число в карточке
        number = next(cell for row in card.grid for cell in row if cell is not None)
        self.assertTrue(card.mark_number(number))  # Успешное зачёркивание
        self.assertFalse(card.mark_number(number))  # Номер уже зачёркнут

    def test_is_complete(self):
        card = Card()
        # Отметим все числа
        for row in card.grid:
            for cell in row:
                if cell is not None:
                    card.mark_number(cell)
        self.assertTrue(card.is_complete())  # Карточка завершена


class TestHumanPlayer(unittest.TestCase):
    @patch('builtins.input', side_effect=['y'])
    def test_make_move_correct_yes(self, mock_input):
        card = Card()
        player = HumanPlayer("Test Player", card)
        # Найдем число в карточке
        number = next(cell for row in card.grid for cell in row if cell is not None)
        self.assertTrue(player.make_move(number))  # Ход успешен

    @patch('builtins.input', side_effect=['n'])
    def test_make_move_correct_no(self, mock_input):
        card = Card()
        player = HumanPlayer("Test Player", card)
        # Число отсутствует
        self.assertTrue(player.make_move(100))  # Ход успешен


class TestComputerPlayer(unittest.TestCase):
    def test_make_move(self):
        card = Card()
        player = ComputerPlayer("Test Computer", card)
        # Найдем число в карточке
        number = next(cell for row in card.grid for cell in row if cell is not None)
        self.assertTrue(player.make_move(number))  # Ход успешен


class TestPlayer(unittest.TestCase):
    def test_make_move_not_implemented(self):
        card = Card()
        player = Player("TestPlayer", card)
        with self.assertRaises(NotImplementedError):
            player.make_move(10)


class TestHumanPlayer(unittest.TestCase):
    @patch('builtins.input', return_value='y')
    def test_make_move_valid_input_yes(self, mock_input):
        card = Card()
        card.grid[0][0] = 10
        player = HumanPlayer("TestHuman", card)
        self.assertTrue(player.make_move(10))

    @patch('builtins.input', return_value='n')
    def test_make_move_valid_input_no(self, mock_input):
        card = Card()
        card.grid[0][0] = 10
        player = HumanPlayer("TestHuman", card)
        self.assertTrue(player.make_move(99))  # Не пытается зачеркнуть отсутствующий номер

    @patch('builtins.input', side_effect=['x', 'y'])
    def test_make_move_invalid_input(self, mock_input):
        card = Card()
        card.grid[0][0] = 10
        player = HumanPlayer("TestHuman", card)
        self.assertTrue(player.make_move(10))  # После некорректного ввода продолжает нормально


class TestComputerPlayer(unittest.TestCase):
    def test_make_move(self):
        card = Card()
        card.grid[0][0] = 10
        player = ComputerPlayer("TestComputer", card)
        self.assertTrue(player.make_move(10))  # Успешно зачеркивает существующий номер
        self.assertTrue(player.make_move(99))  # Пропускает отсутствующий номер


class TestPlayGame(unittest.TestCase):
    @patch('builtins.input', return_value='y')
    @patch('pyloto.Barrel.draw', side_effect=[10, 99])  # Первое число на карте, второе нет
    def test_play_game_human_vs_computer(self, mock_draw, mock_input):
        human_card = Card()
        human_card.grid[0][0] = 10
        computer_card = Card()
        computer_card.grid[0][0] = 10

        players = [
            HumanPlayer("Human", human_card),
            ComputerPlayer("Computer", computer_card)
        ]
        play_game(players)


class TestMain(unittest.TestCase):
    @patch('builtins.input', return_value='1')
    @patch('pyloto.play_game', return_value=None)
    def test_main_human_vs_computer(self, mock_play_game, mock_input):
        main()
        mock_play_game.assert_called_once()

    @patch('builtins.input', return_value='invalid')
    def test_main_invalid_input(self, mock_input):
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_any_call("Неправильный ввод!")



if __name__ == "__main__":
    unittest.main()
