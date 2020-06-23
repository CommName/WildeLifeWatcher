
from CommunicationLayer import NATSCommunication
from CommunicationLayer import Communicator




async def getCommunciator(args, parent):
    communicator = None
    if(args["communicator"]):
        communicator = NATSCommunication.NATSCommunication()
        communicator.logic = parent
        await communicator.connect(args["NATSaddress"])

    return communicator