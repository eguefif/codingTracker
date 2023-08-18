TESTS = ./tests/test_language.py ./tests/test_process.py \
		./tests/test_filedata.py
SRC = ./codingTracker/client.py

.PHONY: test lint type checkall

test:
	pytest

lint:
	isort $(SRC)
	isort $(TESTS)
	black $(SRC)
	black  $(TESTS)
	flake8 $(SRC)
	flake8 $(TESTS)

type:
	mypy --no-strict-optional $(SRC)
	mypy --no-strict-optional $(TESTS)

checkall: lint type test
