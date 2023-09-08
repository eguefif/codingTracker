UNIT_TESTS = ./tests/test_process.py \
		./tests/test_session.py
		#./tests/test_connexion.py \
		#./tests/test_filehandler.py \
		#./tests/test_datahandler.py \
		#./tests/test_client.py

SRC = ./codingTracker/process.py \
	  ./codingTracker/session.py
	  #./codingTracker/connexion.py
	  #./codingTracker/client.py
	  #./codingTracker/persistence.py
	  #./codingTracker/server.py
	  #./codingTracker/setup_app.py
	

.PHONY: test lint type checkall killserver docker

test:
	#./tests/server_for_test.py &
	pytest -vv $(UNIT_TESTS)
	#pgrep server_for | xargs kill
	#codingTrackerServer &
	#pytest -vv $(SERVER_TESTS)
	#pgrep codingTrackerS | xargs kill

acceptance_test:
	pytest -vv $(ACCEPTANCE_TESTS)

killserver:
	pgrep server_for | xargs kill
	pgrep codingTrackerS | xargs kill
	

lint:
	isort $(SRC)
	isort $(UNIT_TESTS)
	black $(SRC)
	black  $(UNIT_TESTS)
	flake8 $(SRC)
	flake8 $(UNIT_TESTS)

type:
	mypy --no-strict-optional $(SRC)
	mypy --no-strict-optional $(UNIT_TESTS)

checkall: lint type test

docker:
	#docker buildx create --driver=docker-container --name=container
	docker buildx build --builder=container --platform=linux/amd64,linux/arm64,linux/arm/v7 -t eguefif/codingtracker:v0.0.2 --push .
