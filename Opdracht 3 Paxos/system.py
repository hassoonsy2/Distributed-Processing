"""Our Distributed System that contains a network of computers."""

from computer import Computer
from message import Message
from network import Network
from message_functions import *
from matrix import Matrix


class DisSystem:
    def __init__(self):
        self.P = []     # Proposers
        self.A = []     # Acceptors
        self.L = []     # Learners
        self.N = Network()  # queue
        self.total_computers = None       # Computers
        self.n = 0      # Propose id
        self.comp_counter = 0
        self.success = []    # Succes messages
        self.current_tick = ""
        self.max_len_tick = 0

    def deliver_message(self, computer, message):
        """
        Puts messages in the Network's queue according to the previously received message.

        :param computer: Computer object
        :param message: Message object
        :return: None
        """
        for p in self.P:
            if p.name == computer:
                computer = p
                continue

        # If the previous message type was PROPOSE
        if message.type == "PROPOSE":
            computer.value = message.value

            if computer.prior < self.n:
                computer.prior = self.n
                computer.prior_value = message.value

            # Send PREPARE to all Acceptors
            for acceptor in self.A:
                m = Message(computer, acceptor, "PREPARE", None, self.n)
                queue_message(self.N, m)

        # If the previous message type was PREPARE
        elif message.type == "PREPARE":
            print(f"{self.current_tick.zfill(self.max_len_tick)}: {message.src.name} -> {message.dst.name}  {message.type} n={message.id}")

            # Send PROMISE
            m = Message(computer, message.src, "PROMISE", computer.value, self.n)
            queue_message(self.N, m)

        # If the previous message type was PROMISE
        elif message.type == "PROMISE":
            prior = f"(Prior: {None if message.src.prior_value == 0 else f'n={message.src.prior}, v={message.src.prior_value}'})"
            print(f"{self.current_tick.zfill(self.max_len_tick)}: {message.src.name} -> {message.dst.name}  {message.type}  n={self.n}  {prior}")

            # If the computer had a value assigned to it prior.
            if message.src.prior_value is not None:
                val = message.src.prior_value
                computer.value = val
            else:
                val = computer.value

            # Send ACCEPT
            m = Message(computer, message.src, "ACCEPT", val, self.n)
            queue_message(self.N, m)

        # If the previous message type was ACCEPT
        elif message.type == "ACCEPT":

            print(f"{self.current_tick.zfill(self.max_len_tick)}: {message.src.name} -> {message.dst.name}  {message.type} n={message.id} v={message.src.value}")

            if message.id < self.n:
                msg_type = "REJECTED"
            else:
                msg_type = "ACCEPTED"

            message.dst.prior_value = message.src.value
            message.dst.prior = self.n
            m = Message(computer, message.src, msg_type, message.value, self.n)
            queue_message(self.N, m)

        elif message.type == "SUCCESS":
            first = message.value[-2]
            last = message.value[-1]
            computer.value.plus_one(first, last)
            print(
                f"{self.current_tick.zfill(self.max_len_tick)}: {message.src.name} -> {message.dst.name}  PREDICTED n={int(computer.value.df.to_numpy().sum())}")

        else:
            self.comp_counter += 1
            if message.type == "ACCEPTED":
                print(
                    f"{str(self.current_tick).zfill(self.max_len_tick)}: {message.src.name} -> {message.dst.name}  {message.type} n={message.id} v={computer.value}")
                message.src.prior = 0
                message.src.prior_value = None
                computer.tot_accept += 1
            else:
                print(f"{self.current_tick.zfill(self.max_len_tick)}: {message.src.name} -> {message.dst.name}  {message.type} n={computer.prior}")

            if computer.tot_accept > (computer.tot_comps/2):    # Checks if there is an agreement
                succes_message = f"{computer.name} heeft wel consensus (voorgesteld: {computer.prior_value}, geaccepteerd: {computer.value})"
                try:
                    if self.success[-1] != succes_message:
                        self.success.append(succes_message)
                        for learner in self.L:
                            m = Message(computer, learner, "SUCCESS", computer.value, self.n)
                            queue_message(self.N, m)

                except IndexError:
                    self.success.append(succes_message)
                    for learner in self.L:
                        m = Message(computer, learner, "SUCCESS", computer.value, self.n)
                        queue_message(self.N, m)



            if self.comp_counter == len(self.A):
                self.comp_counter = 0

                if computer.tot_accept <= (computer.tot_comps / 2):
                    if computer.prior < self.n:
                        self.n += 1
                        computer.prior = self.n

                    for acceptor in self.A:
                        m = Message(computer, acceptor, "PREPARE", None, self.n)
                        queue_message(self.N, m)

    def simulation(self, n_p, n_a, n_l, tmax, E):
        """
        Simulation to manage all the messages and Network queue's.

        :param n_p: Amount of Proposers
        :param n_a: Amount of Acceptors
        :param n_l: Amount of Learners
        :param tmax: Maximum amount of ticks
        :param E: List of events
        :return: None
        """
        self.max_len_tick = len(str(tmax)) if len(str(tmax)) > 3 else 3
        self.total_computers = n_a + n_p + n_l  # Acceptors + Proposers + Learners
        for i in range(n_p):
            self.P.append(Computer(f"P{i + 1}", tot_comps=self.total_computers))
        for i in range(n_a):
            self.A.append(Computer(f"A{i + 1}", tot_comps=self.total_computers))
        for i in range(n_l):
            com = Computer(f"L{i + 1}", tot_comps=self.total_computers)
            com.value = Matrix()
            self.L.append(com)

        for t in range(tmax):
            if len(self.N.queue) == 0 and len(E) == 0:
                return
            e = E[0] if int(t) == E[0][0] else None
            t = str(t)
            if e is not None:
                E.remove(e)
                (i, F, R, pi_c, pi_v) = e

                # Fail computers
                for computer in F:
                    if "P" in computer:  # If the computer is a proposer
                        for proposer in self.P:
                            if proposer.name == computer:
                                proposer.failed = True
                                print(f"{t.zfill(self.max_len_tick)}: ** {proposer.name} kapot **")
                    else:
                        for acceptor in self.A:
                            if acceptor.name == computer:
                                acceptor.failed = True
                                print(f"{t.zfill(self.max_len_tick)}: ** {acceptor.name} kapot **")

                # Repair computers
                for computer in R:
                    if "P" in computer:  # If the computer is a proposer
                        for proposer in self.P:
                            if proposer.name == computer:
                                proposer.failed = False
                                print(f"{t.zfill(self.max_len_tick)}: ** {proposer.name} gerepareerd **")
                    else:
                        for acceptor in self.A:
                            if acceptor.name == computer:
                                acceptor.failed = False
                                print(f"{t.zfill(self.max_len_tick)}: ** {acceptor.name} gerepareerd **")

                if pi_v is not None and pi_c is not None:
                    self.comp_counter = 0
                    self.n += 1
                    m = Message(None, pi_c, "PROPOSE", pi_v, self.n)
                    print(f"{t.zfill(self.max_len_tick)}:    -> {pi_c}  PROPOSE v={pi_v}")
                    self.deliver_message(pi_c, m)
            else:
                m = extract_message(self.N)
                if m is not None:
                    self.current_tick = t
                    self.deliver_message(m.dst, m)
                else:
                    print(f"{str(t).zfill(self.max_len_tick)}:")
        print()
        print(self.L[0].value.df) if self.L else None
        for success in self.success:
            print(success)
