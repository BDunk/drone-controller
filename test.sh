#!/usr/bin/env bash


python3 -m unittest discover -v -p *.py -s ./tests
exit_code=$?
echo "Tests exited with code: $exit_code"

if [ $exit_code -ne 0 ]; then
    echo "Tests have failed!"
    exit $exit_code
fi

