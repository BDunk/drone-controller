#!/usr/bin/env bash


# python3 -m unittest discover -v -p *.py -s ./tests
python3 -m unittest discover --verbose --start-directory ./tests

exit_code=$?
echo "Tests exited with code: $exit_code"

#gnuplot test_PID.plot > test_PID.png
#open test_PID.png

gnuplot test_rise.plot > test_rise.png
open test_rise.png

gnuplot test_lateral.plot > test_lateral.png
open test_lateral.png

if [ $exit_code -ne 0 ]; then
    echo "Tests have failed!"
    exit $exit_code
fi

