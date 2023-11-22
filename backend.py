import re
import json
from datetime import date, datetime
from dateutil import relativedelta
from models import session
from models import Item, Batch, Bill


def get_all_items() -> list[dict]:
    items = session.query(Item).all()
    response = [{
        "code": item.code,
        "name": item.name,
        "price": str(item.price),
        "life_cycle": str(item.life_cycle)
    } for item in items]
    return response


def get_item_batches(item_code: str) -> list[dict]:
    batches = session.query(Batch).filter(Batch.item_code == item_code)
    return batches


def get_all_bills() -> list[dict]:
    bills = session.query(Bill).order_by(Bill.bill_date.desc()).all()
    response = [{
        "id": str(bill.id),
        "customer_name": bill.customer_name,
        "bill_json": json.loads(bill.bill_json),
        "total_amount": str(bill.total_amount),
        "discount": str(bill.discount),
        "net_amount": str(bill.net_amount),
        "payment_type": bill.payment_type,
        "bill_date": bill.bill_date.strftime("%Y-%m-%d %H:%M:%S")
    } for bill in bills]
    return response


def create_item(name: str, price: float, life_cycle: int | None = None) -> Item | str:
    code = re.sub('[^A-Za-z0-9]+', '', name).lower()

    check_code = session.query(Item).filter(Item.code == code).count()
    if check_code:
        return f"{name} already exists in the database."

    item = Item(code, name, price, life_cycle)
    session.add(Item)
    session.commit()
    return item


def create_batch(item_code: str, batch_no: str, quantity: int, mfg_date: date, exp_date: date) -> Batch:
    batch = session.query(Batch).filter(Batch.batch_no == batch_no, Batch.item_code == item_code).scalar()
    if batch is None:
        batch = Batch(item_code, batch_no, quantity, mfg_date, exp_date)
    else:
        batch.quantity += quantity
        batch.mfg_date = mfg_date
        batch.exp_date = exp_date
    session.add(batch)
    session.commit()
    return batch


def create_bill(customer_name: str, bill_json: list[dict], total_amount: float, bill_date: datetime) -> dict[str, str | list[dict]]:
    bill = Bill(customer_name, json.dumps(bill_json), total_amount, bill_date)
    session.add(bill)

    for batch_dict in bill_json:
        batch_no: str = batch_dict.get("batch_no")
        item_code: str = batch_dict.get("item_code")
        quantity: int = batch_dict.get("quantity")
        if batch_no is None or item_code is None:
            continue

        batch = session.query(Batch).filter(Batch.batch_no == batch_no, Batch.item_code == item_code).scalar()
        if batch is None:
            continue
        if batch.quantity < quantity:
            session.delete(batch)
        else:
            batch.quantity -= quantity
    session.commit()

    response = {
        "id": str(bill.id),
        "customer_name": bill.customer_name,
        "bill_json": json.loads(bill.bill_json),
        "total_amount": str(bill.total_amount),
        "bill_date": bill.bill_date.strftime("%Y-%m-%d %H:%M:%S")
    }
    return response


def edit_item(code: str, name: str, price: float, life_cycle: int) -> Item | str:
    item = session.query(Item).filter(Item.code == code).scalar()
    if item is None:
        return f"{code} doesn't exist."

    item.name = name
    item.price = price
    item.life_cycle = life_cycle
    session.commit()
    return item


def edit_batch(item_code: str, batch_no: str, quantity: int, mfg_date: date, exp_date: date) -> Batch | str:
    batch = session.query(Batch).filter(Batch.batch_no == batch_no, Batch.item_code == item_code).scalar()
    if batch is None:
        return f"{batch_no} doesn't exist."

    if quantity == 0:
        session.delete(batch)
    else:
        batch.quantity = quantity
        batch.mfg_date = mfg_date
        batch.exp_date = exp_date
    session.commit()
    return batch


def delete_item(code: str) -> str | None:
    item = session.query(Item).filter(Item.code == code).scalar()
    if item is None:
        return f"{code} doesn't exist."
    session.delete(item)
    session.commit()


def delete_batch(item_code: str, batch_no: str) -> str | None:
    batch = session.query(Batch).filter(Batch.batch_no == batch_no, Batch.item_code == item_code).scalar()
    if batch is None:
        return f"{batch_no} doesn't exist."
    session.delete(batch)
    session.commit()


def create_item_and_batch(name: str, batch_no: str, quantity: int, price: float, mfg_date: date, exp_date: date) -> tuple[Item, Batch]:
    code = re.sub('[^A-Za-z0-9]+', '', name).lower()
    item = session.query(Item).filter(Item.code == code).scalar()
    if item is None:
        best_before = relativedelta.relativedelta(exp_date, mfg_date)
        item = item(code, name, price, (best_before.months + (best_before.years * 12)))
        session.add(item)
        session.commit()
    batch = create_batch(code, batch_no, quantity, mfg_date, exp_date)
    return item, batch
