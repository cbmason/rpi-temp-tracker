import time
from argparse import ArgumentParser

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
        print(f"Temp: {sample.temperature}C, Hum: {sample.humidity}%")
        time.sleep(period_ms / 1000)


if __name__ == "__main__":
    parser = ArgumentParser("Test script for AHT20")
    parser.add_argument('-p', '--port', type=int, default=1, help="The I2C port to connect to")
    parser.add_argument('-t', '--period', type=int, default=1000, help="Period in ms between samples")
    parser.add_argument('-c', '--count', type=int, default=10, help="Number of samples to take")
    args = parser.parse_args()
    run_test(args.port, args.period, args.count)