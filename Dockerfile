FROM ubuntu:14.04
RUN apt-get update -y
RUN apt-get install -y  python3 python3-pip build-essential
COPY . /*
WORKDIR /
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["VegaWeb.py"]