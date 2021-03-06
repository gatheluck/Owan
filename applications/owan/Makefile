TEST-WORKERS=2

.PHONY: run
run:
	poetry run gunicorn 'owan.wsgi:main()' -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

.PHONY: run-worker
run-worker:
	poetry run celery --app owan.worker worker --pool solo --concurrency 1

.PHONY: black
black:
	poetry run black --check owan tests

.PHONY: black-lint
black-lint:
	poetry run black owan tests

.PHONY: flake8
flake8:
	poetry run flake8 owan tests

.PHONY: isort
isort:
	poetry run isort --check-only owan tests

.PHONY: isort-lint
isort-lint:
	poetry run isort owan tests

.PHONY: mypy
mypy:
	poetry run mypy owan

.PHONY: test
test:
	poetry run pytest tests --cov=owan --cov-report term-missing --durations 5

.PHONY: lint
lint:
	$(MAKE) black-lint
	$(MAKE) isort-lint

.PHONY: test-all
test-all:
	$(MAKE) black
	$(MAKE) flake8
	$(MAKE) isort
	$(MAKE) mypy
	$(MAKE) test