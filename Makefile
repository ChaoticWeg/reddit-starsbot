#!/bin/make

DEPS=lockfile-progs

.PHONY: install

install:
	@-sudo apt-get install -y $(DEPS)

