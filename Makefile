.PHONY: build push

IMAGE_TAG ?= latest

help:
	@echo "Makefile Help"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean-test:
	rm -fr .tox/
	rm -fr .pytest_cache

build: ## build the docker image
	IMAGE_TAG=${IMAGE_TAG} docker-compose -f docker-compose.yml build vestapol

build-test-container:
	@IMAGE_TAG=${IMAGE_TAG} docker-compose build vestapol-test

push: clean  ## push the docker image
	IMAGE_TAG=${IMAGE_TAG} docker-compose -f docker-compose.yml push vestapol

test: clean-min ## run tests and linting (flake8, mypy, black), includes warehouse tests
	black vestapol/ tests/  --check
	flake8 vestapol/ tests/
	pytest tests/

