# import json
from dotenv import dotenv_values
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtGui import QPainter
from PyQt6.QtPrintSupport import QPrinter

from backend import get_bills

# For Type Hinting
from PyQt6 import QtWidgets


def show_message(title: str, message: str):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec()


class BillWindow(QWidget):
    def __init__(self, bill_id: int):
        super(BillWindow, self).__init__()
        self.bill_id = bill_id
        loadUi("UI/bill.ui", self)
        self.load_pharma_info()
        self.load_bill()

    def type_hinting(self):
        self.pharmacy_name: QtWidgets.QLabel
        self.pharmacy_address: QtWidgets.QLabel
        self.pan_no: QtWidgets.QLabel
        self.dda_no: QtWidgets.QLabel

        self.bill_no: QtWidgets.QLabel
        self.date: QtWidgets.QLabel
        self.customer_name: QtWidgets.QLabel

        self.total: QtWidgets.QLabel
        self.discount: QtWidgets.QLabel
        self.net_total: QtWidgets.QLabel

        self.button_print: QtWidgets.QPushButton

    def load_pharma_info(self):
        env = dotenv_values(".env")
        self.pharmacy_name.setText(env.get("PHARMACY_NAME"))
        self.pharmacy_address.setText(env.get("PHARMACY_ADDRESS"))
        self.pan_no.setText(f'PAN No.: {env.get("PAN_NO")}')
        self.dda_no.setText(f'DDA No.: {env.get("DDA_NO")}')

    def load_bill(self):
        bill = get_bills(id=self.bill_id)
        if bill is None:
            self.customer_name.setText("Name: Bill doesn't exist.")
            return None

        self.bill_no.setText(f"Bill no.: {bill.id}")
        self.date.setText(f"Date: {bill.bill_date.strftime('%Y/%m/%d %H:%M')}")
        self.customer_name.setText(f"Name: {bill.customer_name}")

        self.total.setText(str(bill.total_amount))
        self.discount.setText(str(bill.discount))
        self.net_total.setText(str(bill.net_amount))

        self.button_print.clicked.connect(self.print_to_printer)

    def print_to_printer(self):
        printer = QPrinter()
        painter = QPainter()
        painter.begin(printer)
        screen = self.grab()
        painter.drawPixmap(10, 10, screen)
        painter.end()
