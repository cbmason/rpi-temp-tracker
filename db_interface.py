from abc import ABC, abstractmethod

import data_packet


class DbInterface(ABC):
    def __init__(self, location: str, device: str):
        self.location = location
        self.device = device

    @abstractmethod
    def write_sample(self, packet: data_packet):
        pass
