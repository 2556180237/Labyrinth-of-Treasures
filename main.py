#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Главный файл игры 'Лабиринт сокровищ'."""

import sys

from constants import MESSAGES
from player_actions import PlayerActions
from utils import format_command, print_health, print_separator


class TreasureMazeGame:
    """Основной класс игры."""

    def __init__(self):
        self.player = PlayerActions()
        self.current_room = "start"
        self.running = True

    def start_game(self) -> None:
        """Запуск игры."""
        print_separator("=", 60)
        print("ЛАБИРИНТ СОКРОВИЩ")
        print_separator("=", 60)
        print(MESSAGES["welcome"])
        print_separator()

        # Показываем начальную комнату
        self.player.look(self.current_room)
        print_health(self.player.health, self.player.max_health)

        # Основной игровой цикл
        while self.running and not self.player.game_over and not self.player.victory:
            try:
                self._process_turn()
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                continue

    def _process_turn(self) -> None:
        """Обработка одного хода игрока."""
        try:
            command_input = input("\nВведите команду: ").strip()

            if not command_input:
                return

            command_parts = format_command(command_input)
            
            if not command_parts:
                return
                
            command = command_parts[0]

            # Обработка команд
            if command == "go":
                if len(command_parts) > 1:
                    direction = command_parts[1]
                    new_room = self.player.go(direction, self.current_room)
                    if new_room != self.current_room:
                        self.current_room = new_room
                        # Проверка ловушек в новой комнате
                        self.player.check_trap(self.current_room)
                        # Показ новой комнаты
                        if not self.player.game_over:
                            self.player.look(self.current_room)
                            print_health(self.player.health, self.player.max_health)
                else:
                    print("Ошибка: Укажите направление. Например: go north, go south, go east, go west")

            elif command == "look":
                self.player.look(self.current_room)

            elif command == "inventory":
                self.player.show_inventory()

            elif command == "take" and len(command_parts) > 1:
                item_name = " ".join(command_parts[1:])
                self.player.take(item_name, self.current_room)

            elif command == "use" and len(command_parts) > 1:
                item_name = " ".join(command_parts[1:])
                self.player.use(item_name, self.current_room)

            elif command == "solve":
                self.player.solve_puzzle(self.current_room)

            elif command == "help":
                self.player.show_help()

            elif command == "quit":
                self.player.quit_game()
                self.running = False

            else:
                print(f"Ошибка: {MESSAGES['invalid_command']}")

        except KeyboardInterrupt:
            print("\n\nИгра прервана пользователем.")
            self.running = False

        except EOFError:
            print("\n\nИгра завершена.")
            self.running = False

        except UnicodeDecodeError:
            print(f"\nОшибка: {MESSAGES['encoding_error']}")
            print(f"Подсказка: {MESSAGES['invalid_characters']}")

    def end_game(self) -> None:
        """Завершение игры."""
        if self.player.victory:
            print("\nПоздравляем с победой!")
        elif self.player.game_over:
            print("\nИгра окончена.")
        else:
            print("\nДо свидания!")


def main() -> None:
    """Главная функция."""
    try:
        game = TreasureMazeGame()
        game.start_game()
        game.end_game()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
