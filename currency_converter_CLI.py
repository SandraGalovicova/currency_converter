import sys
import json
import argparse
import currency_converter


def pars_args():
    parser = argparse.ArgumentParser(description='Currency converter')
    parser.add_argument('--amount', type=float, required=True, help='Amount which we want to convert - float')
    parser.add_argument('--input_currency', type=str, required=True,
                        help='A required input currency - 3 letters name/currency symbol')
    parser.add_argument('--output_currency', type=str,
                        help='An optional output currency - 3 letters name/currency symbol')
    args = parser.parse_args()
    return args


def main():
    pars = pars_args()
    result = currency_converter.input_code(pars.amount, pars.input_currency, pars.output_currency)
    if result is None:
        sys.exit(1)
    print(json.dumps(result, indent=4))
    return json.dumps(result, indent=4)


if __name__ == "__main__":
    main()
