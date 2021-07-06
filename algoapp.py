import json

from algosdk import account, mnemonic
from algosdk.future.transaction import PaymentTxn
from algosdk.v2client import algod

from util import wait_for_confirmed_txn

# they are only for test, please use your own passphrase and do not use them in prduction
sender_passphrase = 'atom exclude camp home dwarf forest noble diesel slush organ gold poet cry cover neck cigar radar cram season cage actress dynamic funny ability parent'
receiver_passphrase = 'require pen civil diary lion common need used tribe six mango pitch region drip rubber curve twelve moral garlic area wing clarify theme about soup'


def get_client():
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    return algod.AlgodClient(algod_token, algod_address)


def generate_account():
    return account.generate_account()


def get_two_accounts_status():
    sender_add, sender_bal = account_balance(sender_passphrase)
    receiver_add, receiver_bal = account_balance(receiver_passphrase)
    return {'sender_add': sender_add, 'sender_bal': sender_bal, 'receiver_add': receiver_add, 'receiver_bal': receiver_bal}


def account_balance(passphrase):
    algod_client = get_client()
    sender_address = mnemonic.to_public_key(passphrase)
    account_info = algod_client.account_info(sender_address)
    print("Account info")
    print(json.dumps(account_info, indent=4))
    return sender_address, account_info.get('amount')


def transfer_algo():
    algod_client = get_client()

    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = 1000  # this is the minimum fee

    sender_address = mnemonic.to_public_key(sender_passphrase)
    sender_private_key = mnemonic.to_private_key(sender_passphrase)
    receiver_address = mnemonic.to_public_key(receiver_passphrase)
    note = 'Bill paid'.encode()
    amount_to_be_paid = 2 * 1000000  # 2 Algos in micro format

    unsigned_txn = PaymentTxn(sender_address, params, receiver_address, amount_to_be_paid, None, note)
    signed_txn = unsigned_txn.sign(sender_private_key)
    txn_id = algod_client.send_transaction(signed_txn)
    print('A signed transaction sent with id: {}'.format(txn_id))

    try:
        return wait_for_confirmed_txn(algod_client, txn_id, 5)
    except Exception as e:
        print(e)
        return {'msg': 'failed', 'err': str(e)}


def get_node_status():
    status = get_client().status()
    return json.dumps(status, indent=4)


def get_suggested_param():
    try:
        params = get_client().suggested_params()
        return json.dumps(vars(params), indent=4)
    except Exception as e:
        print(e)
