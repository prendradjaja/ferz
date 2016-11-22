.PHONY: typecheck

typecheck:
	mypy command_parser.py commands.py constants.py ferz.py filters.py game.py table_display.py utils.py wazir.py
