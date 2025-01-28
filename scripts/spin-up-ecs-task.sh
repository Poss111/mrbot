#!/bin/bash

profile=""
cluster_name=""
task_definition=""
container_name=""

# Get running services on the cluster
running_services=$(aws ecs list-services --cluster $cluster_name --profile $profile | jq -r '.serviceArns[]')

# Get running tasks
running_tasks=$(aws ecs list-tasks --cluster $cluster_name --profile $profile | jq -r '.taskArns[]')

# Print out the running tasks and services on the cluster in a table
echo "Running tasks on the cluster:"
echo "Task ID | Task Definition | Container Name"
for task in $running_tasks; do
  task_definition=$(aws ecs describe-tasks --cluster $cluster_name --tasks $task --profile $profile | jq -r '.tasks[0].taskDefinitionArn')
  container_name=$(aws ecs describe-tasks --cluster $cluster_name --tasks $task --profile $profile | jq -r '.tasks[0].containers[0].name')
  echo "$task | $task_definition | $container_name"
done

# Increase the desired count of the service to 1
if [ -z "$running_services" ]; then
  echo "No services running on the cluster"
else
  for service in $running_services; do
    echo "Updating service $service"
    aws ecs update-service --cluster $cluster_name --service $service --desired-count 1 --profile $profile
  done
fi

