# -*- coding: utf-8 -*-
"""Вспомогательные функции для игры 'Лабиринт сокровищ'."""

import random
from typing import Any, Dict, List

from constants import GAME_SETTINGS, RANDOM_EVENTS


def print_separator(char: str = "=", length: int = 50) -> None:
    """Печатает разделитель для лучшей читаемости."""
    print(char * length)


def print_room_info(room_data: Dict[str, Any]) -> None:
    """Печатает информацию о текущей комнате."""
    print_separator()
    print(f"=== {room_data['name']} ===")
    print_separator("-")
    print(room_data["description"])

    if room_data["exits"]:
        exits = ", ".join(room_data["exits"].keys())
        print(f"\nВыходы: {exits}")

    if room_data["items"]:
        items = ", ".join(room_data["items"])
        print(f"Предметы: {items}")

    if room_data.get("has_puzzle", False):
        print("Здесь есть загадка!")

    if room_data.get("has_trap", False):
        print("Осторожно! Здесь могут быть ловушки!")


def print_inventory(inventory: List[str]) -> None:
    """Печатает содержимое инвентаря игрока."""
    print_separator()
    print("ИНВЕНТАРЬ")
    print_separator("-")

    if not inventory:
        print("Инвентарь пуст.")
    else:
        for i, item in enumerate(inventory, 1):
            print(f"{i}. {item}")


def print_help() -> None:
    """Печатает справку по командам."""
    from constants import COMMANDS

    print_separator()
    print("СПРАВКА ПО КОМАНДАМ")
    print_separator("-")

    for command, description in COMMANDS.items():
        print(f"• {description}")


def check_random_event() -> bool:
    """Проверяет, должно ли произойти случайное событие."""
    return random.random() < GAME_SETTINGS["random_event_chance"]


def trigger_random_event() -> None:
    """Запускает случайное событие."""
    event = random.choice(RANDOM_EVENTS)
    print(f"\n{event}")


def format_command(input_text: str) -> List[str]:
    """Форматирует введенную команду."""
    return input_text.strip().lower().split()


def validate_direction(direction: str) -> bool:
    """Проверяет, является ли строка валидным направлением."""
    from constants import DIRECTIONS

    return direction in DIRECTIONS


def get_standard_direction(direction: str) -> str:
    """Возвращает стандартное направление (на английском)."""
    from constants import DIRECTIONS

    return DIRECTIONS.get(direction, direction)


def print_health(health: int, max_health: int) -> None:
    """Печатает текущее здоровье игрока."""
    hearts = "[*]" * health + "[ ]" * (max_health - health)
    print(f"Здоровье: {hearts} ({health}/{max_health})")


def print_game_over() -> None:
    """Печатает сообщение о завершении игры."""
    from constants import MESSAGES

    print_separator("=", 60)
    print(MESSAGES["game_over"])
    print_separator("=", 60)


def print_victory() -> None:
    """Печатает сообщение о победе."""
    from constants import MESSAGES

    print_separator("=", 60)
    print(MESSAGES["victory"])
    print_separator("=", 60)
