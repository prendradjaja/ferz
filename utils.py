def readable(dt):
    return dt.strftime('%b %d %Y at %H:%M')


def prettify_moves(moves):
    result = []
    for n, i in enumerate(range(0, len(moves), 2), start=1):
        result.append('{}.{}'.format(n, moves[i]))
        try:
            result.append(moves[i + 1])
        except IndexError:
            pass

    return ' '.join(result)
