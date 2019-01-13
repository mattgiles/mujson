import sys

from timeit import Timer


DECODE_TESTS = [
    'yajl',
    'nssjson',
    'json',
    'rapidjson',
    'simplejson',
    'ujson',
    'orjson',
    'mujson'
]


ENCODE_TESTS = [
    'simplejson',
    'nssjson',
    'json',
    'yajl',
    'ujson',
    'rapidjson',
    'metamagic.json',
    'orjson',
    'mujson'
]


DECODE_ENCODE_TESTS = [
    'nssjson',
    'simplejson',
    'yajl',
    'json',
    'rapidjson',
    'ujson',
    'orjson',
    'mujson'
]


ACTIONS = {
    'decoded': 'loads(bin)',
    'encoded': 'dumps(obj)',
    'de/encoded': 'dumps(loads(bin))'
}


ASCII_BREAK = '\n' + '*' * 75 + '\n'


_import_tpl = 'from {} import (dumps, loads)'


_bin_tmpl = "bin = open('json/{}', 'r').read()"


_obj = "obj = loads(bin)"


_warm_up = "loads(dumps([]))"


def timeit(mod, act, num, jsn, import_stmt):
    setup = [import_stmt, _warm_up, _bin_tmpl.format(jsn), _obj]
    try:
        msecs = Timer(ACTIONS[act], '; '.join(setup)).timeit(num) * 1000
        print(f'{mod:15s} {act} {jsn} {num} times in {msecs} milliseconds!')
    except:
        print(f'{mod:15s} threw Exception trying to {act} {jsn} {num} times!')


def main(number, jsn):
    print(ASCII_BREAK)

    for module in DECODE_TESTS:
        timeit(module, 'decoded', number, jsn, _import_tpl.format(module))

    print(ASCII_BREAK)

    for module in ENCODE_TESTS:
        timeit(module, 'encoded', number, jsn, _import_tpl.format(module))

    print(ASCII_BREAK)

    for module in DECODE_ENCODE_TESTS:
        timeit(module, 'de/encoded', number, jsn, _import_tpl.format(module))

    print(ASCII_BREAK)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(int(sys.argv[1]), sys.argv[2])
