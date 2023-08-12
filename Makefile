TESTS = ./test/test.py 
SRC = ./codingTracker/client.py

.PHONY: test lint type checkall

test:
	pytest

lint:
	isort $(SRC) $(TEST)
	black $(SRC) $(TEST)
	flake8 $(SRC) $(TEST)

type:
	mypy $(SRC)

checkall: lint type test
