#!/bin/bash

# Variables
TESTCASE="bad config domain"
TEST_FILE="server_invalid_domain"


# Start the server in the background
coverage run --append server.py tests/invalid_sample_domain.conf> tests/actual/$TEST_FILE.actual &

# Sleep for 2 seconds to ensure the server starts up
sleep 2

# Send the command to the server
echo $TESTCASE

sleep 2

# Compare the output with the expected result
diff tests/actual/$TEST_FILE.actual tests/outputs/$TEST_FILE.out