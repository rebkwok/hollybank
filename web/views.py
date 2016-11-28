from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.template.response import TemplateResponse

from pocketmoney.transactions import (
    get_balance, get_spreadsheet, add_transaction
)


@login_required
def home_view(request):
    service, spsheet = get_spreadsheet()
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        if 'withdraw' in request.POST:
            add_transaction(
                description, in_amount='', out_amount=amount,
                service=service, spsheet=spsheet
            )
        elif 'deposit' in request.POST:
            add_transaction(
                description, in_amount=amount, out_amount='',
                service=service, spsheet=spsheet
            )
    balance =get_balance(service=service, spsheet=spsheet)

    values = spsheet.get('values', [])
    # get last 10 transactions
    if len(values) <= 10:
        values = values
    else:
        values = values[len(values) - 10:]

    return TemplateResponse(
        request, 'web/home.html', {'balance': balance, 'values': values})
