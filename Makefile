clean:
	find . -name *.pyc -delete

lint:
	which pyflakes >/dev/null || pip install --use-mirrors pyflakes
	arc lint

test: clean
	python setup.py nosetests

test-matrix: clean
	which tox >/dev/null || pip install --use-mirrors tox
	tox

.PHONY: clean test test-matrix lint
