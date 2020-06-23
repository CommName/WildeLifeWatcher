import threading
import requests
import time
import socket
import json

RegistryAddress = ""
def registry(serviceName, serverName, port = 9000, serviceRegistryAddress="http://127.0.0.1:8761/" ):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    global RegistryAddress
    RegistryAddress = serviceRegistryAddress

    registryThread = threading.Thread(target=registryMe, args=(serviceName, serverName,"http://"+ip_address, port,serviceRegistryAddress))
    registryThread.start()

def registryMe(serviceName, serverName, address, port, serviceRegistry):
    time.sleep(2)
    s = requests.Session()
    args = { 'serviceName' : serviceName, 'serverName': serverName, 'serviceAddress': address, 'servicePort':port}

    while True:
        try:
            r = s.post(serviceRegistry,params=args)


        except requests.exceptions.RequestException:
            time.sleep(5)
        time.sleep(3)


def getServices(serviceName):

    # Get data centaras
    s = requests.Session()
    parametars = {"serviceName": serviceName}

    try:
        r = s.get(RegistryAddress, params=parametars)
    except requests.exceptions.RequestException:
        return []

    if r.status_code < 200 or r.status_code >= 300:
        return []

    servicesArray = json.loads(r.text)
    if len(servicesArray) == 0:
        return []

    return servicesArray

