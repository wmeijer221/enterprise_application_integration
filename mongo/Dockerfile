# syntax=docker/dockerfile:1

FROM mongo:6.0

COPY ./scripts/init_indexes.js /docker-entrypoint-initdb.d/init_indexes.js
