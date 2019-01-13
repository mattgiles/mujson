import sys

from timeit import Timer


DECODE_TESTS = [
    ('json', 'loads', 'dumps'),
    ('yajl', 'loads', 'dumps'),
    ('nssjson', 'loads', 'dumps'),
    ('simplejson', 'loads', 'dumps'),
    ('ujson', 'loads', 'dumps'),
    ('cjson', 'decode', 'encode'),
    ('mujson', 'loads', 'dumps')
]


ENCODE_TESTS = [
    ('simplejson', 'loads', 'dumps'),
    ('nssjson', 'loads', 'dumps'),
    ('cjson', 'decode', 'encode'),
    ('json', 'loads', 'dumps'),
    ('yajl', 'loads', 'dumps'),
    ('ujson', 'loads', 'dumps'),
    ('mujson', 'loads', 'dumps')
]


DECODE_ENCODE_TESTS = [
    ('json', 'loads', 'dumps'),
    ('yajl', 'loads', 'dumps'),
    ('nssjson', 'loads', 'dumps'),
    ('simplejson', 'loads', 'dumps'),
    ('ujson', 'loads', 'dumps'),
    ('cjson', 'decode', 'encode'),
    ('mujson', 'loads', 'dumps')
]


ACTIONS = {
    'decoded': 'loads(bin)',
    'encoded': 'dumps(obj)',
    'de/encoded': 'dumps(loads(bin))'
}


ASCII_BREAK = '\n' + '*' * 75 + '\n'


_import_tpl = 'from {} import ({} as loads, {} as dumps)'


_bin_tmpl = "bin = open('json/{}', 'rb').read()"


_obj = "obj = loads(bin)"


_warm_up = "loads(dumps([]))"


def timeit(module, action, num, jsn, import_stmt):
    setup = [import_stmt, _warm_up, _bin_tmpl.format(jsn), _obj]
    try:
        result = Timer(ACTIONS[action], '; '.join(setup)).timeit(num) * 1000
        print('{:25s} {} {} {} times in {} milliseconds.'.format(
            module, action, jsn, num, result))
    except:
        raise
        print('{:25s} threw Exception trying to {} {} {} times.'.format(
            module, action, jsn, num))


def main(number, jsn):
    print(ASCII_BREAK)

    for module, decoder, encoder in DECODE_TESTS:
        import_stmt = _import_tpl.format(module, decoder, encoder)
        timeit(module, 'decoded', number, jsn, import_stmt)

    print(ASCII_BREAK)

    for module, decoder, encoder in ENCODE_TESTS:
        import_stmt = _import_tpl.format(module, decoder, encoder)
        timeit(module, 'encoded', number, jsn, import_stmt)

    print(ASCII_BREAK)

    for module, decoder, encoder in DECODE_ENCODE_TESTS:
        import_stmt = _import_tpl.format(module, decoder, encoder)
        timeit(module, 'de/encoded', number, jsn, import_stmt)

    print(ASCII_BREAK)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(int(sys.argv[1]), sys.argv[2])
