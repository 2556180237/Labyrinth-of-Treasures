.PHONY: install project lint build clean run format

install:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e ".[dev]"

project:
	@echo "Проект уже инициализирован"

lint:
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .

format:
	.venv/bin/ruff format .

build:
	.venv/bin/python -m build

clean:
	rm -rf dist/
	rm -rf .venv/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

run:
	.venv/bin/python main.py

test:
	.venv/bin/python -m pytest tests/ -v

help:
	@echo "Доступные команды:"
	@echo "  install  - Установить зависимости"
	@echo "  project  - Инициализировать проект"
	@echo "  lint     - Проверить код линтером"
	@echo "  format   - Форматировать код"
	@echo "  build    - Собрать проект"
	@echo "  run      - Запустить игру"
	@echo "  clean    - Очистить временные файлы"
	@echo "  test     - Запустить тесты"
	@echo "  help     - Показать эту справку"
