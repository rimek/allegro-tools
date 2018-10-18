#!/usr/bin/env python
import argparse
import os
import sys

from requests.exceptions import ConnectionError

from multisearch import MultiSearch


def load_api_key():
    try:
        return os.environ.get('ALLEGRO_API_KEY')
    except KeyError:
        print("You have to provide a ALLEGRO_API_KEY environment variable "
              "with the allegro api key", file=sys.stderr)  # noqa
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Allegro MultiSearch.')
    parser.add_argument('query', metavar='N', type=str, nargs='+', action='append',
                        help='Query strings to search')
    args = parser.parse_args()

    app = MultiSearch(api_key=load_api_key())

    try:
        print('Queries:', args.query[0])

        for query in args.query[0]:
            app.fetch_results({'search': query})

        print('\nResults:')
        items = app.match_uid()
        if not items:
            print('No results')
            sys.exit(0)

        for uid, items in items.items():
            print('\n---%s---\n' % uid)

            [item.display() for item in items]
    except ConnectionError as e:
        print('Connection error: %s ' % e, file=sys.strerr)
    except Exception as e:
        print('Error: %s ' % e, file=sys.strerr)
        import traceback
        traceback.print_exc()
