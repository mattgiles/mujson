FROM python:2.7

ENV PIP_PKGS="ujson simplejson yajl python-cjson nssjson mujson"

RUN pip install --upgrade --compile $PIP_PKGS

COPY . /opt/bench

WORKDIR /opt/bench

ENTRYPOINT ["python", "bench2.py"]

CMD ["10000", "tweet.json"]
