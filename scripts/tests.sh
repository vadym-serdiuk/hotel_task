#!/usr/bin/env bash

scripts/wait-for-it.sh -h db -p 5432 && pytest --create-db --pep8 --flakes