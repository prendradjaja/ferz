from typing import List

def _transpose(matrix: List[List]) -> List[List]:
    return list(map(list, zip(*matrix)))

def _multi_compose(functions, x):
    for f in functions:
        x = f(x)
    return x

def format_table(table, column_formatters):
    WIDTH = len(table[0])
    HEIGHT = len(table)

    assert all(len(row) == WIDTH for row in table), 'table must be rectangular'
    assert len(column_formatters) == WIDTH, 'wrong number of formatters'

    table_t = _transpose(table)
    table_formatted = _transpose([
        [_multi_compose(functions, item) for item in row]
        for functions, row in zip(column_formatters, table_t)
    ])
    return '\n'.join('  '.join(row) for row in table_formatted)
