import argparse
import logging

import powerbiclient as PBC
from powerbiclient.server import Datasets


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
        all_datasets = server.datasets.get()
        for dataset in all_datasets:
            print(dataset)

        dataset = server.datasets.post_dataset("Test",
            [
               {
                   "name": "Product",
                   "columns": [
                       {
                           "name": "ProductID",
                           "dataType": "Int64"
                       },
                       {
                           "name": "Name",
                           "dataType": "string"
                       },
                       {
                           "name": "Category",
                           "dataType": "string"
                       },
                       {
                           "name": "IsCompete",
                           "dataType": "bool"
                       },
                       {
                           "name": "ManufacturedOn",
                           "dataType": "DateTime"
                       }
                   ]
               }
            ]
        )
        print(dataset)
        dataset = server.datasets.get_by_id(dataset.id)
        print(dataset)
        all_tables = server.tables.get(dataset)
        for table in all_tables:
            print(table)
            rows = [
                {
                    "ProductID": 1,
                    "Name": "Adjustable Race",
                    "Category": "Components",
                    "IsCompete": True,
                    "ManufacturedOn": "07/30/2014"
                },
                {
                    "ProductID": 2,
                    "Name": "LL Crankarm",
                    "Category": "Components",
                    "IsCompete": True,
                    "ManufacturedOn": "07/30/2014"
                },
                {
                    "ProductID": 3,
                    "Name": "HL Mountain Frame - Silver",
                    "Category": "Bikes",
                    "IsCompete": True,
                    "ManufacturedOn": "07/30/2014"
                }
            ]
            server.tables.post_rows(dataset, table, rows)
        server.datasets.refresh(dataset)
        # server.datasets.delete(dataset.id)

        # all_capacities = server.capacities.get()
        all_datasets = server.datasets.get()
        for dataset in all_datasets:
            if dataset.name == 'Test':
                print(dataset)
                # server.datasets.delete(dataset.id)
            # server.datasets.refresh(dataset)
            # all_tables = server.tables.get(dataset)
            # for table in all_tables:
                print(table)
        all_apps = server.apps.get()
        for app in all_apps:
            print(app)


if __name__ == '__main__':
    main()
