#!/bin/bash

# Variables
TESTCASE="fake argument testcae"
TEST_FILE="server_invalid_arguments"


# Start the server in the background
coverage run --append server.py fake_argument > tests/actual/$TEST_FILE.actual &

# Sleep for 2 seconds to ensure the server starts up
sleep 2

# Send the command to the server
echo $TESTCASE

sleep 2

# Compare the output with the expected result
diff tests/actual/$TEST_FILE.actual tests/outputs/$TEST_FILE.out
