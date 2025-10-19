# -*- coding: utf-8 -*-
"""Действия игрока в игре 'Лабиринт сокровищ'."""

import random
from typing import Any, Dict, List

from constants import GAME_SETTINGS, ITEMS, MESSAGES, ROOMS
from utils import (
    check_random_event,
    get_standard_direction,
    print_health,
    print_help,
    print_inventory,
    print_room_info,
    print_victory,
    trigger_random_event,
    validate_direction,
)


class PlayerActions:
    """Класс для обработки действий игрока."""

    def __init__(self):
        self.inventory: List[str] = []
        self.health: int = GAME_SETTINGS["max_health"]
        self.max_health: int = GAME_SETTINGS["max_health"]
        self.solved_puzzles: set = set()
        self.game_over: bool = False
        self.victory: bool = False

    def go(self, direction: str, current_room: str) -> str:
        """Перемещение игрока в указанном направлении."""
        if not validate_direction(direction):
            print(f"Ошибка: {MESSAGES['invalid_direction']}")
            return current_room

        standard_direction = get_standard_direction(direction)
        room_data = ROOMS[current_room]

        if standard_direction not in room_data["exits"]:
            print(f"Ошибка: {MESSAGES['invalid_direction']}")
            return current_room

        new_room = room_data["exits"][standard_direction]
        print(f"Вы идете на {direction}...")

        # Проверка случайного события
        if check_random_event():
            trigger_random_event()

        return new_room

    def look(self, current_room: str) -> None:
        """Осмотр текущей комнаты."""
        room_data = ROOMS[current_room]
        print_room_info(room_data)

    def show_inventory(self) -> None:
        """Показ инвентаря игрока."""
        print_inventory(self.inventory)

    def take(self, item_name: str, current_room: str) -> None:
        """Взятие предмета."""
        room_data = ROOMS[current_room]

        if item_name not in room_data["items"]:
            print(f"Ошибка: {MESSAGES['no_item']}")
            return

        self.inventory.append(item_name)
        room_data["items"].remove(item_name)
        print(f"Вы взяли: '{item_name}'")

    def use(self, item_name: str, current_room: str) -> None:
        """Использование предмета."""
        if item_name not in self.inventory:
            print(f"У вас нет предмета '{item_name}'")
            return

        if item_name not in ITEMS:
            print(f"Неизвестный предмет '{item_name}'")
            return

        item_data = ITEMS[item_name]

        if not item_data["usable"]:
            print(f"{item_data['use_description']}")
            return

        # Специальная логика для ключа
        if item_name == "ключ" and current_room == "treasure_room":
            self._use_key()
            return

        # Специальная логика для магического кристалла
        if item_name == "магический кристалл":
            self._use_crystal()
            return

        print(f"Вы использовали: '{item_name}'")
        print(f"{item_data['use_description']}")

    def _use_key(self) -> None:
        """Использование ключа для открытия сундука."""
        print("Ключ идеально подходит к замку!")
        print("Сундук открывается с громким скрипом...")
        print("Внутри вы видите горы золота и драгоценных камней!")
        self.victory = True
        print_victory()

    def _use_crystal(self) -> None:
        """Использование магического кристалла."""
        print("Магический кристалл начинает светиться!")
        print("Вы чувствуете, как магическая сила пронизывает ваше тело!")
        print("Кристалл растворяется в воздухе, но вы чувствуете себя победителем!")
        self.victory = True
        print_victory()

    def solve_puzzle(self, current_room: str) -> None:
        """Решение загадки."""
        room_data = ROOMS[current_room]

        if not room_data.get("has_puzzle", False):
            print(f"Ошибка: {MESSAGES['no_puzzle']}")
            return

        if current_room in self.solved_puzzles:
            print(f"Ошибка: {MESSAGES['already_solved']}")
            return

        print(f"Загадка: {room_data['puzzle_question']}")
        answer = input("Ваш ответ: ").strip().lower()

        if answer == room_data["puzzle_answer"]:
            print(f"Правильно! {MESSAGES['puzzle_solved']}")
            reward = room_data["puzzle_reward"]
            self.inventory.append(reward)
            print(f"Вы получили: {reward}")
            self.solved_puzzles.add(current_room)
        else:
            print("Неправильный ответ. Попробуйте еще раз.")

    def check_trap(self, current_room: str) -> None:
        """Проверка и срабатывание ловушки."""
        room_data = ROOMS[current_room]

        if not room_data.get("has_trap", False):
            return

        # 50% шанс срабатывания ловушки
        if random.random() < 0.5:
            damage = room_data.get("trap_damage", GAME_SETTINGS["trap_damage"])
            self.health -= damage
            print(f"Ловушка! {MESSAGES['trap_triggered']}")
            print(f"Вы потеряли {damage} единицу здоровья!")
            print_health(self.health, self.max_health)

            if self.health <= 0:
                self.game_over = True
                from utils import print_game_over

                print_game_over()

    def quit_game(self) -> None:
        """Выход из игры."""
        print(f"{MESSAGES['game_ended']}")
        self.game_over = True

    def show_help(self) -> None:
        """Показ справки."""
        print_help()

    def get_status(self) -> Dict[str, Any]:
        """Получение текущего статуса игрока."""
        return {
            "health": self.health,
            "max_health": self.max_health,
            "inventory": self.inventory.copy(),
            "game_over": self.game_over,
            "victory": self.victory,
        }
