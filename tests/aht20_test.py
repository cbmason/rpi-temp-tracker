import time
from argparse import ArgumentParser

# Hack to deal with Python's awful directory limitations.
# See https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time/14132912
if __name__ == '__main__' and __package__ is None:
    from os import path
    import sys
    # __file__ should be defined in this case
    PARENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(PARENT_DIR)

from aht20 import Aht20

def run_test(
        i2c_port: int = 1,
        period_ms: int = 1000,
        num_samples: int = 10):
    # Connect to the device
    device = Aht20(i2c_port)
    device.connect()

    # Do a few samples
    for i in range(num_samples):
        sample = device.sample_data()
        print(f"Temp: {sample.temperature:.2f} F, Hum: {sample.humidity:.2f} %")
        time.sleep(period_ms / 1000)


if __name__ == "__main__":
    parser = ArgumentParser("Test script for AHT20")
    parser.add_argument('-p', '--port', type=int, default=1, help="The I2C port to connect to")
    parser.add_argument('-t', '--period', type=int, default=1000, help="Period in ms between samples")
    parser.add_argument('-c', '--count', type=int, default=10, help="Number of samples to take")
    parser.add_argument('-f', '--fahrenheit', type=bool, default=True, help="Use Fahrenheit instead of Celsius")
    args = parser.parse_args()
    run_test(args.port, args.period, args.count)
