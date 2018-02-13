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

For more sophisticated usage, please see doc strings, but consider:

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

To customize the ranked order of JSON libraries:

``` python
from mujson import negotiated_json_function

RANKED_JSON_LIBS = ['ujson', 'rapidjson', 'yajl']

json_dumps = negotiated_json_function('json_dumps', ranking=RANKED_JSON_LIBS)
```

## todo

- turn over idea of "compliance"
- implement checks at import time to see if libraries with optional speedups were successfully installed with speedups in place, as that impacts the assumptions behind the default rankings.