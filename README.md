# WildeLifeWatcher
Microservice student project for watching wildlife



#Commands used
docker pull nats
docker run -d --name nats-main -p 4222:4222 -p 6222:6222 -p 8222:8222 nats

docker pull mongo
docker run --name mongo-data -p 27017:27017 -d mongo:latest

docker pull consul
docker run -d -p 8500:8500 -p 8600:8600/udp --name=badger consul agent -server -ui -node=server-1 -bootstrap-expect=1 
docker run --name=fox consul agent -node=client-1 -join='172.17.0.2'

#DockerImages
docker build .\ServiceRegistry\ -t serviceregistry
docker run --link nats-main:nats-main -e NATSaddress=nats-main -p 8761:8761 --name=service-registry serviceregistry

docker build . -t wildelifevideosensor


docker run --link nats-main:nats-main -e NATSaddress=nats-main wildelifevideosensor


#Data used
https://gist.github.com/alexbfree/d0e5ac821e7b57a005c7d9a0cf9edae1
https://gist.githubusercontent.com/alexbfree/d0e5ac821e7b57a005c7d9a0cf9edae1/raw/002fdd7739e33c2f8331c2ba18a0a4c84b641452/launch_data_set.csv

