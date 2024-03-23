# Stop all containers related to this docker-compose file
docker-compose down

docker rmi -f farawayfarmer
docker rmi -f nearbyfarmer

docker-compose up -d