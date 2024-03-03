#!/bin/bash

if [ "$1" = "hello_world" ]
then
    echo hello world
else
    docker compose run --rm task_tracker python ./manage.py $*
fi
