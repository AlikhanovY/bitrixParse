VENV_NAME := venv
PYTHON := python3

.PHONY: venv install clean

venv:
	$(PYTHON) -m venv $(VENV_NAME)


install: venv
	./$(VENV_NAME)/bin/pip install --upgrade pip
	./$(VENV_NAME)/bin/pip install -r requirements.txt
	cp .env.exmaple .env

