import argparse
import json
import locale
from forex_python.converter import CurrencyRates
from flask import Flask, request, Response

def pars_args():
    parser = argparse.ArgumentParser(description='Currency converter')
    parser.add_argument('--amount', type=float, help='Amount which we want to convert - float')
    parser.add_argument('--input_currency', type=str, help='A required input currency - 3 letters name/currency symbol')
    parser.add_argument('--output_currency', type=str, nargs='?',
                        help='An optional output currency - 3 letters name/currency symbol')
    args = parser.parse_args()
    return args


def get_currency_rate(amount, base_curr, dest_curr):
    result = {}
    c = CurrencyRates()
    if not dest_curr:
        courses = c.get_rates(base_curr)
        for key, value in courses.items():
            result[key] = value * amount
        return result
    else:
        result[dest_curr] = []
        convert = c.convert(base_curr, dest_curr, amount)
        result[dest_curr].append(convert)
        return result


def print_json(amount, input_currency, output_currency):
    data = {'input': {
        'amount': amount,
        'currency': input_currency},
        'output': get_currency_rate(amount, input_currency, output_currency)}
    return json.dumps(data, sort_keys=True, indent=4)


"""def get_code(currency_symbol):
    locale.setlocale(locale.LC_MONETARY, '')
    for name in locale.locale_alias:
        print(name)
        normalized = locale.normalize(name)
        print(normalized)
        locale.setlocale(locale.LC_ALL, normalized)
        conv = locale.localeconv()
        if conv['currency_symbol'] == currency_symbol:
            return conv['int_curr_symbol']"""

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
    result = print_json(amount, base_curr, dest_curr)
    return result


#app.run(debug=True)

def main():
    pars = pars_args()
    return print_json(pars.amount, pars.input_currency, pars.output_currency)


if __name__ == "__main__":
    main()