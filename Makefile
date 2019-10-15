#!/usr/bin/make -f
SHELL=/usr/bin/env bash
.PHONY: all test test-with-docker lint
.DEFAULT_GOAL := all

MONGO_HOST?="localhost"
MONGO_USER?="root"
MONGO_PASSWORD?="test"
MONGO_DB_NAME?=testdb
TOKEN?="test"

all: test lint

lint:
	prospector --full-pep8 --max-line-length 120 --strictness high -i node_modules

test:
	MONGO_HOST=$(MONGO_HOST) \
		MONGO_USER=$(MONGO_USER) \
		MONGO_PASSWORD=$(MONGO_PASSWORD) \
		MONGO_DB_NAME=$(MONGO_DB_NAME) \
		TOKEN=$(TOKEN) \
		py.test --cov-branch --cov=. tests/ ./

test-with-docker:
	docker-compose up -d
	MONGO_HOST=$(MONGO_HOST) \
		MONGO_USER=$(MONGO_USER) \
		MONGO_PASSWORD=$(MONGO_PASSWORD) \
		py.test --cov-branch --cov=. tests/ ./
	docker-compose down
