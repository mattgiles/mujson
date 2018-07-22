FROM pypy:2

ENV PIP_PKGS="ujson simplejson yajl nssjson mujson"

RUN pip install $PIP_PKGS

COPY . /opt/bench

WORKDIR /opt/bench

ENTRYPOINT ["pypy", "bench2.py"]

CMD ["10000", "tweet.json"]
