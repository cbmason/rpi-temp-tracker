import time
from argparse import ArgumentError

from conversions import c_to_f
from data_packet import DataPacket
from enum import Enum
from sensor import Sensor
from smbus3 import SMBus


class Aht20(Sensor):

    def __init__(self, i2c_port_num: int):
        self.i2cPortNum = i2c_port_num
        self.i2cConnection = None
        self.i2cAddress = 0x38
        self.maxTries = 3

    def connect(self):
        self.i2cConnection = SMBus(self.i2cPortNum)

    def disconnect(self):
        if self.i2cConnection is not None:
            self.i2cConnection.close()
            self.i2cConnection = None

    def initialize(self):
        if self.i2cConnection is None:
            raise ConnectionError("AHT20 device not connected!")
        status = self.i2cConnection.read_byte_data(self.i2cAddress, 0x71)
        if status & 0x08 != 0x08:
            self._write_initialize_command()

    def sample_data(self) -> DataPacket | None:
        if self.i2cConnection is None:
            raise ConnectionError("AHT20 device not connected!")
        self._write_trigger_command()
        retries = 0
        while retries < self.maxTries:
            time.sleep(0.08)
            data = self._read_bytes(6)
            # check status
            if (data[0] & 0x80) == 0:
                raw_humidity = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
                raw_temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
                relative_humidity = (raw_humidity / (2**20)) * 100
                temperature = c_to_f(((raw_temp / (2**20)) * 200) - 50)
                return DataPacket(temperature=temperature, humidity=relative_humidity)
            else:
                retries += 1
        return None

    class _Commands(Enum):
        INITIALIZATION = [0xBE, 0x08, 0x00]
        TRIGGER_MEASUREMENT = [0xAC, 0x33, 0x00]
        SOFT_RESET = [0xBA]

    def _write_byte(self, byte_to_write: int):
        if byte_to_write > 255:
            raise ArgumentError(None, f"Attempting to write invalid byte {byte_to_write}")
        self.i2cConnection.write_byte(self.i2cAddress, byte_to_write)

    def _write_bytes(self, bytes_to_write: list[int]):
        self.i2cConnection.write_i2c_block_data(self.i2cAddress, 0, bytes_to_write)

    def _read_bytes(self, count: int) -> list[int]:
        return self.i2cConnection.read_i2c_block_data(self.i2cAddress, 0x00, count)

    def _write_initialize_command(self) -> None:
        self._write_bytes(self._Commands.INITIALIZATION.value)

    def _write_trigger_command(self) -> None:
        self._write_bytes(self._Commands.TRIGGER_MEASUREMENT.value)

    def _write_soft_reset_command(self) -> None:
        self._write_bytes(self._Commands.SOFT_RESET.value)
