import sys

from timeit import Timer


_bin_tmpl = "bin = open('json/{}', 'rb').read()"


_obj = "obj = loads(bin)"


decode_tests = [
    ('json', 'loads'),
    ('yajl', 'loads'),
    ('nssjson', 'loads'),
    ('simplejson', 'loads'),
    ('cjson', 'decode'),
    ('ujson', 'loads'),
    ('mujson', 'loads')
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
    setup = [import_stmt, _bin_tmpl.format(jsn), _obj]
    try:
        result = Timer(actions[action], '; '.join(setup)).timeit(num) * 1000
        print('{:25s} {} {} {} times in {} milliseconds.'.format(
            module, action, jsn, num, result))
    except:
        print('{:25s} threw Exception trying to {} {} {} times.'.format(
            module, action, jsn, num))


def main(number, jsn):
    print('\n' + '*' * 75 + '\n')

    for mod, dec in decode_tests:
        import_stmt = 'from {} import {} as loads; loads("[]")' \
            .format(mod, dec)
        timeit(mod, 'decoded', number, jsn, import_stmt)

    print('\n' + '*' * 75 + '\n')

    for mod, dec, enc in encode_tests:
        import_stmt = (
            'from {} import ({} as loads, {} as dumps); '
            'dumps([])'.format(mod, dec, enc))
        timeit(mod, 'encoded', number, jsn, import_stmt)

    print('\n' + '*' * 75 + '\n')

    for mod, dec, enc in decode_encode_tests:
        import_stmt = (
            'from {} import ({} as loads, {} as dumps); '
            'loads(dumps([]))'.format(mod, dec, enc))
        timeit(mod, 'de/encoded', number, jsn, import_stmt)

    print('\n' + '*' * 75 + '\n')


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(int(sys.argv[1]), sys.argv[2])
