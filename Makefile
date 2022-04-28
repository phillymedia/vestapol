.PHONY: build push

IMAGE_TAG ?= latest

help:
	@echo "Makefile Help"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: clean-docker  ## clean up all artifacts

clean-docker:  ## stop docker containers and remove them
	IMAGE_TAG=${IMAGE_TAG} docker-compose down
	IMAGE_TAG=${IMAGE_TAG} docker-compose rm

clean-min: clean-pyc clean-test clean-docs ## clean up non-docker artifacts

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -fr .pytest_cache

build: clean  ## build the docker image
	IMAGE_TAG=${IMAGE_TAG} docker-compose -f docker-compose.yml build vestapol

build-test-container:
	@IMAGE_TAG=${IMAGE_TAG} docker-compose build vestapol-test

ci-test: clean-min build-test-container
	@IMAGE_TAG=${IMAGE_TAG} docker-compose run --rm vestapol-test
	docker-compose down

ci-release: clean-min build-release-container
	@IMAGE_TAG=${IMAGE_TAG} docker-compose up --exit-code-from=vestapol vestapol

build-release-container:
	@IMAGE_TAG=${IMAGE_TAG} docker-compose build vestapol

push: clean  ## push the docker image
	IMAGE_TAG=${IMAGE_TAG} docker-compose -f docker-compose.yml push vestapol

install: clean
	echo "Install package to activate python's site-packages"
	python setup.py install

dist: install
	python setup.py

test: clean-min ## run tests and linting (flake8, mypy, black), includes warehouse tests
	black vestapol/ tests/  --check
	flake8 vestapol/ tests/
	pytest tests/

