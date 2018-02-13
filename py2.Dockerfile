FROM alpine:3.7

ENV BUILD_PKGS="g++ git musl-dev python2-dev yajl-dev" \
    RUNTIME_PKGS="python2 yajl gcc" \
    PIP_PKGS_COMPILE="ujson simplejson yajl python-cjson nssjson"

RUN \
  apk add --no-cache --virtual .build-deps $BUILD_PKGS && \
  python -m ensurepip && \
  pip install --compile $PIP_PKGS_COMPILE && \
  apk del .build-deps && \
  apk add --no-cache $RUNTIME_PKGS

COPY . /opt/mujson

RUN pip install -e /opt/mujson

WORKDIR /opt/mujson/bench

ENTRYPOINT ["python", "bench2.py"]

CMD ["10000", "tweet.json"]
