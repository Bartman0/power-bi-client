import argparse
import logging

import powerbiclient as PBC
import random
import datetime
import time
import openpyxl as xl


def main():

    parser = argparse.ArgumentParser(description='List datasets from Power-BI')
    parser.add_argument('--application_id', '-i', required=True, help='application ID to sign into with')
    parser.add_argument('--application_secret', '-s', required=True, help='application secret to sign into with')
    parser.add_argument('--username', '-u', required=True, help='username to sign into with')
    parser.add_argument('-p', '--password', required=True, default=None)
    parser.add_argument('--logging-level', '-l', choices=['debug', 'info', 'error'], default='error',
                        help='desired logging level (set to error by default)')

    parser.add_argument('workbook', help='one or more excel workbooks to publish', nargs='+')

    args = parser.parse_args()

    # Set logging level based on user input, or error by default
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)

    # Step 1: Sign in to server.
    powerbi_auth = PBC.PowerBIAuth(args.application_id, args.application_secret, args.username, args.password)
    server = PBC.Server()

    with server.auth.acquire_token(powerbi_auth):
        for fname in args.workbook:
            wb = xl.load_workbook(filename=fname)
            sheet = wb.active
            dataset = server.datasets.get_by_name(fname)
            data = []
            for i, row in enumerate(sheet.values):
                if i == 0:
                    columns = [ { "name": c, "dataType": "String" } for c in row ]
                    if dataset is None:
                        dataset = server.datasets.post_dataset(fname,
                            [
                                {
                                    "name": wb.sheetnames[0],
                                    "columns": columns
                                }
                            ],
                            default_retention_policy='None'
                        )
                else:
                    data.append({ columns[i]['name']: c for i,c in enumerate(row) })
            server.datasets.post_rows(dataset, wb.sheetnames[0], data)


if __name__ == '__main__':
    main()
