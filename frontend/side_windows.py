import os
import json
from dotenv import dotenv_values
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from docx import Document

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

        self.table_bill_print: QtWidgets.QTableWidget
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

        self.table_bill_print.setRowCount(0)
        for i, row in enumerate(json.loads(bill.bill_json)):
            self.table_bill_print.insertRow(i)
            self.table_bill_print.setItem(i, 0, QTableWidgetItem(row.get("item_name")))
            self.table_bill_print.setItem(i, 1, QTableWidgetItem(row.get("batch_no")))
            self.table_bill_print.setItem(i, 2, QTableWidgetItem(row.get("exp_date")))
            self.table_bill_print.setItem(i, 3, QTableWidgetItem(str(row.get("quantity"))))
            self.table_bill_print.setItem(i, 4, QTableWidgetItem(str(row.get("price"))))
            self.table_bill_print.setItem(i, 5, QTableWidgetItem(str(row.get("total"))))
        self.table_bill_print.resizeColumnsToContents()

        self.total.setText(str(bill.total_amount))
        self.discount.setText(str(bill.discount))
        self.net_total.setText(str(bill.net_amount))

        self.button_print.clicked.connect(lambda: self.print_to_printer(bill))

    def print_to_printer(self, bill):
        document = Document("bill_sample.docx")

        id_string = f"[{bill.id:04d}]"
        date_string = bill.bill_date.strftime("%d/%m/%Y")
        customer_name = bill.customer_name
        items = ""
        total = f"{bill.total_amount:8.2f}"
        discount = f"{bill.discount:8.2f}"
        net_total = f"{bill.net_amount:8.2f}"
        payment_type = f"[{bill.payment_type}]".rjust(11)

        for i, item in enumerate(json.loads(bill.bill_json)):
            sn = f"{i:02d}  "

            particular = item.get("item_name", "")
            particular_length = len(particular)
            if particular_length < 10:
                particular = f"{particular}\t\t"
            elif particular_length < 16:
                particular = f"{particular}\t"
            else:
                particular = particular[:15] + "\t"

            batch_no = item.get("batch_no", "")
            batch_no_length = len(batch_no)
            if batch_no_length < 7:
                batch_no = f"{batch_no}\t\t"
            elif batch_no_length < 12:
                batch_no = f"{batch_no}\t"
            else:
                batch_no = batch_no[:11] + "\t"

            exp = item.get("exp_date", "MM/YYYY")
            exp = f"{exp[:3]}{exp[5:7]}\t"

            qty = item.get("quantity", 0)
            qty = f"{qty}".ljust(5)

            price = item.get("price", 0)
            price = f"{price:.2f}\t"

            amount = item.get("total", 0)
            amount = f"{amount:.2f}".rjust(9)

            items += f"{sn}{particular}{batch_no}{exp}{qty}{price}{amount}\n"

        replacement_dictionary = {
            "[----]": id_string,
            "DD/MM/YYYY": date_string,
            "[Customer Name]": customer_name,
            "[Bill]": "\n" + items,
            "[TTTTT.00]": total,
            "[DDDDD.00]": discount,
            "[NNNNN.00]": net_total,
            "[PPPPPPPPPPP]": payment_type,
        }

        def replace_string(paragraph, old_string, new_string):
            inline = paragraph.runs
            for i in range(len(inline)):
                if old_string in inline[i].text:
                    text = inline[i].text.replace(str(old_string), str(new_string))
                    inline[i].text = text

        for paragraph in document.paragraphs:
            for old_string, new_string in replacement_dictionary.items():
                if old_string in paragraph.text:
                    replace_string(paragraph, old_string, new_string)

        document.save("bill_output.docx")
        os.startfile("bill_output.docx", "print")
