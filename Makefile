TESTS = ./tests/test_process.py \
		./tests/test_data.py
SRC = ./codingTracker/client.py ./codingTracker/datahandler.py \
	  ./codingTracker/connexion.py ./codingTracker/process.py \
	  ./codingTracker/server.py ./codingTracker/data.py
	

.PHONY: test lint type checkall

test:
	./tests/server_for_test.py &
	pytest
	pgrep server_for | xargs kill
	

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
