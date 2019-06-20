import argparse
import logging

import powerbiclient as PBC
import random
import datetime
import time


def main():

    parser = argparse.ArgumentParser(description='Refresh one or more datasets in Power-BI')
    parser.add_argument('--application_id', '-i', required=True, help='application ID to sign into with')
    parser.add_argument('--application_secret', '-s', required=True, help='application secret to sign into with')
    parser.add_argument('--username', '-u', required=True, help='username to sign into with')
    parser.add_argument('-p', '--password', required=True, default=None)
    parser.add_argument('--logging-level', '-l', choices=['debug', 'info', 'error'], default='error',
                        help='desired logging level (set to error by default)')

    parser.add_argument('dataset', help='one or more datasets to publish', nargs='+')

    args = parser.parse_args()

    # Set logging level based on user input
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)

    # Step 1: Sign in to server.
    powerbi_auth = PBC.PowerBIAuth(args.application_id, args.application_secret, args.username, args.password)
    server = PBC.Server()

    with server.auth.acquire_token(powerbi_auth):
        for name in args.dataset:
            dataset = server.datasets.get_by_name(name)
            server.datasets.refresh(dataset)
            print("dataset {0} refreshed".format(name))


if __name__ == '__main__':
    main()
