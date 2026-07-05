import time
import os
from aht20 import Aht20
from argparse import ArgumentError, ArgumentParser
from dotenv import load_dotenv
from influxdb_interface import InfluxDbInterface


class RPiTempTracker:
    def __init__(self):
        load_dotenv()

        msPerSample = int(os.getenv("SAMPLE_PERIOD_MS", "2000"))
        db_type = os.getenv("DB_TYPE", "influxdb")
        sensor_type = os.getenv("SENSOR_TYPE", "aht20")
        sensor_port = int(os.getenv("I2C_PORT", "1"))

        self.msPerSample = max(msPerSample, 100)  # Floor at 100 ms

        # Sensor setup
        if sensor_type.lower() == "aht20":
            self.sensor = Aht20(sensor_port)

        # Database setup
        if db_type.lower() == "influxdb":
            bucket = os.getenv("INFLUX_BUCKET")
            api_key = os.getenv("INFLUX_API_KEY")
            influx_port = os.getenv("INFLUX_PORT")
            device_name = os.getenv("INFLUX_DEVICE_NAME")
            location = os.getenv("LOCATION")
            host = os.getenv("INFLUX_HOST", "localhost")
            url = f"http://{host}:{influx_port}"
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
        self.sensor.initialize()
        s_per_sample = self.msPerSample / 1000
        while True:
            start_time = time.time()
            sample = self.sensor.sample_data()
            self.db_interface.write_sample(sample)
            end_time = time.time()
            elapsed = end_time - start_time
            time.sleep(max(s_per_sample - elapsed, 0))


if __name__ == "__main__":
    instance = RPiTempTracker()
    instance.run()
