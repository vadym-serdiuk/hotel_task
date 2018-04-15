#!/usr/bin/env bash
scripts/wait-for-it.sh -h db -p 5432 && ./manage.py runserver 0.0.0.0