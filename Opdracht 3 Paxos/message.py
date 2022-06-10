class Message:
    def __init__(self, src, dst, tpe, value, id):
        self.src = src  # Source computer (computer that sends the message)
        self.dst = dst  # Destination computer (computer that receives the message)
        self.type = tpe  # Message type (PROPOSE, PREPARE, PROMISE, ACCEPT, ACCEPTED, REJECTED)
        self.id = id  # Message identifactor (n)
        self.value = value  # Propose value

