import smbus3

class Tracker:

    def __init__(self, ms_per_sample : int = 1000):
        self.msPerSample = ms_per_sample

    def run(self):
        # just sample every x seconds
        pass

