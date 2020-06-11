
from CommunicationLayer import NATSCommunication
from CommunicationLayer import Communicator




async def getCommunciator(args, parent):
    communicator = None
    if(args["communicator"]=="NATS"):
        communicator = NATSCommunication.NATSCommunication()
        communicator.logic = parent
        await communicator.connect(args["NATSaddress"])

    return communicator