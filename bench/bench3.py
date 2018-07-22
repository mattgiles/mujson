import sys

from timeit import Timer


_import_tpl = 'from {} import (dumps, loads)'


_bin_tmpl = "bin = open('json/{}', 'r').read()"


_obj = "obj = loads(bin)"


_warm_up = "loads(dumps([]))"


decode_tests = [
    'rapidjson',
    'simplejson',
    'nssjson',
    'json',
    'yajl',
    'ujson',
    'mujson'
]


encode_tests = [
    'simplejson',
    'nssjson',
    'json',
    'yajl',
    'ujson',
    'rapidjson',
    'metamagic.json',
    'mujson'
]


decode_encode_tests = [
    'nssjson',
    'simplejson',
    'json',
    'yajl',
    'rapidjson',
    'ujson',
    'mujson'
]


actions = {
    'decoded': 'loads(bin)',
    'encoded': 'dumps(obj)',
    'de/encoded': 'dumps(loads(bin))'
}


def timeit(mod, act, num, jsn, import_stmt):
    setup = [import_stmt, _warm_up, _bin_tmpl.format(jsn), _obj]
    try:
        msecs = Timer(actions[act], '; '.join(setup)).timeit(num) * 1000
        print(f'{mod:15s} {act} {jsn} {num} times in {msecs} milliseconds!')
    except:
        print(f'{mod:15s} threw Exception trying to {act} {jsn} {num} times!')


def main(number, jsn):
    print('\n' + '*' * 75 + '\n')

    for mod in decode_tests:
        timeit(mod, 'decoded', number, jsn, _import_tpl.format(mod))

    print('\n' + '*' * 75 + '\n')

    for mod in encode_tests:
        timeit(mod, 'encoded', number, jsn, _import_tpl.format(mod))

    print('\n' + '*' * 75 + '\n')

    for mod in decode_encode_tests:
        timeit(mod, 'de/encoded', number, jsn, _import_tpl.format(mod))

    print('\n' + '*' * 75 + '\n')


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(int(sys.argv[1]), sys.argv[2])
