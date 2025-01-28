#!/bin/bash

# Retrieve the commit hash
COMMIT_HASH=$(git rev-parse --short HEAD)

# Check if the commit has a tag
TAG=$(git describe --tags --exact-match 2>/dev/null)

# Export the appropriate value to the same variable
if [ -n "$TAG" ]; then
    echo "COMMIT_IDENTIFIER=$TAG" >> $GITHUB_ENV
else
    echo "COMMIT_IDENTIFIER=$COMMIT_HASH" >> $GITHUB_ENV
fi