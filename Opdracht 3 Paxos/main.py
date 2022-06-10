"""Our main program where we run all core functions from"""

from system import DisSystem


def give_inputs():
    """
    Lets the user give inputs to the simulation
    :return: List of inputs
    """
    print("Give inputs\n"
          "'0 END' will end the input session.")
    end = False
    input_list = []
    while not end:
        user_input = input("")
        input_list.append(user_input)

        if user_input == "0 END":
            end = True

    inputs_list = []
    for str in input_list:
        inputs_list.append(str.split(" ", 3))

    # Converts strings to integers where necessary
    for line in inputs_list:
        for i in range(len(line)):
            try:
                line[i] = int(line[i])
            except ValueError:
                line[i] = line[i]
                continue

    return inputs_list


def create_events(inputs):
    """
    Interprets the user inputs and turns them into events.
    :param inputs: Creates events
    :return:
    """
    event_lst = []
    for event in inputs:
        tick = int(event[0])
        F = []
        R = []
        msg_P = None
        msg_V = None

        if event[1] == "PROPOSE":
            msg_P = f"P{event[2]}"
            msg_V = event[3]

        elif event[1] == "FAIL":
            if event[2] == "PROPOSER":
                F.append('P'+str(event[3]))

            else:
                F.append('A'+str(event[3]))

        elif event[1] == "RECOVER":
            if event[2] == "PROPOSER":
                R.append('P'+str(event[3]))

            else:
                R.append('A'+str(event[3]))

        event_lst.append((tick, F, R, msg_P, msg_V))

    return event_lst


def start_sim(inputs):
    """
    Creates our Distributed System and starts the simulation
    :param inputs: The inputs given by the user.
    :return: None
    """
    start = inputs[0]
    n_p = start[0]
    n_a = start[1]
    n_l = start[2]
    tmax = start[3]
    events = inputs[1:]

    E = create_events(events)
    sim = DisSystem()

    sim.simulation(n_p, n_a, n_l, tmax, E)


if __name__ == '__main__':
    # events = give_inputs()
    # start_sim(events)

    # Some shortcuts, uncomment if you want to test these
    # Example 3 from Canvas
    test3 = [(1, 3, 1, 1000), (0, "PROPOSE", 1, "nl: g"), (100, "PROPOSE", 1, "nl:ga"), (200, "PROPOSE", 1, "nl:af"),
            (300, "PROPOSE", 1, "nl:f "), (400, "PROPOSE", 1, "en: g"), (500, "PROPOSE", 1, "en:gr"),
            (600, "PROPOSE", 1, "en:re"), (700, "PROPOSE", 1, "en:ea"), (800, "PROPOSE", 1, "en:at"),
            (900, "PROPOSE", 1, "en:t "), (0, "END")]

    # Example 2 from Canvas
    test2 = [(2, 3, 0, 50), (0, "PROPOSE", 1, 42), (8, "FAIL", "PROPOSER", 1), (11, "PROPOSE", 2, 37),
             (26, "RECOVER", "PROPOSER", 1), (0, "END")]

    # Example 1 from Canvas
    test1 = [(1, 3, 0,15), (0 , "PROPOSE", 1 , 42), (0,"END")]

    print("**********  Voorbeeld 1 ********** ")
    start_sim(test1)

    print("********** Voorbeeld 2 ***************")
    start_sim(test2)

    print("**********  Voorbeeld 3 ********** ")
    start_sim(test3)
