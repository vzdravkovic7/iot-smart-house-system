from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import config

def save_to_db(influxdb_client, data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
    )
    write_api.write(bucket=config.INFLUXDB_BUCKET, org=config.INFLUXDB_ORG, record=point)

def save_people_count(influxdb_client, count):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = Point("PEOPLE_COUNT").field("value", count)
    write_api.write(bucket=config.INFLUXDB_BUCKET, org=config.INFLUXDB_ORG, record=point)

def handle_influx_query(influxdb_client, query):
    from flask import jsonify
    
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=config.INFLUXDB_ORG)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})