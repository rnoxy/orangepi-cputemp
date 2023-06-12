# orangepi-cputemp
Very simple service to provide the CPU temp of raspberry/orange pi.

This service is written in Python and uses the Flask framework.

# Deployment
The service can be easily deployed with docker.

We have prepared the docker image on docker hub.
One can start the service with the command
```bash
docker run -d -p 5000:80 --restart unless-stopped rnoxy/orangepi-cputemp
```
The option `--restart unless-stopped` is optional, and is used to restart the service
if it crashes or if the host is rebooted.

# Usage
The service provides the CPU temperature in Celsius degrees.
One query the service in the web browser with the URL [http://localhost:5000/cpu_temp?n_zones=6](http://localhost:5000/cpu_temp?n_zones=6).
The parameter `n_zones` is optional and specifies the number of zones to divide the temperature range into.
The default value is `n_zones=6`, which works well for Orage PI 5B.

Please chage `localhost` to the IP address of the host if the service is not running on the local machine.
One can also change the port number `5000` to a different number if it is already used by another service.

The service can also be queried with the command
```bash
curl http://localhost:5000/cpu_temp?n_zones=6
```

Please note that the service is not secured and can be accessed by anyone.
It is recommended to use the service only on a local network.


# Build
We provide a [`Dockerfile`](Dockerfile) to build the image manually.
One can build the image with the command
```bash
docker build -t orangepi-cputemp .
```
