import argparse
import hashlib
import logging
import os
import requests
import time
from datetime import datetime
from email_service import send_change_email, send_reminder_email


def get_arguments():
    # <email> <link> optional<frequency(h)> optional<no_of_checks> optional<reminder(h)>
    parser = argparse.ArgumentParser(
        description='Detect changes in a web page')
    parser.add_argument('email', metavar='E', type=str, help='email to notify')
    parser.add_argument('link', metavar='L', type=str,
                        help='link to the website')
    parser.add_argument('frequency', metavar='--fr', type=float,
                        help='period of time between comparisons', default=12.0, nargs='?')
    parser.add_argument('checks', metavar='--c', type=int,
                        help='Number of checks before killing script', default=4, nargs='?')
    parser.add_argument('reminder', metavar='--rm', type=float,
                        help='Number of hours which a reminder will be sent', default=168, nargs='?')
    args = parser.parse_args()

    logging.info(
        f'Retrieved arguments. Email={args.email}, Link={args.link}, Frequency={args.frequency}h, Checks={args.checks}')
    return args


def get_page_html(link):
    logging.info(f'Retrieving html for {link}')
    html = requests.get(link).content

    logging.info(f'Successfully retrieved html for {link}')
    return html


def save_page(html, i):
    logging.info(f'Saving html for {i}th time')

    with open(f'page/v{i}', 'w') as f:
        f.write(html)


def get_hash(s):
    return hashlib.md5(s).hexdigest()


if __name__ == "__main__":
    if not os.path.exists('logs/'):
        os.makedirs('logs/')
    if not os.path.exists('page/'):
        os.makedirs('page/')

    logging.basicConfig(filename=f'logs/{datetime.now()}.log',
                        format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

    args = get_arguments()

    wait = args.frequency * 60 * 60  # convert h to s
    reminder_limit = args.reminder * 60 * 60  # convert h to s
    time_since_check = 0
    number_of_hashes_collected = 0

    html = get_page_html(args.link)
    hashed_content = get_hash(html)
    save_page(html, number_of_hashes_collected)

    for i in range(args.checks):
        logging.info('Waiting for another check')
        time.sleep(wait)
        time_since_check += wait

        new_html = get_page_html(args.link)
        new_hash = get_hash(new_html)

        if new_hash != hashed_content:
            logging.info(
                f'Hashes differ, sending notification to {args.email}')
            send_change_email(args.email, args.link)

            number_of_hashes_collected += 1
            save_page(new_html, number_of_hashes_collected)

            hashed_content = new_hash
            time_since_check = 0

        elif time_since_check >= reminder_limit:
            logging.info(
                f'Reminder limit time passed, sending reminder email to {args.email}')
            send_reminder_email(args.email, args.link)

            time_since_check = 0
