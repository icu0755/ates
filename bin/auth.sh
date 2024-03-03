#!/bin/bash

if [ "$1" = "hello_world" ]
then
    echo hello world
else
    docker compose run --rm auth python ./manage.py $*
fi
