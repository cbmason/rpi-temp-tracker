from influxdb_client import InfluxDBClient, Point, BucketRetentionRules
from influxdb_client.client.write_api import SYNCHRONOUS

import data_packet

from db_interface import DbInterface

class InfluxDbInterface(DbInterface):
    def __init__(self, url: str, token: str, org: str, location: str, device: str, bucket: str):
        super().__init__(location, device)
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.buckets_api = self.client.buckets_api()
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = bucket
        if not self._bucket_exists(self.bucket):
            self._create_bucket(self.bucket)

    def _bucket_exists(self, name: str):
        buckets = self.buckets_api.find_buckets()
        for bucket in buckets.buckets:
            if bucket.name == name:
                return True
        return False

    def _create_bucket(self, name: str):
        retention_rules = BucketRetentionRules(type="expire", every_seconds=0) # retain forever
        self.buckets_api.create_bucket(bucket_name=name, retention_rules=retention_rules, org=self.client.org)

    def write_sample(self, packet: data_packet):
        point = Point("RPiSensor")\
            .tag("location", self.location)\
            .tag("device", self.device)\
            .field("temperature", packet.temperature)\
            .field("humidity", packet.humidity)\
            .time(packet.timestamp)
        self.write_api.write(bucket=self.bucket, org=self.client.org, record=point)