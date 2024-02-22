#!/bin/bash

# Start the server in the background
coverage run --append server.py tests/sample.conf > tests/actual/server_start.actual &

# Sleep for 2 seconds to ensure the server starts up
sleep 2

# Send the EXIT command
echo fake recursor sending EXIT command
echo "!EXIT" | ncat localhost 1024

sleep 2

# Compare the output with the expected result
diff tests/actual/server_start.actual tests/outputs/server_start.out