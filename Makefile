TESTS = ./tests/test_language_tracker.py ./tests/test_processtracker_editorprocess.py \
		./tests/test_dataProcessing.py
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
