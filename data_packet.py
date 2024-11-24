from dataclasses import dataclass


@dataclass
class DataPacket:
    temperature: float
    humidity: float
    timestamp: int