FROM alpine:3.7

ENV BUILD_PKGS="g++ git musl-dev python3-dev yajl-dev" \
    RUNTIME_PKGS="python3 yajl gcc" \
    PIP_PKGS_COMPILE="ujson simplejson python-rapidjson yajl metamagic.json nssjson"

RUN \
  apk add --no-cache --virtual .build-deps $BUILD_PKGS && \
  pip3 install --compile $PIP_PKGS_COMPILE && \
  apk del .build-deps && \
  apk add --no-cache $RUNTIME_PKGS && \
  python3 -m ensurepip && rm -r /usr/lib/python*/ensurepip && \
  ln -s pip3 /usr/bin/pip && ln -sf /usr/bin/python3 /usr/bin/python

COPY . /opt/mujson

RUN pip install -e /opt/mujson

WORKDIR /opt/mujson/bench

ENTRYPOINT ["python", "bench3.py"]

CMD ["10000", "tweet.json"]
