import argparse
import logging

import powerbiclient as PBC
import random
import datetime
import time


def main():

    parser = argparse.ArgumentParser(description='List datasets from Power-BI')
    parser.add_argument('--application_id', '-i', required=True, help='application ID to sign into with')
    parser.add_argument('--application_secret', '-s', required=True, help='application secret to sign into with')
    parser.add_argument('--username', '-u', required=True, help='username to sign into with')
    parser.add_argument('-p', '--password', required=True, default=None)
    parser.add_argument('--logging-level', '-l', choices=['debug', 'info', 'error'], default='error',
                        help='desired logging level (set to error by default)')

    args = parser.parse_args()

    # Set logging level based on user input, or error by default
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)

    # Step 1: Sign in to server.
    powerbi_auth = PBC.PowerBIAuth(args.application_id, args.application_secret, args.username, args.password)
    server = PBC.Server()

    with server.auth.acquire_token(powerbi_auth):
        dataset = server.datasets.get_by_name("Realtime")
        dataset_id = dataset.id
        if dataset_id == '':
            dataset = server.datasets.post_dataset("Realtime",
                [
                   {
                       "name": "Measurements",
                       "columns": [
                           {
                               "name": "Timestamp",
                               "dataType": "DateTime"
                           },
                           {
                               "name": "Value",
                               "dataType": "Double"
                           }
                       ]
                   }
                ],
                default_retention_policy='basicFIFO'
            )
        print(dataset)
        table = server.datasets.get_table_by_name(dataset, 'Measurements')
        for tick in range(1000000):
            now = datetime.datetime.now()
            rows = [
                {
                    "Timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "Value": 20+random.uniform(0, 10)-5     # random value between 15 and 25
                }
            ]
            server.datasets.post_rows(dataset, table.name, rows)
            time.sleep(0.5)     # push dataset limit: 2 requests/s


if __name__ == '__main__':
    main()
