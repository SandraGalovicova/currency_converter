from forex_python.converter import CurrencyRates
from forex_python.converter import RatesNotAvailableError
from collections import OrderedDict

symbol_to_currency_code = {
    'р. ': ['RUB'],
    '฿': ['THB'],
    'Rp': ['IDR'],
    '₩': ['KRW'],
    'zł': ['PLN'],
    '$': ['AUD', 'CAD', 'HKD', 'MXN', 'NZD', 'SGD', 'USD'],
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
    'kr': ['DKK', 'NOK', 'SEK'],
    'R': ['ZAR'],
    '₪': ['ILS'],
    '¥': ['CNY', 'JPY']
}


def input_code(amount, input_currency, output_currency):
    try:
        currency_code_input = symbol_to_currency_code[input_currency]  # try if it is symbol and return code
    except KeyError:
        currency_code_input = [input_currency]  # else try if it is code
    try:
        currency_code_output = symbol_to_currency_code[output_currency]
    except KeyError:
        currency_code_output = [output_currency]
    cnt = 1
    if len(currency_code_input) == 1:
        return print_json(amount, currency_code_input[0], currency_code_output)
    data = OrderedDict()
    for i in range(len(currency_code_input)):  # if input was symbol, there may be more valid codes
        data = print_json(amount, currency_code_input[i], currency_code_output, data, str(cnt))
        cnt += 1
    return data


def get_currency_rate(amount, base_curr, dest_curr):
    result = OrderedDict()
    c = CurrencyRates()
    if dest_curr[0] is None:  # if output is missing, convert to all known currencies
        try:
            courses = c.get_rates(base_curr)
        except RatesNotAvailableError:
            return None
        for key, value in sorted(courses.items()):
            result.update({key: round(value * amount, 2)})
        return result
    if len(dest_curr) == 1:  # if only one output code
        try:
            convert = c.convert(base_curr, dest_curr[0], amount)
            result[dest_curr[0]] = round(convert, 2)
        except RatesNotAvailableError:
            return None
        return result
    try:
        courses = c.get_rates(base_curr)
    except RatesNotAvailableError:
        return None
    for key, value in sorted(courses.items()):  # if output argument was currency symbol, may exists more valid codes
        if key in dest_curr:
            result.update({key: round(value * amount, 2)})
    return result


def print_json(amount, input_currency, output_currency, data=OrderedDict(), i=''):
    output = get_currency_rate(amount, input_currency, output_currency)
    if output is None:
        return None
    data['input' + i] = OrderedDict({'amount': amount})
    data['input' + i].update({'currency': input_currency})
    data['output' + i] = output
    return data

