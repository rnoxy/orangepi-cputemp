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

# Build
We provide a [`Dockerfile`](Dockerfile) to build the image manually.
One can build the image with the command
```bash
docker build -t orangepi-cputemp .
```
