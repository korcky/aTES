from datetime import datetime, timezone

import db
from message_broker import business_events


if __name__ == '__main__':
    today = datetime.now(tz=timezone.utc).date()
    new_balances = db.calculate_new_balances(today=today)
    db.create_balances(new_balances)
    for balance in new_balances:
        if balance.balance > 0:
            business_events.billing_cycle_closed(
                user_public_id=balance.user_id,
                balance=balance.balance,
            )
