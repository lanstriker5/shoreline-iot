from datetime import datetime
from bson import ObjectId
from typing import Dict
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")  # Please edit this accordingly
db = client["shoreline_iot"]  # Please edit this accordingly


# Device model
class DeviceModel(BaseModel):
    name: str
    sensors: Dict[str, int]  # Sensor name and quantity


# Sensor data model
class SensorDataModel(BaseModel):
    value: float
    timestamp: datetime


# Create a new device with specified sensors
@app.post("/devices")
async def create_device(device: DeviceModel):
    device_data = {
        "name": device.name,
        "sensors": []
    }

    # Add default sensors (temperature and pressure)
    default_sensors = ["temperature", "pressure"]
    for sensor in default_sensors:
        device_data["sensors"].append({
            "sensor_name": sensor,
            "sensor_id": str(ObjectId()),
            "data": []
        })

    # Add specified sensors with quantities and generate sensor IDs
    for sensor_name, quantity in device.sensors.items():
        for i in range(1, quantity + 1):
            sensor_id = str(ObjectId())
            device_data["sensors"].append({
                "sensor_name": f"{sensor_name}_{i}",
                "sensor_id": sensor_id,
                "data": []
            })

    # Inserting into MongoDB
    result = await db.devices.insert_one(device_data)
    return {"message": "Device created successfully", "device_id": str(result.inserted_id)}


# Update device name based on device_id
@app.put("/devices/{device_id}")
async def update_device(device_id: str, new_name: str):
    # Check if the device exists before updating the name
    device = await db.devices.find_one({"_id": ObjectId(device_id)})
    if device:
        # If the device exists update it in MongoDB
        await db.devices.update_one({"_id": ObjectId(device_id)}, {"$set": {"name": new_name}})
        return {"message": "Device name updated successfully"}
    # If not found return an Error saying device with device_id not found
    return {"message": f"Device with ID '{device_id}' not found"}


# Add sensor data for a specific sensor in a device using provided device_id and sensor_id
@app.post("/devices/{device_id}/sensors/{sensor_id}/data")
async def add_sensor_data(device_id: str, sensor_id: str, sensor_data: SensorDataModel):
    # Check if the device exists
    device = await db.devices.find_one({"_id": ObjectId(device_id)})
    if not device:
        return {"message": f"Device with ID '{device_id}' not found"}

    # Check if the sensor_id exists in the device
    sensor_exists = any(sensor["sensor_id"] == sensor_id for sensor in device["sensors"])
    if not sensor_exists:
        return {"message": f"Sensor with ID '{sensor_id}' not found in device {device_id}"}

    # Add sensor data for a specific sensor in a device using provided sensor_id
    sensor_data_with_id = {
        "value": sensor_data.value,
        "timestamp": sensor_data.timestamp
    }
    await db.devices.update_one(
        {"_id": ObjectId(device_id), "sensors.sensor_id": sensor_id},
        {"$push": {"sensors.$.data": sensor_data_with_id}}
    )
    return {"message": f"Sensor data added to {sensor_id} for device {device_id}"}


# Get sensor data for a specific sensor within a time range by device_id and sensor_id. Need to provide start_time
# and end_time parameters.
@app.get("/devices/{device_id}/sensors/{sensor_id}/data")
async def get_sensor_data_by_id(device_id: str, sensor_id: str, start_time: datetime, end_time: datetime):
    # Get sensor data for a specific sensor within a time range by sensor_id
    device = await db.devices.find_one({"_id": ObjectId(device_id)})
    if device:
        sensor = next((s for s in device["sensors"] if s["sensor_id"] == sensor_id), None)
        if sensor:
            sensor_data = sensor["data"]
            filtered_data = [data for data in sensor_data if start_time <= data["timestamp"] <= end_time]
            return {"sensor_data": filtered_data}
        return {"message": f"Sensor with ID '{sensor_id}' not found in device {device_id}"}
    return {"message": f"Device {device_id} not found"}


# Get all devices along with their sensors
@app.get("/devices")
async def get_all_devices():
    # Get all devices
    devices = []
    async for device in db.devices.find():
        device_info = {
            "device_id": str(device["_id"]),
            "name": device["name"],
            "sensor_data": []  # Structure for sensor data
        }

        for sensor in device["sensors"]:
            sensor_info = {
                "sensor_name": sensor["sensor_name"],
                "sensor_id": sensor["sensor_id"],
                "data": []  # Empty data list
            }
            device_info["sensor_data"].append(sensor_info)

        devices.append(device_info)

    return {"devices": devices}


# Get all sensor data for all devices
@app.get("/all-sensor-data")
async def get_all_sensor_data():
    all_sensor_data = []
    async for device in db.devices.find():
        device_data = {
            "device_id": str(device["_id"]),
            "device_name": device["name"],
            "sensor_data": []  # Initialize sensor data for the device
        }

        for sensor in device["sensors"]:
            sensor_info = {
                "sensor_id": sensor["sensor_id"],
                "sensor_name": sensor["sensor_name"],
                "data": sensor["data"]
            }
            device_data["sensor_data"].append(sensor_info)

        all_sensor_data.append(device_data)

    return {"all_sensor_data": all_sensor_data}
