# Stop all containers related to this docker-compose file
docker-compose down

# Remove all containers
docker rm $(docker ps -a -q -f "name=farawayfarmer")

# Remove all images related to this project
docker rmi $(docker images -q -f "reference=farawayfarmer")

# Run docker-compose
docker-compose up -d