import random
import string




def generate_unique_transaction_id():
    from admin_app.models import Transaction
    while True:
        tx_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))
        if not Transaction.objects.filter(transaction_id=tx_id).exists():
            return tx_id
