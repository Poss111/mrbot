#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <CPU> <MEMORY> <EXECUTION_ROLE_ARN>"
    exit 1
fi

# Assign arguments to variables
CPU=$1
MEMORY=$2
EXECUTION_ROLE_ARN=$3

# Use jq to update the task definition
jq --arg CPU "$CPU" --arg MEMORY "$MEMORY" --arg EXEC_ROLE_ARN "$EXECUTION_ROLE_ARN" \
   '.containerDefinitions[0].cpu = $CPU | .containerDefinitions[0].memory = $MEMORY | .executionRoleArn = $EXEC_ROLE_ARN' \
   ../ecs/task-definition.json > ../ecs/task-definition-updated.json