.PHONY: test
test:
	pytest -p no:cacheprovider ./tests/

.PHONY: conf_test
conf_test:
	python ./mask/config/parser.py