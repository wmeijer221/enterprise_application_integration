.DEFAULT_GOAL := all

all: build_base build_no_cache up

build_base:
	docker build base --tag sentiment_pipeline_base

build_no_cache:
	docker compose build --no-cache

build_and_up:
	docker compose up --build

up: 
	docker compose up
	