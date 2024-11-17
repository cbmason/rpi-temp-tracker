from abc import ABC, abstractmethod

import data_packet


class Sensor(ABC):
    @abstractmethod
    def connect(self):
        """
        Method to connect to the sensor
        """
        pass

    @abstractmethod
    def disconnect(self):
        """
        Method to disconnect to the sensor
        """
        pass

    @abstractmethod
    def initialize(self):
        """
        Method to initialize the sensor
        """

    @abstractmethod
    def sample_data(self) -> data_packet:
        """
        Retrieve a sample from the device
        :return: the data packet, or None if it failed
        """
        pass