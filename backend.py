import re
import json
from datetime import date, datetime
from dateutil import relativedelta
from models import session
from models import Item, Batch, Bill


def get_items(code: str | None = None) -> list[dict]:
    items = session.query(Item)
    if code is not None:
        items = items.filter(Item.code == code)
    response = [{
        "code": item.code,
        "name": item.name,
        "price": str(item.price),
        "life_cycle": str(item.life_cycle)
    } for item in items]
    return response


def get_batches(item_code: str | None = None, exp_date: date | None = None, obj: bool = False) -> list[dict] | list[Batch]:
    batches = session.query(Batch)
    if item_code is not None:
        batches = batches.filter(Batch.item_code == item_code)
    if exp_date is not None:
        batches = batches.filter(Batch.exp_date <= exp_date.replace(day=1))
    batches = batches.order_by(Batch.exp_date)
    if obj:
        return batches
    response = [{
        "batch_no": batch.batch_no,
        "name": batch.item.name,
        "quantity": str(batch.quantity),
        "price": str(batch.price),
        "mfg_date": batch.mfg_date.strftime("%m/%Y"),
        "exp_date": batch.exp_date.strftime("%m/%Y"),
        "color": (255, 225, 100) if batch.exp_date <= date.today().replace(day=1) else None
    } for batch in batches]
    return response


def get_bills(id: int | None = None) -> Bill | list[dict]:
    if id is not None:
        bill = session.query(Bill).filter(Bill.id == id).scalar()
        return bill

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


def create_item(name: str, price: float, life_cycle: int | None = None) -> dict | str:
    code = re.sub('[^A-Za-z0-9]+', '', name).lower()
    check_code = session.query(Item).filter(Item.code == code).count()
    if check_code:
        return f"{name} already exists in the database."
    item = Item(code, name, price, life_cycle)
    session.add(item)
    session.commit()
    response = {
        "code": item.code,
        "name": item.name,
        "price": str(item.price),
        "life_cycle": str(item.life_cycle)
    }
    return response


def create_batch(item_code: str, batch_no: str, quantity: int, price: float, mfg_date: date, exp_date: date) -> Batch:
    batch = session.query(Batch).filter(Batch.batch_no == batch_no, Batch.item_code == item_code).scalar()
    if batch is None:
        batch = Batch(item_code, batch_no, quantity, price, mfg_date, exp_date)
    else:
        batch.quantity += quantity
        batch.price = price
        batch.mfg_date = mfg_date.replace(day=1)
        batch.exp_date = exp_date.replace(day=1)
    session.add(batch)
    session.commit()
    return batch


def create_bill(customer_name: str, bill_json: list[dict], total_amount: float, discount: float, net_amount: float, payment_type: str, bill_date: datetime) -> Bill:
    bill = Bill(customer_name, json.dumps(bill_json), total_amount, discount, net_amount, payment_type, bill_date)
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
    return bill


def edit_item(code: str, name: str, price: float, life_cycle: int) -> Item | str:
    item = session.query(Item).filter(Item.code == code).scalar()
    if item is None:
        return f"{code} doesn't exist."
    item.name = name
    item.price = price
    item.life_cycle = life_cycle
    session.commit()
    return item


def edit_batch(item_code: str, batch_no: str, quantity: int, price: float, mfg_date: date, exp_date: date) -> Batch | str:
    batch = session.query(Batch).filter(Batch.batch_no == batch_no, Batch.item_code == item_code).scalar()
    if batch is None:
        return f"{batch_no} doesn't exist."
    if quantity == 0:
        session.delete(batch)
    else:
        batch.quantity = quantity
        batch.price = price
        batch.mfg_date = mfg_date.replace(day=1)
        batch.exp_date = exp_date.replace(day=1)
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
        item = Item(code, name, price, (best_before.months + (best_before.years * 12)))
        session.add(item)
        session.commit()
    batch = create_batch(code, batch_no, quantity, price, mfg_date, exp_date)
    return item, batch
