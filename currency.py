from flask import Flask, request, flash, redirect, render_template, request, session, abort
import json
import requests
import requests_cache
import os
from cassandra.cluster import Cluster

requests_cache.install_cache('rates_api_cache', backend='sqlite', expire_after=36000)
cluster = Cluster(['cassandra'])
session1 = cluster.connect()

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Hello Boss!  <a href="/logout">Logout</a>'

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return str(rates)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

url = 'https://api.exchangeratesapi.io/latest?base={base}'

#I have allowed the user to choose their specific currency in this app,
#for example you can type USD, GBP, EUR or any other currency
#to find out the rate for today.

@app.route('/<currency>',  methods=['GET', 'POST'])
def rates(currency):
    base = request.args.get('base')

    rate_url = url.format(base = currency)
    rates = None
    response = requests.get(rate_url)
    if response.ok:
        rates = response.json()
    else:
        print(response.reason)
    return str(rates)

@app.route('/db/<currency>')
def hello():
    name = request.args.get("name","World")
    return('<h1>The currency is, {}!</h1>'.format(name))

@app.route('/rates/<currency>')
def profile(name):
    rows = session1.execute( """Select * From exchangerates.rates
                            where name = '{}'""".format(name))
    for exchangerates in rows:
        return('<h1>{} has {} exchange rate!</h1>'.format(name,exchangerates.rates))
        return('<h1>This exchange rate does not exist!</h1>')

if __name__=="__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8080, debug=True)
