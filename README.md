[![Build and Publish Docker Image](https://github.com/rnoxy/orangepi-cputemp/actions/workflows/build.yml/badge.svg)](https://github.com/rnoxy/orangepi-cputemp/actions/workflows/build.yml)

# orangepi-cputemp
Extremely simple service to provide the CPU temp (in Celsius degrees) of raspberry/orange pi as a web service,
running as a docker container on the host and accessible via the link `http://<IP_ADDRESS>:<PORT>/cpu_temp`,
where `<IP_ADDRESS>` is the IP address of the raspberry/orange pi host and `<PORT>` is the port number.

Below we assume that the service is running on the host with the IP address `10.1.2.3` and the port number `5000`.

The service is written in Python and uses the Flask framework.

The sample response from the server is JSON format with the following keys:
```json
{
    "temp_average": 38.07683333333333,
    "temp_zone0":37.923,
    "temp_zone1":37.923,
    "temp_zone2":38.846,
    "temp_zone3":38.846,
    "temp_zone4":37.923,
    "temp_zone5":37.0
}
```

The key `temp_average` is the average temperature of all zones.
By default the temperature range is divided into 6 zones, which is suitable for [Orange PI 5B](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-5B.html).


One can use this service in order to create a sensor in [Home Assistant](https://www.home-assistant.io/) that reads the CPU temperature of the raspberry/orange pi host every 5 seconds; see figure below.
<img width="502" alt="image" src="https://github.com/rnoxy/orangepi-cputemp/assets/12031664/b23a7ce0-639f-433f-ade4-a60b03449aef">

See the section [Usage](#usage) for more details.


# Deployment

## Docker
The service can be easily deployed provided that docker is installed on the host.

The image 
[rnoxy/orangepi-cputemp](https://hub.docker.com/repository/docker/rnoxy/orangepi-cputemp/general)
is available on [Docker Hub](https://hub.docker.com/repository/docker/rnoxy/orangepi-cputemp/general).

One can start the service with the command
```bash
docker run -d -p 5000:80 --restart unless-stopped rnoxy/orangepi-cputemp
```
The option `--restart unless-stopped` is optional, and is used to restart the service
if it crashes or if the host is rebooted.

## docker-compose
The service can be deployed with docker-compose.

Below is an example of a `docker-compose.yml` file:
```yaml
version: '3.7'

services:
  orangepi-cputemp:
    image: rnoxy/orangepi-cputemp
    container_name: orangepi-cputemp
    restart: unless-stopped
    ports:
      - 5000:80
```

You can set up the port number (defaults to `5000`) and the container name as you like.


# Usage

The service provides the CPU temperature in Celsius degrees for all zones available on the host.

One can specify the number of zones to divide the temperature range into with the parameter `n_zones`.
The default value is `n_zones=6`, which works well for [Orage PI 5B](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-5B.html).

## Web browser
The example query is [http://10.1.2.3:5000/cpu_temp?n_zones=6](http://10.1.2.3:5000/cpu_temp?n_zones=6).
 
Please chage `localhost` to the IP address of the host if the service is not running on the local machine.
One can also change the port number `5000` to a different number if it is already used by another service.


## curl
The service can also be queried with the command
```bash
curl http://10.1.2.3:5000/cpu_temp?n_zones=6
```

## home assistant sensor
Here is and example YAML configuration for the [Home Assistant](https://www.home-assistant.io/) sensor:
```yaml
command_line:
  - sensor:
      name: PI CPU Temperature
      command: 'curl "http://10.1.2.3:5000/cpu_temp?n_zones=6"'
      unit_of_measurement: "°C"
      value_template: "{{ value_json.temp_average | round(1) }}"
      scan_interval: 5
```

This configuration will create a sensor with the name `PI CPU Temperature` and the unit of measurement `°C`.
Please change the IP address `10.1.2.3` to the IP address of the raspberry/orange pi host running the service.

The sensor will be updated every 5 seconds (see the parameter `scan_interval`).


# Build

## Manual installation
The service can be deployed manually on the host with Python 3.9+ and Flask installed.

First, clone the repository:
```bash
git clone https://github.com/rnoxy/orangepi-cputemp.git
```

Then change the directory:
```bash
cd orangepi-cputemp
```

Next, run the service with the command
```bash
python3 app.py
```

We provide a [`Dockerfile`](Dockerfile) to build the image manually.

One can build the image with the command
```bash
docker build -t orangepi-cputemp --platform linux/arm64 .
```

The option `--platform linux/arm64` is required if you run the command on a x86_64 machine.
