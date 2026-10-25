.PHONY: build validate test check install list doctor clean

PYTHON ?= python3
TARGET ?= ../my-app

build:
	$(PYTHON) tools/secmatrix.py build

validate:
	$(PYTHON) tools/secmatrix.py validate

test:
	$(PYTHON) -m unittest discover -s tests -v

check: build validate test

install:
	$(PYTHON) tools/secmatrix.py install --target $(TARGET)

list:
	$(PYTHON) tools/secmatrix.py list

doctor:
	$(PYTHON) tools/secmatrix.py doctor

clean:
	$(PYTHON) tools/secmatrix.py clean
