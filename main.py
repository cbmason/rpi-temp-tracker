import time
import os
from aht20 import Aht20
from argparse import ArgumentError, ArgumentParser
from dotenv import load_dotenv
from influxdb_interface import InfluxDbInterface


class RPiTempTracker:
    def __init__(
            self,
            ms_per_sample : int = 1000,
            db_type: str="influxdb",
            sensor_type: str="aht20",
            port: int=1):
        load_dotenv()
        self.msPerSample = max(ms_per_sample, 100) # Max

        # Sensor setup
        if sensor_type.lower() == "aht20":
            self.sensor = Aht20(port)

        # Database setup
        if db_type.lower() == "influxdb":
            bucket = os.getenv("INFLUX_BUCKET")
            api_key = os.getenv("INFLUX_API_KEY")
            port = os.getenv("INFLUX_PORT")
            device_name = os.getenv("INFLUX_DEVICE_NAME")
            location = os.getenv("INFLUX_LOCATION")
            url = f"http://localhost:{port}"
            org = os.getenv("INFLUX_ORG")
            self.db_interface = InfluxDbInterface(
                url=url,
                token=api_key,
                org=org,
                location=location,
                device=device_name,
                bucket=bucket)
        else:
            raise ArgumentError(None, f"Unknown DB ({db_type}) requested!")

    def run(self):
        print("Starting RPiTempTracker service.  Press ctrl+c to exit")
        self.sensor.connect()
        while True:
            start_time = time.time()
            sample = self.sensor.sample_data()
            self.db_interface.write_sample(sample)
            end_time = time.time()
            elapsed = end_time - start_time
            time.sleep(max((self.msPerSample / 1000) - elapsed, 0))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=1,
        help="The I2C port to connect to"
    )
    parser.add_argument(
        '-t',
        '--period',
        type=int,
        default=1000,
        help="Max period in ms between samples"
    )
    parser.add_argument(
        '-d',
        '--db_type',
        type=str,
        choices=['influxdb'],
        default="influxdb",
        help="Type of database to use"
    )
    parser.add_argument(
        '-s',
        '--sensor_type',
        type=str,
        choices=['aht20'],
        default="aht20",
        help="Type of sensor to use"
    )
    args = parser.parse_args()
    instance = RPiTempTracker(args.period / 1000, args.db_type, args.sensor_type, args.port)
    instance.run()
