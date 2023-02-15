.PHONY: test
test:
	pytest -p no:cacheprovider -v ./django_mask/tests/
