# Shoreline IoT Project

This project is a FastAPI-based application for managing IoT devices, sensors, and sensor data.

## Project Overview

The Shoreline IoT project allows users to:

- Create devices with custom sensors.
- Update device names.
- Push sensor data to specific sensors in devices.
- Retrieve sensor data within a time range.
- View all devices.
- View all sensor data.

## Installation

### Prerequisites

- Python 3.x installed
- MongoDB installed and running locally

### Steps

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd shoreline-iot
    ```

2. **Set up a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    # On GitBash Windows, use:
    source venv/Scripts/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up MongoDB:**
   
   - Ensure MongoDB is installed and running locally.
   - Adjust MongoDB connection details in `shoreline_IOT.py` if needed (`mongodb://localhost:27017` by default).

## Usage

- Run the FastAPI application:

    ```bash
    uvicorn shoreline_IOT:app --reload
    ```

- Access the API via `http://localhost:8000/docs` to view the interactive API documentation.

## Endpoints

### `/devices`

- **Request Type**: GET
- **Parameters**: None
- **Request Body**: None
- **Description**: Retrieve a list of all devices.
- **How to use**: Send a GET request to `/devices`.

### `/devices`

- **Request Type**: POST
- **Parameters**: None
- **Request Body**: 
    ```json
    {
        "name": "Device Name",
        "sensors": {
            "sensor_name_1": 2,
            "sensor_name_2": 1
        }
    }
    ```
- **Description**: Create a new device with specified sensors.
- **How to use**: Send a POST request to `/devices` with device information in the request body.

### `/devices/{device_id}`

- **Request Type**: PUT
- **Parameters**:
    - `device_id` (str): ID of the device to update.
- **Request Body**: None
- **Description**: Update the name of a device by its ID.
- **How to use**: Send a PUT request to /devices/{device_id} with the device_id in the URL and the updated name as a query parameter.

### `/devices/{device_id}/sensors/{sensor_id}/data`

- **Request Type**: POST
- **Parameters**:
    - `device_id` (str): ID of the device where the sensor belongs.
    - `sensor_id` (str): ID of the sensor to which data will be added.
- **Request Body**: 
    ```json
    {
        "value": 23.5,
        "timestamp": "2023-12-01T12:00:00"
    }
    ```
- **Description**: Add sensor data to a specific sensor in a device.
- **How to use**: Send a POST request to `/devices/{device_id}/sensors/{sensor_id}/data` with the `device_id` and `sensor_id` in the URL and the sensor data in the request body.

### `/devices/{device_id}/sensors/{sensor_id}/data`

- **Request Type**: GET
- **Parameters**: `device_id`, `sensor_id` (Path), `start_time`, `end_time` (Query)
- **Request Body**: None
- **Description**: Retrieve sensor data within a time range.
- **How to use**: Send a GET request to `/devices/{device_id}/sensors/{sensor_id}/data` with the specified time range as query parameters.

### `/all-sensor-data`

- **Request Type**: GET
- **Parameters**: None
- **Request Body**: None
- **Description**: View all sensor data.
- **How to use**: Send a GET request to `/all-sensor-data` to retrieve sensor data for all devices.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.
