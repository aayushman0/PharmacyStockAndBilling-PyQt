from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Float, Date, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
BaseModel = declarative_base()


class Item(BaseModel):
    __tablename__ = "item"

    code = Column("code", String(64), primary_key=True)
    name = Column("name", String(64), index=True)
    price = Column("price", Float)
    life_cycle = Column("life_cycle", Integer)

    def __init__(self, code, name, price, life_cycle):
        self.code = code
        self.name = name
        self.price = price
        self.life_cycle = life_cycle

    def __repr__(self):
        return self.name


class Batch(BaseModel):
    __tablename__ = "batch"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    batch_no = Column("batch_no", String(100), index=True)
    quantity = Column("quantity", Integer)
    price = Column("price", Float)
    mfg_date = Column("mfg_date", Date)
    exp_date = Column("exp_date", Date)
    item_code = Column(String(64), ForeignKey("item.code", ondelete="CASCADE"))
    item = relationship("Item", backref="batches")

    def __init__(self, item_code, batch_no, quantity, price, mfg_date, exp_date):
        self.batch_no = batch_no
        self.quantity = quantity
        self.price = price
        self.mfg_date = mfg_date
        self.exp_date = exp_date
        self.item_code = item_code

    def __repr__(self):
        return f"{self.item.name} Batch: {self.batch_no}"


class Bill(BaseModel):
    __tablename__ = "bill"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    customer_name = Column("name", String(64))
    bill_json = Column("bill_json", String)
    total_amount = Column("total_amount", Float)
    discount = Column("discount", Float)
    net_amount = Column("net_amount", Float)
    payment_type = Column("payment_type", String(64))
    bill_date = Column("bill_date", DateTime)

    def __init__(self, customer_name, bill_json, total_amount, discount, net_amount, payment_type, bill_date):
        self.customer_name = customer_name
        self.bill_json = bill_json
        self.total_amount = total_amount
        self.discount = discount
        self.net_amount = net_amount
        self.payment_type = payment_type
        self.bill_date = bill_date

    def __repr__(self):
        return f"{self.id}. {self.customer_name}"


class ServiceBill(BaseModel):
    __tablename__ = "service_bill"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    patient_name = Column("name", String(64))
    bill_json = Column("bill_json", String)
    total_amount = Column("total_amount", Float)
    discount = Column("discount", Float)
    net_amount = Column("net_amount", Float)
    payment_type = Column("payment_type", String(64))
    bill_date = Column("bill_date", DateTime)

    def __init__(self, patient_name, bill_json, total_amount, discount, net_amount, payment_type, bill_date):
        self.patient_name = patient_name
        self.bill_json = bill_json
        self.total_amount = total_amount
        self.discount = discount
        self.net_amount = net_amount
        self.payment_type = payment_type
        self.bill_date = bill_date

    def __repr__(self):
        return f"{self.id}. {self.patient_name}"


engine = create_engine("sqlite:///mydb.db", echo=False)
BaseModel.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
