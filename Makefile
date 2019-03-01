#!/bin/make

DEPS=lockfile-progs

.PHONY: install

install:
	@-sudo apt-get install -y $(DEPS)
	@-python3 -m pip install -r tweets/requirements.txt

