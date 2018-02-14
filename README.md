# mujson

`mujson` lets python libraries make use of the most performant JSON functions available at import time. It does not itself implement any encoding or decoding functionality.

## rationale

JSON decoding and encoding is a common application bottleneck, and a variety of "fast" substitutes for the standard library's `json` exist, typically implemented in C. This is great for applications which can fine tune their dependency trees, but third party libraries are often forced to rely on the standard library so as to avoid superfluous or expensive dependencies.

The situation is sufficiently frustrating that it is common for third party libraries to use `try... except` logic around imports, hoping to find some better third party JSON library available. But even that approach is sub-optimal. In fact, the relative performance of different JSON libraries varies between encoding and decoding activities, as well as between Python 2.x and Python 3.x environments.

`mujson` is designed to let libraries simply ask for whatever the most performant json functions available are at import time. Library owners are also given the option to specify what JSON implementations are most proficient for their purposes.

## usage

For simple usage:

```python
import mujson as json

json.loads(json.dumps({'hello': 'world!'}))
```

To customize the ranked order of JSON libraries, or to protect against collision with other customized use of mujson at runtime:

``` python
from mujson import mujson_function

FAST_JSON_LIBS = ['ujson', 'rapidjson', 'yajl']

fast_dumps = mujson_function('fast_dumps', ranking=FAST_JSON_LIBS)
```

`mujson` comes with one custom set of functions already implemented, using a ranking that excludes json libraries that do not support the function signatures supported by corresponding functions in the standard library. Consider:

```python
import logging

from mujson import compliant_dumps
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()

logHandler = logging.StreamHandler()
# NOTE: we use `compliant_dumps` here mainly because the `JsonFormmatter` makes
# use of kwargs like `cls` and `default` which not all json libraries support.
# This would NOT be an issue if this were the ONLY usage of mujson at runtime.
# However, if there are other places in an application where `mujson.dumps` is
# being used, we neither want to deny performance improvements which are
# otherwise available to simple uses of `dumps` nor do we want to risk throwing
# an error here if we go to use `dumps` and a non-compliant json function has
# already been "negotiated" by mujson.
formatter = jsonlogger.JsonFormatter(json_serializer=compliant_dumps)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
```

## default rankings

`mujson`'s default rankings are scoped to function (e.g. `loads`) and python version. They are based on benchmarked performance of different JSON libraries encoding and decoding the twitter data at [`bench/json/tweet.json`](bench/json/tweet.json).

### python 3

``` python
DEFAULT_RANKINGS = {
    'dump': [mjson, rapidjson, ujson, yajl, json, nssjson, simplejson],
    'dumps': [mjson, rapidjson, ujson, yajl, json, nssjson, simplejson],
    'load': [ujson, yajl, json, nssjson, simplejson, rapidjson],
    'loads': [ujson, yajl, json, nssjson, simplejson, rapidjson]
}
```

### python 2

``` python
DEFAULT_RANKINGS = {
    'dump': [ujson, yajl, json, cjson, nssjson, simplejson],
    'dumps': [ujson, yajl, json, cjson, nssjson, simplejson],
    'load': [ujson, cjson, simplejson, nssjson, yajl, json],
    'loads': [ujson, cjson, simplejson, nssjson, yajl, json]
}
```

## running benchmarks

You can build the python 3 benchmarking environment with something like:

``` shell
$ docker build -t mujson-bench:py3 -f py3.Dockerfile .
```

And you can run the benchmark against any of the provided json files:

``` text
$ docker run -it mujson-bench:py3 1000 apache.json

***************************************************************************

rapidjson       decoded apache.json 1000 times in 1602.057653999509 milliseconds
simplejson      decoded apache.json 1000 times in 1034.323225998378 milliseconds
nssjson         decoded apache.json 1000 times in 1100.1701329987554 milliseconds
json            decoded apache.json 1000 times in 1170.220017000247 milliseconds
yajl            decoded apache.json 1000 times in 1224.6836369995435 milliseconds
ujson           decoded apache.json 1000 times in 971.0670500026026 milliseconds
mujson          decoded apache.json 1000 times in 966.8092329993669 milliseconds

***************************************************************************

simplejson      encoded apache.json 1000 times in 2175.9825850022025 milliseconds
nssjson         encoded apache.json 1000 times in 2175.597892000951 milliseconds
json            encoded apache.json 1000 times in 1711.0415339993779 milliseconds
yajl            encoded apache.json 1000 times in 1038.154541998665 milliseconds
ujson           encoded apache.json 1000 times in 789.5985149989428 milliseconds
rapidjson       encoded apache.json 1000 times in 616.3629779985058 milliseconds
metamagic.json  encoded apache.json 1000 times in 357.27883399886196 milliseconds
mujson          encoded apache.json 1000 times in 364.98578699684003 milliseconds

***************************************************************************

nssjson         de/encoded apache.json 1000 times in 3245.4301819998363 milliseconds
simplejson      de/encoded apache.json 1000 times in 3285.083388000203 milliseconds
json            de/encoded apache.json 1000 times in 2727.172070000961 milliseconds
yajl            de/encoded apache.json 1000 times in 2573.481614999764 milliseconds
rapidjson       de/encoded apache.json 1000 times in 2262.237699000252 milliseconds
ujson           de/encoded apache.json 1000 times in 1749.4632090019877 milliseconds
mujson          de/encoded apache.json 1000 times in 1608.914870001172 milliseconds

***************************************************************************
```

## todo

- provide more context on benchmarks
- implement checks at import time to see if libraries with optional speedups were successfully installed with speedups in place, as that impacts the assumptions behind the default rankings.