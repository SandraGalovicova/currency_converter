import argparse
import json
import sys
from forex_python.converter import CurrencyRates
from forex_python.converter import RatesNotAvailableError
from flask import Flask, request, Response
from collections import OrderedDict


symbol_to_currency_code = {
    'р. ': ['RUB'],
    '฿': ['THB'],
    'Rp': ['IDR'],
    '₩': ['KRW'],
    'zł': ['PLN'],
    '$': ['CAD','AUD', 'MXN', 'USD', 'HKD', 'SGD', 'NZD'],
    '£': ['GBP'],
    '₤': ['TRY'],
    'L': ['RON'],
    'Kn': ['HRK'],
    'лв': ['BGN'],
    'Ft': ['HUF'],
    'R$': ['BRL'],
    'Kč': ['CZK'],
    'Kr': ['ISK'],
    'RM': ['MYR'],
    '€': ['EUR'],
    '₱': ['PHP'],
    '₨': ['INR'],
    '₣': ['CHF'],
    'kr': ['NOK', 'SEK', 'DKK'],
    'R': ['ZAR'],
    '₪': ['ILS'],
    '¥': ['CNY', 'JPY']
}


def pars_args():
    parser = argparse.ArgumentParser(description='Currency converter')
    parser.add_argument('--amount', type=float, help='Amount which we want to convert - float')
    parser.add_argument('--input_currency', type=str, help='A required input currency - 3 letters name/currency symbol')
    parser.add_argument('--output_currency', type=str, nargs='?',
                        help='An optional output currency - 3 letters name/currency symbol')
    args = parser.parse_args()
    return args


def input_code(amount, input_currency, output_currency):
    try:
        currency_code_input = symbol_to_currency_code[input_currency]
    except KeyError:
        currency_code_input = [input_currency]
    try:
        currency_code_output = symbol_to_currency_code[output_currency]
    except KeyError:
        currency_code_output = [output_currency]
    cnt = 1
    if len(currency_code_input) == 1:
        return print_json(amount, currency_code_input[0], currency_code_output)
    data = OrderedDict()
    for i in range(len(currency_code_input)):
        data = print_json(amount, currency_code_input[i], currency_code_output, data, str(cnt))
        cnt += 1
    return data


def get_currency_rate(amount, base_curr, dest_curr):
    result = {}
    c = CurrencyRates()
    if dest_curr[0] is None:
        try:
            courses = c.get_rates(base_curr)
        except RatesNotAvailableError:
            return None
        for key, value in courses.items():
            result[key] = value * amount
        return result
    if len(dest_curr) == 1:
        try:
            convert = c.convert(base_curr, dest_curr[0], amount)
            result[dest_curr[0]] = convert
        except RatesNotAvailableError:
            return None
        return result
    try:
        courses = c.get_rates(base_curr)
    except RatesNotAvailableError:
        return None
    for key, value in courses.items():
        if key in dest_curr:
            result[key] = value * amount
    return result


def print_json(amount, input_currency, output_currency, data=OrderedDict(), i=''):
    output = get_currency_rate(amount, input_currency, output_currency)
    if output is None:
        return None
    data['input'+i] = {
        'amount': amount,
        'currency': input_currency}
    data['output'+i] = output
    return data


app = Flask(__name__)


@app.route('/currency_converter', methods=['GET'])
def web_api():
    if not request.args.get('amount', None, float):
        return Response("Wrong amount argument.", status=400)
    amount = request.args.get('amount', None, float)
    if not request.args.get('input_currency', None, str):
        return Response("Wrong input currency.", status=400)
    base_curr = request.args.get('input_currency', None, str)
    dest_curr = request.args.get('output_currency', None, str)
    result = input_code(amount, base_curr, dest_curr)
    if result is None:
        return Response("Wrong argument", status=400)
    return json.dumps(result, indent=4)


def main():
    if 2 <= len(sys.argv) <= 7:  # --amount 10.92 --input_currency $ --output_currency $
        pars = pars_args()
        result = input_code(pars.amount, pars.input_currency, pars.output_currency)
        if result is None:
            sys.exit(1)
        #print(json.dumps(result, indent=4))
        return json.dumps(result, indent=4)
    else:
        app.run()  # /currency_converter?amount=5&input_currency=USD


if __name__ == "__main__":
    main()

