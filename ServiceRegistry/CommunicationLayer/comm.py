
from CommunicationLayer import NATSCommunication
from CommunicationLayer import Communicator

async def getCommunciator(args):
    communicator = None
    if args["communicator"]=="NATS":
        communicator = NATSCommunication.NATSCommunication()
        await communicator.connect(args["NATSaddress"])

    return communicator