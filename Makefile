UNIT_TESTS = ./tests/test_process.py \
		./tests/test_data.py \
		./tests/test_connexion.py \
		./tests/test_filehandler.py \
		./tests/test_datahandler.py \
		./tests/test_client.py


SERVER_TESTS = ./tests/test_server.py

ACCEPTANCE_TESTS = ./tests/test_acceptance.py

SRC = ./codingTracker/client.py ./codingTracker/datahandler.py \
	  ./codingTracker/connexion.py ./codingTracker/process.py \
	  ./codingTracker/server.py ./codingTracker/data.py \
	  ./codingTracker/setup_app.py
	

.PHONY: test lint type checkall killserver docker

test:
	./tests/server_for_test.py &
	pytest -vv $(UNIT_TESTS)
	pgrep server_for | xargs kill
	codingTrackerServer &
	pytest -vv $(SERVER_TESTS)
	pgrep codingTrackerS | xargs kill

acceptance_test:
	pytest -vv $(ACCEPTANCE_TESTS)

killserver:
	pgrep server_for | xargs kill
	pgrep codingTrackerS | xargs kill
	

lint:
	isort $(SRC)
	isort $(UNIT_TESTS)
	isort $(SERVER_TESTS)
	isort $(ACCEPTANCE_TESTS)
	black $(SRC)
	black  $(UNIT_TESTS)
	black  $(SERVER_TESTS)
	black  $(ACCEPTANCE_TESTS)
	flake8 $(SRC)
	flake8 $(UNIT_TESTS)
	flake8 $(SERVER_TESTS)
	flake8 $(ACCEPTANCE_TESTS)

type:
	mypy --no-strict-optional $(SRC)
	mypy --no-strict-optional $(UNIT_TESTS)
	mypy --no-strict-optional $(SERVER_TESTS)
	mypy --no-strict-optional $(ACCEPTANCE_TESTS)

checkall: lint type test

docker:
	#docker buildx create --driver=docker-container --name=container
	docker buildx build --builder=container --platform=linux/amd64,linux/arm64,linux/arm/v7 -t eguefif/codingtracker:v0.0.2 --push .
