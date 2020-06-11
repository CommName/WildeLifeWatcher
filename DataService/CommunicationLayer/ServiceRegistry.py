import threading
import requests
import time

def registry(serviceName, serverName,address = "http://127.0.0.1", port = 9000 ):
    registryThread = threading.Thread(target=registryMe, args=(serviceName, serverName,address, port,))
    registryThread.start()

def registryMe(serviceName, serverName, address, port):
    time.sleep(2)
    code = "http://127.0.0.1:8761/"
    s = requests.Session()
    args = { 'serviceName' : serviceName, 'serverName': serverName, 'serviceAddress': address, 'servicePort':port}

    while True:
        r = s.post(code,params=args)
        time.sleep(3)
