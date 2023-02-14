.PHONY: test
test:
	pytest -p no:cacheprovider -v ./django_mask/tests/

.PHONY: conf_test
conf_test:
	python ./mask/config/parser.py