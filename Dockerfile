FROM ubuntu:14.04
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-setuptools python3 build-essential sqlite3 libsqlite3-dev bcrypt libffi-dev libssl-dev python-dev
RUN easy_install3 pip
COPY . /app
RUN git clone https://github.com/corpetty/py-etherscan-api
WORKDIR /py-etherscan-api
RUN python3 setup.py install
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN export TERM=xterm
ENTRYPOINT ["python3"]
CMD ["VegaWeb.py"]
