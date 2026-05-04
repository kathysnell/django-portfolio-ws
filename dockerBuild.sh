#!/bin/bash
set -e

# A script to build a docker image that will build the 
# container for the Django project portfolio-ws. The image will 
# be used to run the app in a container that will be use 
# PostgreSQL as the database.
# Usage: ./dockerBuild.sh

# Build the Docker image
docker build -t portfolio-ws .

# Exit script
exit 0
