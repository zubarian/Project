from flask import Flask, request
import json
import requests

app = Flask(__name__)

url = 'https://api.exchangeratesapi.io/latest?base={base}'

#I have allowed the user to choose their specific currency in this app,
#for example you can type USD, GBP, EUR or any other currency
#to find out the rate for today.

@app.route('/<currency>',  methods=['GET'])
def rates(currency):
    base = request.args.get('base')

    rate_url = url.format(base = currency)

    response = requests.get(rate_url)
    if response.ok:
        rates = response.json()
    else:
        print(response.reason)

    return str(rates)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
