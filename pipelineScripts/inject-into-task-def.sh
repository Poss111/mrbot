#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <CPU> <MEMORY> <EXECUTION_ROLE_ARN> <TASK_ROLE_ARN> <TASK_JSON_PATH>"
    exit 1
fi

# Assign arguments to variables
CPU=$1
MEMORY=$2
EXECUTION_ROLE_ARN=$3
TASK_ROLE_ARN=$4
TASK_JSON_PATH=$5

# Use jq to update the task definition
jq --arg CPU "$CPU" --arg MEMORY "$MEMORY" --arg EXEC_ROLE_ARN "$EXECUTION_ROLE_ARN" --arg TASK_ROLE_ARN "$TASK_ROLE_ARN" \
'.containerDefinitions[0].cpu = ($CPU | tonumber) | .cpu = $CPU | .containerDefinitions[0].memory = ($MEMORY | tonumber) | .memory = $MEMORY | .executionRoleArn = $EXEC_ROLE_ARN | .taskRoleArn = $TASK_ROLE_ARN' \
   "$TASK_JSON_PATH" > "${TASK_JSON_PATH%.json}-updated.json"