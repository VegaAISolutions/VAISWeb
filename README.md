# VegaWeb

Vega AIS Website

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
See deployment for notes on how to deploy the project on a live system. Note this is a work in progress

### Prerequisites

```
pyhon3, pip, sqlAlchemy, Flask, JinJa, sqlite3
```
to install prerequisites on ubuntu:
```
apt-get update -y
apt-get install -y python3-pip python3-setuptools python3 build-essential sqlite3 libsqlite3-dev
easy_install3 pip
```
Sorry windows user, this can be run by installing the software manually - for easiest experience, docker up.


### Installing

Installing is easy assuming you have python3 and pip installed:

```
git clone https://github.com/slapglif/VAISWeb.git
cd VAISWeb
```
```
pip install -r requirements.txt
```

## Running the app

Running is one command

```
python VegaWeb.py
```

Once it's running, you can browse to the test port

```
http://127.0.0.1:1900
```

## Deployment
Using Docker to deploy on a remote port  (default 1900)

```
docker build -t vaisw:latest .
```
```
docker run -d -p 1900:1900 vaisw
```
Running on the native http port
```
docker run -d -p 80:1900 vaisw
```
you can see the container running
```
$ docker ps -a
CONTAINER ID        IMAGE                              COMMAND                CREATED             STATUS                             PORTS                    NAMES
92fb4d65c7cd        vaisw:latest            "python VegaWeb.py"        22 minutes ago      Up 22 minutes                      0.0.0.0:1900->1900/tcp   clever_blackwell
```
