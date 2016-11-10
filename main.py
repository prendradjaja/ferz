import argparse
from datetime import datetime
import requests
import time
import json


LICHESS_URL = 'https://en.lichess.org'
PAGE_SIZE = 100


def main(username, num_pages, output_path):
    games = []

    # TODO is it bad to use my own page enumeration despite the API having a 'nextPage'?
    # TODO what happens if you reach the last page of games?

    for i in range(1, 1 + num_pages):
        partial_print('Fetching games... ')
        # API seems to exclude aborted games
        response = requests.get('{}/api/user/{}/games'.format(LICHESS_URL, username),
                                params={'with_moves': 1,
                                        'nb': PAGE_SIZE,
                                        'page': i})
        assert response.status_code == 200, 'Response code was {}'.format(response.status_code)

        page = [g for g in response.json()['currentPageResults']]
        games.extend(page)
        partial_print('{n} total up to {earliest}. '
                .format(n = len(games),
                        earliest = readable_date(page[-1]['createdAt'])))

        if i != num_pages:
            partial_print('Sleeping for one second.')
            time.sleep(1)

        print()

        if not response.json()['nextPage']:
            break

    if not output_path:
        output_path = '{username}--{timestamp}.json'.format(
                          username=username,
                          timestamp=datetime.now().strftime('%Y-%m-%d--%H-%M'))
    print()
    print('Dumping output to file: ' + output_path)
    with open(output_path, 'w') as output_file:
        json.dump(games, output_file)


def partial_print(s):
    print(s, end='', flush=True)


def readable_date(unix_time_ms):
    return datetime.fromtimestamp(unix_time_ms/1000).strftime('%b %d %Y at %H:%M')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('username',
                        help='the user whose games you want to download')
    parser.add_argument('-n', default=5, type=int,
                        help='number of "pages" to download (each page is 100 games; ' +
                             'default is 5 pages)')
    parser.add_argument('-o',
                        help='output file')
    args = parser.parse_args()

    main(args.username, args.n, args.o)
