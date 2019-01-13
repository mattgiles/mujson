FROM pypy:3

ENV PIP_PKGS="ujson simplejson python-rapidjson yajl nssjson mujson orjson"

RUN pip install $PIP_PKGS

COPY . /opt/bench

WORKDIR /opt/bench

ENTRYPOINT ["pypy3", "bench3.py"]

CMD ["10000", "tweet.json"]
