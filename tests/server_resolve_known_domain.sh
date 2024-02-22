#!/bin/bash

# Variables
TESTCASE="Resolve known domain"
TEST_FILE="server_resolve_known_domain"

# Start the server in the background
coverage run --append server.py tests/sample.conf > tests/actual/$TEST_FILE.actual &

# Sleep for 2 seconds to ensure the server starts up
echo "www.google.com" | nc localhost 1024 >> tests/actual/$TEST_FILE.actual

# Check the output
echo $TESTCASE
diff tests/actual/$TEST_FILE.actual tests/outputs/$TEST_FILE.out
