"""File containing the functons for getting and sending messages"""


def queue_message(network, message):
    """
    Puts a message object in the given Network's queue
    :param network: Network object
    :param message: Message object
    :return: None
    """
    network.queue.append(message)


def extract_message(network):
    """
    Gets the first message in a Network's queue of which the source and destination computers are both alive
    :param network: Network object
    :return: Message object that's first in the queue if there is one, else return None
    """
    network = network
    if network.queue:

        for message in network.queue:

            if not message.src.failed and not message.dst.failed:
                network.queue.remove(message)
                return message
