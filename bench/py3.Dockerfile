FROM python:3.6

ENV PIP_PKGS="ujson simplejson python-rapidjson yajl metamagic.json nssjson orjson mujson"

RUN pip3 install --upgrade --compile $PIP_PKGS

COPY . /opt/bench

WORKDIR /opt/bench

ENTRYPOINT ["python", "bench3.py"]

CMD ["10000", "tweet.json"]
