from models import session
from models import Item, Batch


items = session.query(Item).order_by(Item.code).all()
with open("items.txt", "w") as f:
    for item in items:
        string = f"{item.code}, {item.name}, {item.price}, {item.life_cycle}\n"
        f.write(string)

batches = session.query(Batch).order_by(Batch.item_code).all()
with open("batches.txt", "w") as f:
    for batch in batches:
        string = f"{batch.item_code}, {batch.batch_no}, {batch.quantity}, {batch.price}, {batch.mfg_date}, {batch.exp_date}\n"
        f.write(string)
