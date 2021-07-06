import json
from algosdk.v2client.algod import AlgodClient


def wait_for_confirmed_txn(algod_client: AlgodClient, txn_id, timeout_attempts):
    last_round = algod_client.status()['last-round']
    print('Status of last-round {}'.format(last_round))

    start_round = last_round + 1
    next_round = start_round

    while next_round < start_round + timeout_attempts:
        try:
            txn_info = algod_client.pending_transaction_info(txn_id)
        except Exception as e:
            print('Failed to confirm pending txn {}'.format(txn_id))
            print(e)
            return

        print('Status of confirm-round {}'.format(txn_info.get('confirmed-round', 0)))
        if txn_info.get('confirmed-round', 0) > 0:
            return txn_info
        elif txn_info['pool-error']:
            raise Exception('Pool error and transaction failed to complete: {}'.format(txn_info['pool-error']))
        print('Fetching node status after block #{}'.format(next_round))
        current_status = algod_client.status_after_block(next_round)
        print(json.dumps(current_status, indent=3))
        next_round += 1

    raise Exception('Pending txn not completed within the desired round, timeout round {}'.format(timeout_attempts))
