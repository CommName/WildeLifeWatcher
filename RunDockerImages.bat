docker run --link nats-main:nats-main -e NATSaddress=nats-main -p 8761:8761 -d --name=service-registry serviceregistry
docker run --link nats-main:nats-main --link mongo-data:mongo-data --link service-registry:service-registry -e DataBaseAddress=mongo-data -e NATSaddress=nats-main -e ServiceRegistry=service-registry -p 9010:9010 -d --name=data dataservice
 
 docker run --link nats-main:nats-main --link service-registry:service-registry -e NATSaddress=nats-main -e ServiceRegistry=http://service-registry:8761/ -p 9000:9000 -d --name=sensor1 videosensor