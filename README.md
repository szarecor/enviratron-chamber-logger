
# Enviratron Chamber Logger

This is a simple package for logging plant growth chamber data for the Enviratron project. 

The package logs environmental set point and observed data on a per-chamber basis.

Data is logged using the python-json-logger package and each log line is a Python dictionary string.

Here's an example log file entry:

```json
{
    "timestamp": "2021-09-14T14:03:48.099574Z", 
    "level": "INFO", 
    "co2_actual": 502.0, 
    "chamber_id": 1, 
    "co2_target": 500.0, 
    "humidity_actual": 72.0, 
    "humidity_target": 74.0, 
    "humidification_enabled": true, 
    "dehumidification_enabled": true, 
    "lighting_1": 100.0, 
    "lighting_2": 100.0, 
    "lighting_3": 100.0, 
    "lighting_4": 100.0, 
    "lighting_5": 100.0, 
    "lighting_6": 100.0, 
    "lighting_7": 100.0, 
    "temperature_actual": 26.0, 
    "temperature_target": 26.0, 
    "air_diverter_state": false, 
    "watering_actual": 98.0, 
    "watering_target": 0.0, 
    "door_state": false, 
    "curtain_state": false, 
    "operating_mode": "Manual"
}
```

## Example Usage

The logger can be called like so: ```python -m enviratron_logger <my_config.yml>```

The yaml config has an extremely minimal structure and is not absolutely required. If the config file is not specified, the default chamber list is ALL chambers and the default location for the log files is the current directory.

