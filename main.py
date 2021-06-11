import argparse
import hashlib
import logging
import os
import requests
import time
from datetime import datetime
from email_service import send_email


def get_arguments():
    # <email> <link> optional<frequency(h)> optional<no_of_checks>
    parser = argparse.ArgumentParser(
        description='Detect changes in a web page')
    parser.add_argument('email', metavar='E', type=str, help='email to notify')
    parser.add_argument('link', metavar='L', type=str,
                        help='link to the website')
    parser.add_argument('frequency', metavar='--fr', type=float,
                        help='period of time between comparisons', default=12.0, nargs='?')
    parser.add_argument('checks', metavar='--c', type=int,
                        help='Number of checks before killing script', default=4, nargs='?')
    args = parser.parse_args()

    logging.info(
        f'Retrieved arguments. Email={args.email}, Link={args.link}, Frequency={args.frequency}h, Checks={args.checks}')
    return args


def get_page_hash(link):
    logging.info(f'Retrieving html for {link}')
    html = requests.get(link).content

    logging.info(f'Successfully retrieved, returning hash')
    return hashlib.md5(html).hexdigest()


if __name__ == "__main__":
    if not os.path.exists('logs/'):
        os.makedirs('logs/')
    logging.basicConfig(filename=f'logs/{datetime.now()}.log',
                        format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

    args = get_arguments()

    wait = args.frequency * 60 * 60  # convert h to s
    hashed_content = get_page_hash(args.link)

    for i in range(args.checks):
        logging.info('Waiting for another check')
        # time.sleep(wait)
        new_hash = get_page_hash(args.link)

        if new_hash != hashed_content:
            logging.info(
                f'Hashes differ, sending notification to {args.email}')
            send_email(args.email, args.link)

            hashed_content = new_hash
