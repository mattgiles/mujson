import collections
import inspect
import json
import sys

json_module = collections.namedtuple('json_module', 'load loads dump dumps')

try:
    import ujson  # https://github.com/esnme/ultrajson
except ImportError:
    ujson = False

try:
    import rapidjson  # https://github.com/python-rapidjson/python-rapidjson
except ImportError:
    rapidjson = False

try:
    import simplejson  # https://github.com/simplejson/simplejson
except ImportError:
    simplejson = False

try:
    import nssjson  # https://github.com/lelit/nssjson
except ImportError:
    nssjson = False

try:
    import yajl  # https://github.com/rtyler/py-yajl
except ImportError:
    yajl = False

try:
    import cjson  # https://github.com/AGProjects/python-cjson
    cjson = json_module(
        dump=None, dumps=cjson.encode, load=None, loads=cjson.decode)
except ImportError:
    cjson = None

try:
    import metamagic.json as mjson  # https://github.com/sprymix/metamagic.json
except ImportError:
    mjson = False


NON_COMPLIANT = [ujson, cjson, mjson]


# NOTE(mattgiles): default rankings are based on benchmarked performance
# encoding and decoding the "tweet" json at mujson/bench/json/tweet.json,
# as a best guess at representative json for most applications.
if sys.version_info.major == 3:
    basestring = str
    dump_rank = [mjson, rapidjson, ujson, yajl, json, nssjson, simplejson]
    dumps_rank = [mjson, rapidjson, ujson, yajl, json, nssjson, simplejson]
    load_rank = [ujson, yajl, json, nssjson, simplejson, rapidjson]
    loads_rank = [ujson, yajl, json, nssjson, simplejson, rapidjson]

else:
    dump_rank = [ujson, yajl, json, cjson, nssjson, simplejson]
    dumps_rank = [ujson, yajl, json, cjson, nssjson, simplejson]
    load_rank = [ujson, cjson, simplejson, nssjson, yajl, json]
    loads_rank = [ujson, cjson, simplejson, nssjson, yajl, json]


default_rankings = {
    'compliant_dump': [mod for mod in dump_rank if mod not in NON_COMPLIANT],
    'compliant_dumps': [mod for mod in dumps_rank if mod not in NON_COMPLIANT],
    'compliant_load': [mod for mod in load_rank if mod not in NON_COMPLIANT],
    'compliant_loads': [mod for mod in loads_rank if mod not in NON_COMPLIANT],
    'dump': [mod for mod in dump_rank],
    'dumps': [mod for mod in dumps_rank],
    'load': [mod for mod in load_rank],
    'loads': [mod for mod in loads_rank]
}


def prepare_module_ranking(rank):
    ranking = []
    for module in rank:
        if isinstance(module, basestring):
            if module not in globals():
                try:
                    globals()[module] = __import__(module)
                except ModuleNotFoundError:
                    globals()[module] = False
            if globals()[module]:
                ranking.append(globals()[module])
        else:
            if module:
                ranking.append(module)
    return ranking


def choose_json_function(func_name, ranking, **kwargs):
    """Choose the "best" available json function.

    Compares a ranking of preferred json modules with what is available for
    import, choosing the first available that supports invoked kwargs.

    Args:
        func_name (str): name of function to choose. Must be one of: "load",
          "loads", "dump", "dumps", "compliant_load", "compliant_loads",
          "compliant_dump", "compliant_dumps".
        ranking (list|None): if a list, will use ranking when evaluating the
          best module available. If None, rthe default rankings will be used.

    """
    ranking = ranking or default_rankings[func_name]
    ranking = prepare_module_ranking(ranking)
    func_name = func_name.replace('compliant_', '')
    if not kwargs:
        return getattr(ranking[0], func_name)
    for module in ranking:
        try:
            func = getattr(module, func_name)
            if set(kwargs.keys()).issubset(inspect.getargspec(func)[0]):
                return func
        except (AttributeError, TypeError, ValueError):
            continue
    raise TypeError('{}() got an unexpected kwarg'.format(func_name))


def negotiated_json_function(func_name, ranking=None):
    """Use the best available version of some common json function.

    The performance ranking of different json libraries varies widely based on
    the actual JSON data being encoded or decoded. It may be desirable to pass
    your own `ranking` based on your knowledge of the common shape or
    characteristics of the JSON data relevant to your library/application.

    Args:
        func_name (str): name of function to choose. Must be one of: "load",
          "loads", "dump", "dumps", "compliant_load", "compliant_loads",
          "compliant_dump", "compliant_dumps".
        ranking (list): if a list, will use ranking when evaluating
          the best module available. If not passed, the default rankings will
          be used.

    NOTE(mattgiles): the returned function behaves differently the first time
    it is invoked, compared to all subsequent times. On first invocation,
    before any desired output is returned, the "best" implementation of the
    desired json function available for import is selected and made to replace
    the temporary function returned by `negotiated_json_function` in the global
    namespace. The reason for this hackery is because, given the implicit
    desire for speed, extra function calls are are needlessly slow.

    NOTE(mattgiles): there is here implemented a notion of "compliant" vs
    "non-compliant" json functions, which is a pragmatic simplification used to
    mean "supports common kwargs supported by the sdtlib's json library". Users
    of this library can choose to use "compliant_*" versions of standard
    functions to avoid mixed use of json functions in their own libraries, i.e.
    with and without various kwargs, throwing runtime errors that depend on
    which invokation signatures hit `temp_json_func` first. In reality, there
    are subtle differences in the behavior of different implementations of JSON
    encoding and decoding that make virtually all 3rd party implementations
    strictly "non-compliant". A best effort is here made to ensure that first
    invoked usage is supported by the returned json function, but this DYNAMIC
    behavior may lead to confusion and/or NON-DETERMINISTIC behavior in larger
    or more complex libraries, or in the applications which ultimately dictate
    behavior. In cases where the simple distinction between compliance and
    non-compliance is insufficient, an `ranking of modules should be
    provided as a means of avoiding unwanted behavior.

    """
    def temp_json_func(*args, **kwargs):
        func = choose_json_function(func_name, ranking, **kwargs)
        globals()[func_name] = func
        return func(*args, **kwargs)

    return temp_json_func


load = negotiated_json_function('load')
loads = negotiated_json_function('loads')
dump = negotiated_json_function('dump')
dumps = negotiated_json_function('dumps')

compliant_load = negotiated_json_function('compliant_load')
compliant_loads = negotiated_json_function('compliant_loads')
compliant_dump = negotiated_json_function('compliant_dump')
compliant_dumps = negotiated_json_function('compliant_dumps')
