

cd .\DataService
docker build . -t dataservice
cd ..

cd  .\ServiceRegistry
docker build . -t serviceregistry
cd ..

cv .\VideoSensors
docker build . -t videosensor
cd ..