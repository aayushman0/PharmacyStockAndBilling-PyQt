import re
from dotenv import dotenv_values
from datetime import date
from PyQt6.uic import loadUi
from PyQt6.QtCore import QDate, QDateTime, Qt
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit
from PyQt6.QtWidgets import QAbstractSpinBox, QPushButton, QLineEdit
from PyQt6.QtGui import QColor

from backend import create_item, create_batch, create_item_and_batch, create_bill, create_service_bill
from backend import get_item, get_items, get_batches, get_bills, get_service_bills
from backend import edit_item, edit_batch, delete_item, delete_batch
from .side_windows import show_message, BillWindow, ServiceBillWindow

# For Type Hinting
from PyQt6 import QtWidgets, QtGui


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("UI/main.ui", self)

        self.current_lifecycle: int = 0
        self.items_list: list[dict] = get_items()

        self.load_top_layout()
        self.load_menubar_logic()
        self.load_page_logic()

    def type_hinting(self):
        # Top Layout
        self.pharmacy_name: QtWidgets.QLabel
        self.pharmacy_address: QtWidgets.QLabel
        self.pan_no: QtWidgets.QLabel
        self.dda_no: QtWidgets.QLabel

        # Menu Bar
        self.action_add_item: QtGui.QAction
        self.action_add_batch: QtGui.QAction
        self.action_add_item_and_batch: QtGui.QAction
        self.action_add_bill: QtGui.QAction
        self.action_add_service_bill: QtGui.QAction
        self.action_get_all_items: QtGui.QAction
        self.action_get_batches: QtGui.QAction
        self.action_get_all_bills: QtGui.QAction
        self.action_get_all_service_bills: QtGui.QAction
        self.action_edit_item: QtGui.QAction
        self.action_edit_batch: QtGui.QAction

        # Stacked Widget and Pages
        self.stacked_widget: QtWidgets.QStackedWidget
        self.page_add_item: QtWidgets.QWidget
        self.page_add_batch: QtWidgets.QWidget
        self.page_add_item_and_batch: QtWidgets.QWidget
        self.page_add_bill: QtWidgets.QWidget
        self.page_get_all_items: QtWidgets.QWidget
        self.page_get_batches: QtWidgets.QWidget
        self.page_get_all_bills: QtWidgets.QWidget
        self.page_edit_item: QtWidgets.QWidget
        self.page_edit_batch: QtWidgets.QWidget

        # Get All Items Page
        self.table_item: QtWidgets.QTableWidget

        # Get Batches Page
        self.table_batch: QtWidgets.QTableWidget
        self.input_batch_filter_code: QtWidgets.QComboBox
        self.input_batch_filter_date: QtWidgets.QDateEdit
        self.button_batch_filter_reset: QtWidgets.QPushButton

        # Get All Bills Page
        self.table_bill: QtWidgets.QTableWidget
        self.input_list_bills_date: QtWidgets.QDateEdit
        self.input_bill_day_total: QtWidgets.QDoubleSpinBox

        # Get All Service Bills Page
        self.table_service_bill: QtWidgets.QTableWidget
        self.input_list_service_bills_date: QtWidgets.QDateEdit
        self.input_service_bill_day_total: QtWidgets.QDoubleSpinBox

        # Add Item Page
        self.input_item_name: QtWidgets.QLineEdit
        self.input_price: QtWidgets.QDoubleSpinBox
        self.input_lifecycle: QtWidgets.QSpinBox
        self.button_add_item: QtWidgets.QPushButton

        # Add Batch Page
        self.input_item_code: QtWidgets.QComboBox
        self.input_batch_no: QtWidgets.QLineEdit
        self.input_quantity: QtWidgets.QSpinBox
        self.input_batch_price: QtWidgets.QDoubleSpinBox
        self.input_mfg_date: QtWidgets.QDateEdit
        self.input_exp_date: QtWidgets.QDateEdit
        self.button_add_batch: QtWidgets.QPushButton

        # Add Item and Batch
        self.input_both_item_name: QtWidgets.QLineEdit
        self.input_both_batch_no: QtWidgets.QLineEdit
        self.input_both_quantity: QtWidgets.QSpinBox
        self.input_both_price: QtWidgets.QDoubleSpinBox
        self.input_both_mfg_date: QtWidgets.QDateEdit
        self.input_both_exp_date: QtWidgets.QDateEdit
        self.button_add_both: QtWidgets.QPushButton

        # Add Bill Page
        self.input_customer_name: QtWidgets.QLineEdit
        self.input_bill_date: QtWidgets.QDateTimeEdit
        self.table_add_bill: QtWidgets.QTableWidget
        self.button_add_next_item: QtWidgets.QPushButton
        self.input_total_amount: QtWidgets.QDoubleSpinBox
        self.input_discount: QtWidgets.QDoubleSpinBox
        self.input_net_amount: QtWidgets.QDoubleSpinBox
        self.input_payment_type: QtWidgets.QComboBox
        self.button_add_bill: QtWidgets.QPushButton

        # Add Service Bill Page
        self.input_patient_name: QtWidgets.QLineEdit
        self.input_service_bill_date: QtWidgets.QDateTimeEdit
        self.table_add_service_bill: QtWidgets.QTableWidget
        self.button_add_next_service_item: QtWidgets.QPushButton
        self.input_total_service_amount: QtWidgets.QDoubleSpinBox
        self.input_service_discount: QtWidgets.QDoubleSpinBox
        self.input_service_net_amount: QtWidgets.QDoubleSpinBox
        self.input_service_payment_type: QtWidgets.QComboBox
        self.button_add_service_bill: QtWidgets.QPushButton

        # Edit Item Page
        self.input_edit_code: QtWidgets.QComboBox
        self.input_edit_item_name: QtWidgets.QLineEdit
        self.input_edit_price: QtWidgets.QDoubleSpinBox
        self.input_edit_lifecycle: QtWidgets.QSpinBox
        self.button_edit_item: QtWidgets.QPushButton
        self.button_delete_item: QtWidgets.QPushButton

        # Edit Batch Page
        self.input_edit_item_code: QtWidgets.QComboBox
        self.input_edit_batch_no: QtWidgets.QComboBox
        self.input_edit_quantity: QtWidgets.QSpinBox
        self.input_edit_batch_price: QtWidgets.QDoubleSpinBox
        self.input_edit_mfg_date: QtWidgets.QDateEdit
        self.input_edit_exp_date: QtWidgets.QDateEdit
        self.button_edit_batch: QtWidgets.QPushButton
        self.button_delete_batch: QtWidgets.QPushButton

    def load_top_layout(self):
        env = dotenv_values(".env")
        self.pharmacy_name.setText(env.get("PHARMACY_NAME"))
        self.pharmacy_address.setText(env.get("PHARMACY_ADDRESS"))
        self.pan_no.setText(f'PAN No.: {env.get("PAN_NO")}')
        self.dda_no.setText(f'DDA No.: {env.get("DDA_NO")}')

    def load_menubar_logic(self):
        def change_screen(page_name):
            self.stacked_widget.setCurrentWidget(getattr(self, page_name))
            getattr(self, f"reset_{page_name}")()

        change_screen("page_add_bill")
        self.action_add_item.triggered.connect(lambda: change_screen("page_add_item"))
        self.action_add_batch.triggered.connect(lambda: change_screen("page_add_batch"))
        self.action_add_item_and_batch.triggered.connect(lambda: change_screen("page_add_item_and_batch"))
        self.action_add_bill.triggered.connect(lambda: change_screen("page_add_bill"))
        self.action_add_service_bill.triggered.connect(lambda: change_screen("page_add_service_bill"))
        self.action_get_all_items.triggered.connect(lambda: change_screen("page_get_all_items"))
        self.action_get_batches.triggered.connect(lambda: change_screen("page_get_batches"))
        self.action_get_all_bills.triggered.connect(lambda: change_screen("page_get_all_bills"))
        self.action_get_all_service_bills.triggered.connect(lambda: change_screen("page_get_all_service_bills"))
        self.action_edit_item.triggered.connect(lambda: change_screen("page_edit_item"))
        self.action_edit_batch.triggered.connect(lambda: change_screen("page_edit_batch"))

    def load_page_logic(self):
        # Get All Items Page

        # Get Batches Page
        self.button_batch_filter_reset.clicked.connect(self.batch_reset_button_clicked)
        self.input_batch_filter_code.currentTextChanged.connect(self.batch_filter_code_changed)
        self.input_batch_filter_date.dateChanged.connect(self.batch_filter_date_changed)

        # Get All Bills Page
        self.input_list_bills_date.dateChanged.connect(self.list_bill_date_changed)

        # Get All Service Bills Page
        self.input_list_service_bills_date.dateChanged.connect(self.list_service_bill_date_changed)

        # Add Item Page
        self.button_add_item.clicked.connect(self.add_item_button_clicked)

        # Add Batch Page
        self.input_item_code.activated.connect(self.add_batch_code_entered)
        self.input_mfg_date.dateChanged.connect(self.add_batch_mfg_changed)
        self.button_add_batch.clicked.connect(self.add_batch_button_clicked)

        # Add Item and Batch
        self.button_add_both.clicked.connect(self.add_both_button_clicked)

        # Add Bill Page
        self.button_add_next_item.clicked.connect(self.add_next_item_button_clicked)
        self.input_discount.valueChanged.connect(self.net_amount_updated)
        self.button_add_bill.clicked.connect(self.add_bill_button_clicked)

        # Add Service Bill Page
        self.button_add_next_service_item.clicked.connect(self.add_next_service_item_button_clicked)
        self.input_service_discount.valueChanged.connect(self.service_net_amount_updated)
        self.button_add_service_bill.clicked.connect(self.add_service_bill_button_clicked)

        # Edit Item Page
        self.input_edit_code.activated.connect(self.edit_item_code_entered)
        self.button_edit_item.clicked.connect(self.edit_item_saved)
        self.button_delete_item.clicked.connect(self.edit_item_deleted)

        # Edit Batch Page
        self.input_edit_item_code.activated.connect(self.edit_batch_code_entered)
        self.input_edit_batch_no.activated.connect(self.edit_batch_no_entered)
        self.button_edit_batch.clicked.connect(self.edit_batch_saved)
        self.button_delete_batch.clicked.connect(self.edit_batch_deleted)

    # --------------------------------------------Click Event---------------------------------------------
    # ----------------------------------------------------------------------------------------------------
    def batch_reset_button_clicked(self):
        self.input_batch_filter_code.setCurrentIndex(0)
        self.input_batch_filter_date.setDate(QDate.currentDate())
        self.table_batch.setRowCount(0)
        for row in get_batches():
            row_count = self.table_batch.rowCount()
            self.table_batch.insertRow(row_count)
            for i, column in enumerate(["batch_no", "name", "quantity", "price", "total", "mfg_date", "exp_date"]):
                table_item = QTableWidgetItem(row.get(column))
                if row.get("color") is not None:
                    table_item.setBackground(QColor(*row.get("color")))
                self.table_batch.setItem(row_count, i, table_item)
        self.table_batch.resizeColumnsToContents()

    def batch_filter_code_changed(self):
        current_text = self.input_batch_filter_code.currentText()
        if not current_text:
            return None
        current_text = re.sub('[^A-Za-z0-9]+', '', current_text).lower()
        self.table_batch.setRowCount(0)
        for row in get_batches(item_code=current_text):
            row_count = self.table_batch.rowCount()
            self.table_batch.insertRow(row_count)
            for i, column in enumerate(["batch_no", "name", "quantity", "price", "total", "mfg_date", "exp_date"]):
                table_item = QTableWidgetItem(row.get(column))
                if row.get("color") is not None:
                    table_item.setBackground(QColor(*row.get("color")))
                self.table_batch.setItem(row_count, i, table_item)
        self.table_batch.resizeColumnsToContents()

    def batch_filter_date_changed(self):
        self.table_batch.setRowCount(0)
        for row in get_batches(exp_date=self.input_batch_filter_date.date().toPyDate()):
            row_count = self.table_batch.rowCount()
            self.table_batch.insertRow(row_count)
            for i, column in enumerate(["batch_no", "name", "quantity", "price", "mfg_date", "exp_date"]):
                table_item = QTableWidgetItem(row.get(column))
                if row.get("color") is not None:
                    table_item.setBackground(QColor(*row.get("color")))
                self.table_batch.setItem(row_count, i, table_item)
        self.table_batch.resizeColumnsToContents()

    def list_bill_date_changed(self):
        self.table_bill.setRowCount(0)
        day_total: float = 0

        def fill_table_row(row):
            row_count = self.table_bill.rowCount()
            self.table_bill.insertRow(row_count)
            self.table_bill.setItem(row_count, 0, QTableWidgetItem(row.get("id")))
            self.table_bill.setItem(row_count, 1, QTableWidgetItem(row.get("customer_name")))
            self.table_bill.setItem(row_count, 2, QTableWidgetItem(row.get("bill_date")))
            self.table_bill.setItem(row_count, 3, QTableWidgetItem(row.get("total_amount")))
            self.table_bill.setItem(row_count, 4, QTableWidgetItem(row.get("discount")))
            self.table_bill.setItem(row_count, 5, QTableWidgetItem(row.get("net_amount")))
            bill_detail_button = QPushButton()
            bill_detail_button.setText("Bill Detail")
            bill_detail_button.clicked.connect(lambda: self.show_bill_window(row.get("id")))
            self.table_bill.setCellWidget(row_count, 6, bill_detail_button)
            return float(row.get("net_amount"))

        for row in get_bills(date=self.input_list_bills_date.date().toPyDate()):
            day_total += fill_table_row(row)
        self.table_bill.resizeColumnsToContents()
        self.input_bill_day_total.setValue(day_total)

    def list_service_bill_date_changed(self):
        self.table_service_bill.setRowCount(0)
        day_total: float = 0

        def fill_table_row(row):
            row_count = self.table_service_bill.rowCount()
            self.table_service_bill.insertRow(row_count)
            self.table_service_bill.setItem(row_count, 0, QTableWidgetItem(row.get("id")))
            self.table_service_bill.setItem(row_count, 1, QTableWidgetItem(row.get("patient_name")))
            self.table_service_bill.setItem(row_count, 2, QTableWidgetItem(row.get("bill_date")))
            self.table_service_bill.setItem(row_count, 3, QTableWidgetItem(row.get("total_amount")))
            self.table_service_bill.setItem(row_count, 4, QTableWidgetItem(row.get("discount")))
            self.table_service_bill.setItem(row_count, 5, QTableWidgetItem(row.get("net_amount")))
            bill_detail_button = QPushButton()
            bill_detail_button.setText("Bill Detail")
            bill_detail_button.clicked.connect(lambda: self.show_service_bill_window(row.get("id")))
            self.table_service_bill.setCellWidget(row_count, 6, bill_detail_button)
            return float(row.get("total_amount"))

        for row in get_service_bills(date=self.input_list_service_bills_date.date().toPyDate()):
            day_total += fill_table_row(row)
        self.table_service_bill.resizeColumnsToContents()
        self.input_service_bill_day_total.setValue(day_total)

    def add_item_button_clicked(self):
        name = self.input_item_name.text()
        price = self.input_price.value()
        lifecycle = self.input_lifecycle.value()
        if not (name and price):
            show_message(title="Missing Value", message="One or more field is missing a value.")
            return None
        response = create_item(name, price, lifecycle)
        if type(response) is str:
            show_message(title="Error", message=response)
            return None
        self.items_list = get_items()
        self.reset_page_add_item()
        show_message(title="Success", message=f"{response.get('code')} successfully created.")

    def add_batch_code_entered(self):
        if not self.input_item_code.currentData():
            return None
        self.current_lifecycle = int(self.input_item_code.currentData()[0])
        self.input_batch_price.setValue(float(self.input_item_code.currentData()[1]))
        self.add_batch_mfg_changed()

    def add_batch_mfg_changed(self):
        self.input_exp_date.setDate(self.input_mfg_date.date().addMonths(self.current_lifecycle))

    def add_batch_button_clicked(self):
        code = self.input_item_code.currentText()
        if get_item(code=code) is None:
            return None
        batch_no = self.input_batch_no.text()
        quantity = self.input_quantity.value()
        price = self.input_batch_price.value()
        if not (code and batch_no and quantity and price):
            show_message(title="Missing Value", message="One or more field is missing a value.")
            return None
        mfg_date = self.input_mfg_date.date().toPyDate()
        exp_date = self.input_exp_date.date().toPyDate()
        response = create_batch(code, batch_no, quantity, price, mfg_date, exp_date)
        if type(response) is str:
            show_message(title="Error", message=response)
            return None
        self.reset_page_add_batch()
        show_message(title="Success", message=f"{response.batch_no} successfully created.")

    def add_both_button_clicked(self):
        name = self.input_both_item_name.text()
        batch_no = self.input_both_batch_no.text()
        quantity = self.input_both_quantity.value()
        price = self.input_both_price.value()
        if not (name and batch_no and quantity and price):
            show_message(title="Missing Value", message="One or more field is missing a value.")
            return None
        mfg_date = self.input_both_mfg_date.date().toPyDate()
        exp_date = self.input_both_exp_date.date().toPyDate()
        item, batch = create_item_and_batch(name, batch_no, quantity, price, mfg_date, exp_date)
        self.items_list = get_items()
        self.reset_page_add_item_and_batch()
        show_message(title="Success", message=f"{item.name} Batch No.: {batch.batch_no} successfully created.")

    def add_next_item_button_clicked(self):
        cell_particular = QComboBox()
        cell_batch_no = QComboBox()
        cell_mfg_date = QDateEdit()
        cell_exp_date = QDateEdit()
        cell_quantity = QSpinBox()
        cell_price = QDoubleSpinBox()
        cell_single_total = QDoubleSpinBox()

        # -------------------------------------------------------------------------------- #
        cell_particular.setEditable(True)
        # -------------------------------------------------------------------------------- #
        cell_mfg_date.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        cell_mfg_date.setReadOnly(True)
        cell_mfg_date.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # -------------------------------------------------------------------------------- #
        cell_exp_date.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        cell_exp_date.setReadOnly(True)
        cell_exp_date.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # -------------------------------------------------------------------------------- #
        cell_quantity.setMaximum(9999999)
        cell_quantity.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        # -------------------------------------------------------------------------------- #
        cell_price.setMaximum(9999999)
        cell_price.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        cell_price.setReadOnly(True)
        cell_price.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # -------------------------------------------------------------------------------- #
        cell_single_total.setMaximum(999999999)
        cell_single_total.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        cell_single_total.setReadOnly(True)
        cell_single_total.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # -------------------------------------------------------------------------------- #

        row_count = self.table_add_bill.rowCount()
        self.table_add_bill.insertRow(row_count)

        cell_particular.activated.connect(lambda: self.cell_particular_activated(row_count))
        cell_batch_no.activated.connect(lambda: self.cell_batch_no_activated(row_count))
        cell_quantity.valueChanged.connect(lambda: self.cell_quantity_updated(row_count))

        for i, cell in enumerate([cell_particular, cell_batch_no, cell_mfg_date, cell_exp_date, cell_quantity, cell_price, cell_single_total]):
            self.table_add_bill.setCellWidget(row_count, i, cell)
        self.table_add_bill.resizeColumnsToContents()
        self.table_add_bill.cellWidget(row_count, 0).setFocus()

    def cell_particular_activated(self, row_no):
        current_text = self.table_add_bill.cellWidget(row_no, 0).currentText()
        if not current_text:
            return None
        current_text = re.sub('[^A-Za-z0-9 ]+', '', current_text).lower()
        item = get_item(code=current_text.replace(" ", ""))
        self.table_add_bill.cellWidget(row_no, 0).clear()
        if item is not None:
            self.table_add_bill.cellWidget(row_no, 0).addItem(item.name, item.code)
        else:
            current_text = current_text.split()
            for item in get_items(code_list=current_text):
                self.table_add_bill.cellWidget(row_no, 0).addItem(item.get("name"), item.get("code"))

        code = self.table_add_bill.cellWidget(row_no, 0).currentData()
        if not code:
            return None
        self.table_add_bill.cellWidget(row_no, 1).clear()
        for batch in get_batches(item_code=code, obj=True, exact=True):
            if batch.exp_date > date.today().replace(day=1):
                self.table_add_bill.cellWidget(row_no, 1).addItem(batch.batch_no, (batch.mfg_date, batch.exp_date, batch.price))
        self.cell_batch_no_activated(row_no)

    def cell_batch_no_activated(self, row_no):
        data = self.table_add_bill.cellWidget(row_no, 1).currentData()
        if not data:
            return None
        self.table_add_bill.cellWidget(row_no, 2).setDate(data[0])
        self.table_add_bill.cellWidget(row_no, 3).setDate(data[1])
        self.table_add_bill.cellWidget(row_no, 5).setValue(data[2])

    def cell_quantity_updated(self, row_no):
        quantity = self.table_add_bill.cellWidget(row_no, 4).value()
        price = self.table_add_bill.cellWidget(row_no, 5).value()
        self.table_add_bill.cellWidget(row_no, 6).setValue(quantity * price)

        total = 0
        for row_no in range(self.table_add_bill.rowCount()):
            total += self.table_add_bill.cellWidget(row_no, 6).value()
        self.input_total_amount.setValue(total)
        self.net_amount_updated()

    def net_amount_updated(self):
        self.input_net_amount.setValue(self.input_total_amount.value() - self.input_discount.value())

    def add_bill_button_clicked(self):
        customer_name = self.input_customer_name.text()
        bill_date = self.input_bill_date.dateTime().toPyDateTime()
        total_amount = self.input_total_amount.value()
        discount = self.input_discount.value()
        net_amount = self.input_net_amount.value()
        payment_type = self.input_payment_type.currentText()
        bill_json = list()
        for row in range(self.table_add_bill.rowCount()):
            row_json = {
                "item_code": self.table_add_bill.cellWidget(row, 0).currentData(),
                "item_name": self.table_add_bill.cellWidget(row, 0).currentText(),
                "batch_no": self.table_add_bill.cellWidget(row, 1).currentText(),
                "mfg_date": self.table_add_bill.cellWidget(row, 2).date().toString("MM/yyyy"),
                "exp_date": self.table_add_bill.cellWidget(row, 3).date().toString("MM/yyyy"),
                "quantity": self.table_add_bill.cellWidget(row, 4).value(),
                "price": self.table_add_bill.cellWidget(row, 5).value(),
                "total": self.table_add_bill.cellWidget(row, 6).value()
            }
            bill_json.append(row_json)
        bill = create_bill(customer_name, bill_json, total_amount, discount, net_amount, payment_type, bill_date)
        self.reset_page_add_bill()
        self.show_bill_window(bill.id)

    def add_next_service_item_button_clicked(self):
        cell_particular = QLineEdit()
        cell_quantity = QSpinBox()
        cell_price = QDoubleSpinBox()
        cell_single_total = QDoubleSpinBox()

        cell_quantity.setMaximum(9999999)
        cell_quantity.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        cell_price.setMaximum(9999999)
        cell_price.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        cell_single_total.setMaximum(999999999)
        cell_single_total.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        row_count = self.table_add_service_bill.rowCount()
        self.table_add_service_bill.insertRow(row_count)

        cell_quantity.valueChanged.connect(lambda: self.cell_service_qty_or_price_updated(row_count))
        cell_price.valueChanged.connect(lambda: self.cell_service_qty_or_price_updated(row_count))

        for i, cell in enumerate([cell_particular, cell_quantity, cell_price, cell_single_total]):
            self.table_add_service_bill.setCellWidget(row_count, i, cell)
        self.table_add_service_bill.resizeColumnsToContents()
        self.table_add_service_bill.cellWidget(row_count, 0).setFocus()

    def cell_service_qty_or_price_updated(self, row_no):
        quantity = self.table_add_service_bill.cellWidget(row_no, 1).value()
        price = self.table_add_service_bill.cellWidget(row_no, 2).value()
        self.table_add_service_bill.cellWidget(row_no, 3).setValue(quantity * price)

        total = 0
        for row_no in range(self.table_add_service_bill.rowCount()):
            total += self.table_add_service_bill.cellWidget(row_no, 3).value()
        self.input_total_service_amount.setValue(total)
        self.service_net_amount_updated()

    def service_net_amount_updated(self):
        self.input_service_net_amount.setValue(self.input_total_service_amount.value() - self.input_service_discount.value())

    def add_service_bill_button_clicked(self):
        patient_name = self.input_patient_name.text()
        bill_date = self.input_service_bill_date.dateTime().toPyDateTime()
        total_amount = self.input_total_service_amount.value()
        discount = self.input_service_discount.value()
        net_amount = self.input_service_net_amount.value()
        payment_type = self.input_service_payment_type.currentText()
        bill_json = list()
        for row in range(self.table_add_service_bill.rowCount()):
            row_json = {
                "particular": self.table_add_service_bill.cellWidget(row, 0).text(),
                "quantity": self.table_add_service_bill.cellWidget(row, 1).value(),
                "price": self.table_add_service_bill.cellWidget(row, 2).value(),
                "total": self.table_add_service_bill.cellWidget(row, 3).value(),
            }
            bill_json.append(row_json)
        service_bill = create_service_bill(patient_name, bill_json, total_amount, discount, net_amount, payment_type, bill_date)
        self.reset_page_add_service_bill()
        self.show_service_bill_window(service_bill.id)

    def edit_item_code_entered(self):
        if not self.input_edit_code.currentText():
            return None
        response = get_item(code=self.input_edit_code.currentText())
        if not response:
            return None
        self.input_edit_item_name.setText(response.name)
        self.input_edit_price.setValue(float(response.price))
        self.input_edit_lifecycle.setValue(int(response.life_cycle))

    def edit_item_saved(self):
        code = self.input_edit_code.currentData()
        if not code:
            show_message(title="Missing Value", message="'Code' field is missing value.")
            return None
        name = self.input_edit_item_name.text()
        price = self.input_edit_price.value()
        lifecycle = self.input_edit_lifecycle.value()
        response = edit_item(code, name, price, lifecycle)
        if type(response) is str:
            show_message(title="Error", message=response)
            return None
        self.items_list = get_items()
        self.reset_page_edit_item()
        show_message(title="Success", message=f"{response.code} sucessfully updated.")

    def edit_item_deleted(self):
        code = self.input_edit_code.currentData()
        if not code:
            show_message(title="Missing Value", message="'Code' field is missing value.")
            return None
        response = delete_item(code)
        if type(response) is str:
            show_message(title="Error", message=response)
            return None
        self.items_list = get_items()
        self.reset_page_edit_item()
        show_message(title="Success", message="Item sucessfully deleted.")

    def edit_batch_code_entered(self):
        if not self.input_edit_item_code.currentData():
            return None
        self.input_edit_batch_no.clear()
        for batch in get_batches(item_code=self.input_edit_item_code.currentData(), obj=True):
            self.input_edit_batch_no.addItem(batch.batch_no, (batch.quantity, batch.price, batch.mfg_date, batch.exp_date))
        if self.input_edit_batch_no.count() > 0:
            self.edit_batch_no_entered()

    def edit_batch_no_entered(self):
        self.input_edit_quantity.setValue(self.input_edit_batch_no.currentData()[0])
        self.input_edit_batch_price.setValue(self.input_edit_batch_no.currentData()[1])
        self.input_edit_mfg_date.setDate(self.input_edit_batch_no.currentData()[2])
        self.input_edit_exp_date.setDate(self.input_edit_batch_no.currentData()[3])

    def edit_batch_saved(self):
        code = self.input_edit_item_code.currentData()
        if not (code and self.input_edit_batch_no.count()):
            show_message(title="Missing Value", message="One or more field is missing a value.")
            return None
        batch_no = self.input_edit_batch_no.currentText()
        quantity = self.input_edit_quantity.value()
        price = self.input_edit_batch_price.value()
        mfg_date = self.input_edit_mfg_date.date().toPyDate()
        exp_date = self.input_edit_exp_date.date().toPyDate()
        response = edit_batch(code, batch_no, quantity, price, mfg_date, exp_date)
        if type(response) is str:
            show_message(title="Error", message=response)
            return None
        self.reset_page_edit_batch()
        show_message(title="Success", message=f"{response.batch_no} successfully edited.")

    def edit_batch_deleted(self):
        code = self.input_edit_item_code.currentData()
        if not (code and self.input_edit_batch_no.count()):
            show_message(title="Missing Value", message="One or more field is missing a value.")
            return None
        batch_no = self.input_edit_batch_no.currentText()
        response = delete_batch(code, batch_no)
        if type(response) is str:
            show_message(title="Error", message=response)
            return None
        self.reset_page_edit_batch()
        show_message(title="Success", message="Batch successfully deleted.")

    def show_bill_window(self, bill_id: int):
        self.bill_window = BillWindow(bill_id)
        self.bill_window.show()

    def show_service_bill_window(self, service_bill_id: int):
        self.service_bill_window = ServiceBillWindow(service_bill_id)
        self.service_bill_window.show()

    # ------------------------------------------Reset Page Logic------------------------------------------
    # ----------------------------------------------------------------------------------------------------
    def reset_input_code_and_bill_table(self):
        self.current_lifecycle = 0
        self.input_item_code.clear()
        self.input_edit_code.clear()
        self.input_edit_item_code.clear()
        self.input_batch_filter_code.clear()
        self.table_add_bill.setRowCount(0)
        self.table_add_service_bill.setRowCount(0)

    def reset_page_get_all_items(self):
        self.reset_input_code_and_bill_table()
        self.table_item.setRowCount(0)
        for row in self.items_list:
            row_count = self.table_item.rowCount()
            self.table_item.insertRow(row_count)
            for i, column in enumerate(row.values()):
                self.table_item.setItem(row_count, i, QTableWidgetItem(column))
        self.table_item.resizeColumnsToContents()

    def reset_page_get_batches(self):
        self.reset_input_code_and_bill_table()
        self.input_batch_filter_code.addItem(None, None)
        self.input_batch_filter_date.setDate(QDate.currentDate())
        self.batch_reset_button_clicked()

    def reset_page_get_all_bills(self):
        self.reset_input_code_and_bill_table()
        self.input_list_bills_date.setDate(QDate.currentDate())
        self.input_bill_day_total.setValue(0)
        self.table_bill.setRowCount(0)

        def fill_table_row(row):
            row_count = self.table_bill.rowCount()
            self.table_bill.insertRow(row_count)
            self.table_bill.setItem(row_count, 0, QTableWidgetItem(row.get("id")))
            self.table_bill.setItem(row_count, 1, QTableWidgetItem(row.get("customer_name")))
            self.table_bill.setItem(row_count, 2, QTableWidgetItem(row.get("bill_date")))
            self.table_bill.setItem(row_count, 3, QTableWidgetItem(row.get("total_amount")))
            self.table_bill.setItem(row_count, 4, QTableWidgetItem(row.get("discount")))
            self.table_bill.setItem(row_count, 5, QTableWidgetItem(row.get("net_amount")))
            bill_detail_button = QPushButton()
            bill_detail_button.setText("Bill Detail")
            bill_detail_button.clicked.connect(lambda: self.show_bill_window(row.get("id")))
            self.table_bill.setCellWidget(row_count, 6, bill_detail_button)

        for row in get_bills():
            fill_table_row(row)
        self.table_bill.resizeColumnsToContents()

    def reset_page_get_all_service_bills(self):
        self.reset_input_code_and_bill_table()
        self.input_list_service_bills_date.setDate(QDate.currentDate())
        self.input_service_bill_day_total.setValue(0)
        self.table_service_bill.setRowCount(0)

        def fill_table_row(row):
            row_count = self.table_service_bill.rowCount()
            self.table_service_bill.insertRow(row_count)
            self.table_service_bill.setItem(row_count, 0, QTableWidgetItem(row.get("id")))
            self.table_service_bill.setItem(row_count, 1, QTableWidgetItem(row.get("patient_name")))
            self.table_service_bill.setItem(row_count, 2, QTableWidgetItem(row.get("bill_date")))
            self.table_service_bill.setItem(row_count, 3, QTableWidgetItem(row.get("total_amount")))
            self.table_service_bill.setItem(row_count, 4, QTableWidgetItem(row.get("discount")))
            self.table_service_bill.setItem(row_count, 5, QTableWidgetItem(row.get("net_amount")))
            bill_detail_button = QPushButton()
            bill_detail_button.setText("Bill Detail")
            bill_detail_button.clicked.connect(lambda: self.show_service_bill_window(row.get("id")))
            self.table_service_bill.setCellWidget(row_count, 6, bill_detail_button)

        for row in get_service_bills():
            fill_table_row(row)
        self.table_service_bill.resizeColumnsToContents()

    def reset_page_add_item(self):
        self.reset_input_code_and_bill_table()
        self.input_item_name.setText("")
        self.input_price.setValue(0)
        self.input_lifecycle.setValue(0)

    def reset_page_add_batch(self):
        self.reset_input_code_and_bill_table()
        self.input_item_code.addItem(None, None)
        for item in self.items_list:
            self.input_item_code.addItem(item.get("code"), (item.get("life_cycle"), item.get("price")))
        self.input_batch_no.setText("")
        self.input_quantity.setValue(0)
        self.input_batch_price.setValue(0)
        self.input_mfg_date.setDate(QDate.currentDate())
        self.input_exp_date.setDate(QDate.currentDate())

    def reset_page_add_item_and_batch(self):
        self.reset_input_code_and_bill_table()
        self.input_both_item_name.setText("")
        self.input_both_batch_no.setText("")
        self.input_both_price.setValue(0)
        self.input_both_quantity.setValue(0)
        self.input_both_mfg_date.setDate(QDate.currentDate())
        self.input_both_exp_date.setDate(QDate.currentDate())

    def reset_page_add_bill(self):
        self.reset_input_code_and_bill_table()
        self.input_customer_name.setText("")
        self.input_bill_date.setDateTime(QDateTime.currentDateTime())
        self.input_total_amount.setValue(0)
        self.input_discount.setValue(0)
        self.input_net_amount.setValue(0)
        self.input_payment_type.setCurrentIndex(0)

    def reset_page_add_service_bill(self):
        self.reset_input_code_and_bill_table()
        self.input_patient_name.setText("")
        self.input_service_bill_date.setDateTime(QDateTime.currentDateTime())
        self.input_total_service_amount.setValue(0)
        self.input_service_discount.setValue(0)
        self.input_service_net_amount.setValue(0)
        self.input_service_payment_type.setCurrentIndex(0)
        self.table_add_service_bill.resizeColumnsToContents()

    def reset_page_edit_item(self):
        self.reset_input_code_and_bill_table()
        self.input_edit_code.addItem(None, None)
        for item in self.items_list:
            self.input_edit_code.addItem(item.get("code"), item.get("code"))
        self.input_edit_item_name.setText("")
        self.input_edit_price.setValue(0)
        self.input_edit_lifecycle.setValue(0)

    def reset_page_edit_batch(self):
        self.reset_input_code_and_bill_table()
        self.input_edit_item_code.addItem(None, None)
        for item in self.items_list:
            self.input_edit_item_code.addItem(item.get("code"), item.get("code"))
        self.input_edit_batch_no.clear()
        self.input_edit_quantity.setValue(0)
        self.input_edit_batch_price.setValue(0)
        self.input_edit_mfg_date.setDate(QDate.currentDate())
        self.input_edit_exp_date.setDate(QDate.currentDate())
