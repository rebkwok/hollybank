from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.template.response import TemplateResponse
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

from pocketmoney.transactions import (
    get_balance, get_service, get_spreadsheet, add_transaction
)


@login_required
def home_view(request):
    cached_values = cache.get('values', None)
    cached_balance = cache.get('balance', None)
    if cached_values and cached_balance:
        values = json.loads(cached_values)
        balance = float(cached_balance)
    else:
        service = get_service()
        spsheet = get_spreadsheet(service)
        values = spsheet.get('values', [])
        balance = get_balance(service=service, spsheet=spsheet).strip('£')
        balance = float(balance)
        cache.set('values', json.dumps(values), 300)
        cache.set('balance', balance, 300)

    if request.method == 'POST':

        if 'clear' in request.POST:
            cache.clear()
        else:
            service = get_service()
            spsheet = get_spreadsheet(service)

            amount = request.POST['amount']
            description = request.POST['description']
            if 'withdraw' in request.POST:
                add_transaction(
                    description, in_amount='', out_amount=amount,
                    service=service, spsheet=spsheet
                )
                amount = float(amount)
                balance -= amount
                values.append(
                    [datetime.today().strftime('%d-%b-%Y'), description, '',
                     '£%.2f' % amount, '£%.2f' % balance]
                )
            elif 'deposit' in request.POST:
                add_transaction(
                    description, in_amount=amount, out_amount='',
                    service=service, spsheet=spsheet
                )
                amount = float(amount)
                balance += amount
                values.append(
                    [datetime.today().strftime('%d-%b-%Y'), description,
                     '£%.2f' % amount, '', '£%.2f' % balance]
                )

            cache.set('values', json.dumps(values), 300)
            cache.set('balance', balance, 300)
        return HttpResponseRedirect(reverse('web:home'))

    # get last 10 transactions
    if len(values) <= 10:
        values = values
    else:
        values = values[len(values) - 10:]

    return TemplateResponse(
        request, 'web/home.html', {'balance': balance, 'values': values})
