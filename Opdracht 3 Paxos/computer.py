class Computer:
    def __init__(self, name, value=None, tot_comps=0):
        self.name = name  # Computer name (P_i or A_i)
        self.failed = False  # Has the computer failed or not?
        self.prior = 0      # Prior Propose Id
        self.prior_value = None  # Prior value
        self.tot_comps = tot_comps  # Total computers
        self.tot_accept = 1  # Total accepted computers
        self.value = value  # Propose value
