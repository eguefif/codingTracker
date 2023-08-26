TESTS = ./tests/test_process.py \
		./tests/test_data.py \
		./tests/test_server.py
SRC = ./codingTracker/client.py ./codingTracker/datahandler.py \
	  ./codingTracker/connexion.py ./codingTracker/process.py \
	  ./codingTracker/server.py ./codingTracker/data.py
	

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
