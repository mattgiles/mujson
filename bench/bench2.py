import sys

from timeit import Timer


_import_tpl = 'from {} import ({} as loads, {} as dumps)'


_bin_tmpl = "bin = open('json/{}', 'rb').read()"


_obj = "obj = loads(bin)"


_warm_up = "loads(dumps([]))"


decode_tests = [
    ('json', 'loads', 'dumps'),
    ('yajl', 'loads', 'dumps'),
    ('nssjson', 'loads', 'dumps'),
    ('simplejson', 'loads', 'dumps'),
    ('cjson', 'decode', 'encode'),
    ('ujson', 'loads', 'dumps'),
    ('mujson', 'loads', 'dumps')
]


encode_tests = [
    ('simplejson', 'loads', 'dumps'),
    ('nssjson', 'loads', 'dumps'),
    ('cjson', 'decode', 'encode'),
    ('json', 'loads', 'dumps'),
    ('yajl', 'loads', 'dumps'),
    ('ujson', 'loads', 'dumps'),
    ('mujson', 'loads', 'dumps')
]


decode_encode_tests = [
    ('json', 'loads', 'dumps'),
    ('nssjson', 'loads', 'dumps'),
    ('simplejson', 'loads', 'dumps'),
    ('cjson', 'decode', 'encode'),
    ('yajl', 'loads', 'dumps'),
    ('ujson', 'loads', 'dumps'),
    ('mujson', 'loads', 'dumps')
]


actions = {
    'decoded': 'loads(bin)',
    'encoded': 'dumps(obj)',
    'de/encoded': 'dumps(loads(bin))'
}


def timeit(module, action, num, jsn, import_stmt):
    setup = [import_stmt, _warm_up, _bin_tmpl.format(jsn), _obj]
    try:
        result = Timer(actions[action], '; '.join(setup)).timeit(num) * 1000
        print('{:25s} {} {} {} times in {} milliseconds.'.format(
            module, action, jsn, num, result))
    except:
        print('{:25s} threw Exception trying to {} {} {} times.'.format(
            module, action, jsn, num))


def main(number, jsn):
    print('\n' + '*' * 75 + '\n')

    for mod, dec, enc in decode_tests:
        timeit(mod, 'decoded', number, jsn, _import_tpl.format(mod, dec, enc))

    print('\n' + '*' * 75 + '\n')

    for mod, dec, enc in encode_tests:
        timeit(mod, 'encoded', number, jsn, _import_tpl.format(mod, dec, enc))

    print('\n' + '*' * 75 + '\n')

    for mod, dec, enc in decode_encode_tests:
        timeit(
            mod, 'de/encoded', number, jsn, _import_tpl.format(mod, dec, enc))

    print('\n' + '*' * 75 + '\n')


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(int(sys.argv[1]), sys.argv[2])
