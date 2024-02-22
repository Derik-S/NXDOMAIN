#!/bin/bash

# Erase previous coverage
coverage erase

# Run test scripts
tests/server_start.sh
tests/server_invalid_arguments.sh
tests/server_invalid_port.sh
tests/server_invalid_configuration.sh
tests/server_invalid_domain.sh

# Delay for the coverage to finalize
sleep 0.1

# Print the coverage report
coverage report -m
