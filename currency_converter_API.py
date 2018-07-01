import currency_converter
from flask import Flask, request, jsonify, Response


app = Flask(__name__)


@app.route('/currency_converter', methods=['GET'])
def web_api():
    if not request.args.get('amount', None, float):  # required argument
        return Response("Wrong amount argument.", status=400)
    amount = request.args.get('amount', None, float)
    if not request.args.get('input_currency', None, str):  # required argument
        return Response("Wrong input currency.", status=400)
    base_curr = request.args.get('input_currency', None, str)
    dest_curr = request.args.get('output_currency', None, str)
    result = currency_converter.main(amount, base_curr, dest_curr)
    if result is None:
        return Response("Wrong argument", status=400)
    return jsonify(result)


def main():
    app.run()  # /currency_converter?amount=5&input_currency=USD


if __name__ == "__main__":
    main()


