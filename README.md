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

- `/devices`: CRUD operations for devices.
- `/devices/{device_id}`: Update device names.
- `/devices/{device_id}/sensors/{sensor_id}/data`: Push sensor data to specific sensors.
- `/devices/{device_id}/sensors/{sensor_id}/data`: Retrieve sensor data within a time range.
- `/devices`: GET method to view all devices.
- `/all-sensor-data`: View all sensor data.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.
