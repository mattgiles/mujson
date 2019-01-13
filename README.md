# mujson

`mujson` lets python libraries make use of the most performant JSON functions available at import time. It is small, and does not itself implement any encoding or decoding functionality.

## installation

Install with:

``` shell
$ pip install --upgrade mujson
```

## rationale

JSON decoding and encoding is a common application bottleneck, and a variety of "fast" substitutes for the standard library's `json` exist, typically implemented in C. This is great for projects which can fine tune their dependency trees, but third party libraries are often forced to rely on the standard library so as to avoid superfluous or expensive requirements.

It is common for libraries to use guarded imports (i.e. `try... except` logic), hoping to find some better JSON implementation available. But this approach is sub-optimal. There are many python JSON libraries, and the relative performance of these varies between encoding and decoding, as well as between Python 2 and 3.

`mujson` just uses the most performant JSON functions available, with the option to specify what JSON implementations are best for your project. It may also be of use to developers who don't always want to worry about compiling C extensions, but still want performance in production.

## usage

For simple usage:

```python
import mujson as json

json.loads(json.dumps({'hello': 'world!'}))
```

To customize the ranked preference of JSON libraries, including libraries not contemplated by `mujson`:

``` python
from mujson import mujson_function

FAST_JSON_LIBS = ['newjsonlib', 'orjson', 'ujson', 'rapidjson', 'yajl']

fast_dumps = mujson_function('fast_dumps', ranking=FAST_JSON_LIBS)
```

`mujson` implements one additional set of custom mujson functions, called "compliant". These functions use a ranking that excludes JSON libraries that do not support the function signatures supported by corresponding functions in the standard library.

```python
import logging

from mujson import compliant_dumps
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()

logHandler = logging.StreamHandler()
# NOTE: we use `compliant_dumps` because the `JsonFormmatter` makes use of
# kwargs like `cls` and `default` which not all json libraries support. (This
# would not strictly be a concern if this was the only use of mujson in a given
# application, but better safe than sorry.)
formatter = jsonlogger.JsonFormatter(json_serializer=compliant_dumps)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
```

## default rankings

`mujson`'s default rankings are scoped to function and python version. The default rankings are based on the benchmarked performance of common JSON libraries encoding and decoding the JSON data in [bench/json](bench/json). [`bench/json/tweet.json`](bench/json/tweet.json) was given the most weight, under the assumption that it most closely resembles common application data.

### python 3

| library                                                           | dumps | dump | loads | load | compliant |
|:------------------------------------------------------------------|:-----:|:----:|:-----:|:----:|:---------:|
| [orjson](https://github.com/ijl/orjson)                           |  1st  |      |  1st  |      |    no     |
| [metamagic.json](https://github.com/sprymix/metamagic.json)       |  2nd  |      |       |      |    no     |
| [ujson](https://github.com/esnme/ultrajson)                       |  4th  | 2nd  |  2nd  | 1st  |    no     |
| [rapidjson](https://github.com/python-rapidjson/python-rapidjson) |  3rd  | 1st  |  4th  | 3rd  |    yes    |
| [simplejson](https://github.com/simplejson/simplejson)            |  8th  | 6th  |  3rd  | 2nd  |    yes    |
| [json](https://docs.python.org/3.6/library/json.html)             |  6th  | 4th  |  5th  | 4th  |    yes    |
| [yajl](https://github.com/rtyler/py-yajl)                         |  5th  | 3rd  |  7th  | 6th  |    yes    |
| [nssjson](https://github.com/lelit/nssjson)                       |  7th  | 5th  |  6th  | 5th  |    yes    |

### python 2

| library                                                | dumps | dump | loads | load | compliant |
|:-------------------------------------------------------|:-----:|:----:|:-----:|:----:|:---------:|
| [ujson](https://github.com/esnme/ultrajson)            |  1st  | 1st  |  2nd  | 1st  |    no     |
| [cjson](https://github.com/AGProjects/python-cjson)    |  4th  |      |  1st  |      |    no     |
| [yajl](https://github.com/rtyler/py-yajl)              |  2nd  | 2nd  |  5th  | 4th  |    yes    |
| [simplejson](https://github.com/simplejson/simplejson) |  6th  | 5th  |  3rd  | 2nd  |    yes    |
| [nssjson](https://github.com/lelit/nssjson)            |  5th  | 4th  |  4th  | 3rd  |    yes    |
| [json](https://docs.python.org/2/library/json.html)    |  3rd  | 3rd  |  6th  | 5th  |    yes    |

### PyPy

When [PyPy](https://pypy.org/) is used, `mujson` simply falls back to the standard library's `json`, as it currently outperforms all third party libaries.

## running benchmarks

You can build the python 3 benchmarking environment from within the bench directory with something like:

``` shell
$ docker build -t mujson-bench:py3 -f py3.Dockerfile .
```

And you can run the benchmark against any of the provided json files:

``` text
$ docker run -it mujson-bench:py3 10000 tweet.json

***************************************************************************

yajl            decoded tweet.json 10000 times in 559.8183549998339 milliseconds!
nssjson         decoded tweet.json 10000 times in 435.359974999983 milliseconds!
json            decoded tweet.json 10000 times in 399.63585400005286 milliseconds!
rapidjson       decoded tweet.json 10000 times in 356.57377199981966 milliseconds!
simplejson      decoded tweet.json 10000 times in 407.5520390001657 milliseconds!
ujson           decoded tweet.json 10000 times in 350.63891499999045 milliseconds!
orjson          decoded tweet.json 10000 times in 326.77353500002937 milliseconds!
mujson          decoded tweet.json 10000 times in 372.2860130001209 milliseconds!

***************************************************************************

simplejson      encoded tweet.json 10000 times in 439.0100820000953 milliseconds!
nssjson         encoded tweet.json 10000 times in 463.51910400017005 milliseconds!
json            encoded tweet.json 10000 times in 317.38250700004755 milliseconds!
yajl            encoded tweet.json 10000 times in 300.33104299991464 milliseconds!
ujson           encoded tweet.json 10000 times in 247.8906360001929 milliseconds!
rapidjson       encoded tweet.json 10000 times in 177.36121699999785 milliseconds!
metamagic.json  encoded tweet.json 10000 times in 105.27558500007217 milliseconds!
orjson          encoded tweet.json 10000 times in 71.5665820000595 milliseconds!
mujson          encoded tweet.json 10000 times in 72.24357600011899 milliseconds!

***************************************************************************

nssjson         de/encoded tweet.json 10000 times in 991.1501950000456 milliseconds!
simplejson      de/encoded tweet.json 10000 times in 940.1593679999678 milliseconds!
yajl            de/encoded tweet.json 10000 times in 962.6767610000115 milliseconds!
json            de/encoded tweet.json 10000 times in 824.6134749999783 milliseconds!
rapidjson       de/encoded tweet.json 10000 times in 544.7737629999665 milliseconds!
ujson           de/encoded tweet.json 10000 times in 588.3431380000275 milliseconds!
orjson          de/encoded tweet.json 10000 times in 407.2712429999683 milliseconds!
mujson          de/encoded tweet.json 10000 times in 410.43202300011217 milliseconds!

***************************************************************************
```

---

_In computability theory, the **μ** operator, minimization operator, or unbounded search operator searches for the least natural number with a given property._