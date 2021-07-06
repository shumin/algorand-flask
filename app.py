from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from algoapp import generate_account, sender_passphrase, account_balance, receiver_passphrase, transfer_algo, \
    get_two_accounts_status

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('account.html')


@app.route('/transfer')
def transfer():
    return render_template('transfer.html')


@app.route('/delegate')
def delegate():
    return render_template('delegate.html')


@app.route('/atomic_transfer')
def atomic_transfer():
    return render_template('atomictransfer.html')


@app.route('/multisign')
def multisign():
    return render_template('multisign.html')


@app.route('/app/create')
def create_account():
    private_key, address = generate_account()
    return {'sk': private_key, 'address': address, 'passphrase': sender_passphrase}


@app.route('/app/balance')
def get_balance():
    address, bal = account_balance(sender_passphrase)
    return {'address': address, 'balance': str(bal)}


@app.route('/app/transfer_state')
def get_initial_account_states():
    return get_two_accounts_status()


@app.route('/app/do/transfer')
def do_algo_transfer():
    transfer_algo()
    return get_two_accounts_status()


if __name__ == '__main__':
    app.run()