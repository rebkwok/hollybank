from datetime import datetime
from django.core.management.base import BaseCommand

from pocketmoney.transactions import add_transaction


WEEKDAYS = {
    'mon': 0,
    'tue': 1,
    'wed': 2,
    'thu': 3,
    'fri': 4,
    'sat': 5,
    'sun': 6
}


class Command(BaseCommand):
    help = 'Make a transaction'

    def add_arguments(self, parser):
        parser.add_argument(
            'transaction_type', choices=['withdraw', 'deposit']
        )
        parser.add_argument(
            'description', help='Description of transaction'
        )
        parser.add_argument('amount')

        parser.add_argument('--only_on', choices=WEEKDAYS.keys())

    def handle(self, *args, **options):

        transaction_type = options.get('transaction_type')
        description = options.get('description')
        amount = options.get('amount')

        only_on = options.get('only_on', '')
        if not only_on or \
                (only_on and WEEKDAYS[only_on] == datetime.today().weekday()):
            if transaction_type == 'withdraw':
                add_transaction(description, '', amount)
            elif transaction_type == 'deposit':
                add_transaction(description, amount, '')

        else:
            self.stdout.write('Not done')
