from dotenv import dotenv_values
from PyQt6.uic import loadUi
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt6.QtGui import QColor

from backend import create_item, create_batch, edit_item, edit_batch
from backend import get_items, get_batches, get_bills, delete_item, delete_batch

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
        self.action_add_bill: QtGui.QAction
        self.action_get_all_items: QtGui.QAction
        self.action_get_batches: QtGui.QAction
        self.action_get_all_bills: QtGui.QAction
        self.action_edit_item: QtGui.QAction
        self.action_edit_batch: QtGui.QAction

        # Stacked Widget and Pages
        self.stacked_widget: QtWidgets.QStackedWidget
        self.page_add_item: QtWidgets.QWidget
        self.page_add_batch: QtWidgets.QWidget
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

        # Add Bill Page

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
            self.reset_page_values(page_name)

        change_screen("page_add_bill")
        self.action_add_item.triggered.connect(lambda: change_screen("page_add_item"))
        self.action_add_batch.triggered.connect(lambda: change_screen("page_add_batch"))
        self.action_add_bill.triggered.connect(lambda: change_screen("page_add_bill"))
        self.action_get_all_items.triggered.connect(lambda: change_screen("page_get_all_items"))
        self.action_get_batches.triggered.connect(lambda: change_screen("page_get_batches"))
        self.action_get_all_bills.triggered.connect(lambda: change_screen("page_get_all_bills"))
        self.action_edit_item.triggered.connect(lambda: change_screen("page_edit_item"))
        self.action_edit_batch.triggered.connect(lambda: change_screen("page_edit_batch"))

    def load_page_logic(self):
        # Load ComboBoxes with Items
        self.input_batch_filter_code.addItem(None, None)
        self.input_item_code.addItem(None, None)
        self.input_edit_code.addItem(None, None)
        self.input_edit_item_code.addItem(None, None)
        for item in self.items_list:
            self.input_batch_filter_code.addItem(item.get("code"), item.get("code"))
            self.input_item_code.addItem(item.get("code"), (item.get("life_cycle"), item.get("price")))
            self.input_edit_code.addItem(item.get("code"), item.get("code"))
            self.input_edit_item_code.addItem(item.get("code"), item.get("code"))

        # Get All Items Page
        for row in self.items_list:
            row_count = self.table_item.rowCount()
            self.table_item.insertRow(row_count)
            for i, column in enumerate(row.values()):
                self.table_item.setItem(row_count, i, QTableWidgetItem(column))
        self.table_item.resizeColumnsToContents()

        # Get Batches Page
        self.button_batch_filter_reset.clicked.connect(self.batch_reset_button_clicked)
        self.input_batch_filter_code.activated.connect(self.batch_filter_code_entered)
        self.input_batch_filter_date.dateChanged.connect(self.batch_filter_date_changed)

        # Get All Bills Page

        # Add Item Page
        self.button_add_item.clicked.connect(self.add_item_button_clicked)

        # Add Batch Page
        self.input_item_code.activated.connect(self.add_batch_code_entered)
        self.input_mfg_date.dateChanged.connect(self.add_batch_mfg_changed)
        self.button_add_batch.clicked.connect(self.add_batch_button_clicked)

        # Add Bill Page

        # Edit Item Page
        self.input_edit_code.activated.connect(self.edit_item_code_entered)
        self.button_edit_item.clicked.connect(self.edit_item_saved)
        self.button_delete_item.clicked.connect(self.edit_item_deleted)

        # Edit Batch Page
        self.input_edit_item_code.activated.connect(self.edit_batch_code_entered)
        self.input_edit_batch_no.activated.connect(self.edit_batch_no_entered)
        self.button_edit_batch.clicked.connect(self.edit_batch_saved)
        self.button_delete_batch.clicked.connect(self.edit_batch_deleted)

    # -------------------Click Events--------------------
    # ---------------------------------------------------
    def batch_reset_button_clicked(self):
        self.input_batch_filter_code.setCurrentIndex(0)
        self.input_batch_filter_date.setDate(QDate.currentDate())
        self.table_batch.setRowCount(0)
        for row in get_batches():
            row_count = self.table_batch.rowCount()
            self.table_batch.insertRow(row_count)
            for i, column in enumerate(["batch_no", "name", "quantity", "price", "mfg_date", "exp_date"]):
                table_item = QTableWidgetItem(row.get(column))
                if row.get("color") is not None:
                    table_item.setBackground(QColor(*row.get("color")))
                self.table_batch.setItem(row_count, i, table_item)
        self.table_batch.resizeColumnsToContents()

    def batch_filter_code_entered(self):
        if not self.input_batch_filter_code.currentData():
            return None
        self.table_batch.setRowCount(0)
        for row in get_batches(item_code=self.input_batch_filter_code.currentData()):
            row_count = self.table_batch.rowCount()
            self.table_batch.insertRow(row_count)
            for i, column in enumerate(["batch_no", "name", "quantity", "price", "mfg_date", "exp_date"]):
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

    def add_item_button_clicked(self):
        name = self.input_item_name.text()
        price = self.input_price.value()
        lifecycle = self.input_lifecycle.value()
        if not (name and price):
            return None  # <----------------------------------------------------------------------------Enter warning msg here
        response = create_item(name, price, lifecycle)
        if type(response) is str:
            return None  # <----------------------------------------------------------------------------Enter warning msg here
        # <---------------------------------------------------------------------------------------------Enter success msg here
        self.update_item_list(response)
        self.reset_page_values("page_add_item")

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
        batch_no = self.input_batch_no.text()
        quantity = self.input_quantity.value()
        price = self.input_batch_price.value()
        if not (code and batch_no and quantity and price):
            return None  # <----------------------------------------------------------------------------Enter warning msg here
        mfg_date = self.input_mfg_date.date().toPyDate()
        exp_date = self.input_exp_date.date().toPyDate()
        response = create_batch(code, batch_no, quantity, price, mfg_date, exp_date)
        if type(response) is str:
            return None  # <----------------------------------------------------------------------------Enter warning msg here
        # <---------------------------------------------------------------------------------------------Enter success msg here
        self.reset_page_values("page_add_batch")

    def edit_item_code_entered(self):
        if not self.input_edit_code.currentText():
            return None
        response = get_items(code=self.input_edit_code.currentText())
        if not response:
            return None
        self.input_edit_item_name.setText(response[0].get("name"))
        self.input_edit_price.setValue(float(response[0].get("price")))
        self.input_edit_lifecycle.setValue(int(response[0].get("life_cycle")))

    def edit_item_saved(self):  # <------------------------------------------------------------------------WIP
        code = self.input_edit_code.currentData()
        if not code:
            return None
        name = self.input_edit_item_name.text()
        price = self.input_edit_price.value()
        lifecycle = self.input_edit_lifecycle.value()
        edit_item(code, name, price, lifecycle)
        self.reset_page_values("page_edit_item")

    def edit_item_deleted(self):  # <----------------------------------------------------------------------WIP
        code = self.input_edit_code.currentData()
        if not code:
            return None
        delete_item(code)
        self.reset_page_values("page_edit_item")

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
            return None  # <----------------------------------------------------------------------------Enter warning msg here
        batch_no = self.input_edit_batch_no.currentText()
        quantity = self.input_edit_quantity.value()
        price = self.input_edit_batch_price.value()
        mfg_date = self.input_edit_mfg_date.date().toPyDate()
        exp_date = self.input_edit_exp_date.date().toPyDate()
        response = edit_batch(code, batch_no, quantity, price, mfg_date, exp_date)
        if type(response) is str:
            return None  # <----------------------------------------------------------------------------Enter warning msg here
        # <---------------------------------------------------------------------------------------------Enter success msg here
        self.reset_page_values("page_edit_batch")

    def edit_batch_deleted(self):
        code = self.input_edit_item_code.currentData()
        if not (code and self.input_edit_batch_no.count()):
            return None  # <----------------------------------------------------------------------------Enter warning msg here
        batch_no = self.input_edit_batch_no.currentText()
        response = delete_batch(code, batch_no)
        if type(response) is str:
            return None  # <----------------------------------------------------------------------------Enter warning msg here
        # <---------------------------------------------------------------------------------------------Enter success msg here
        self.reset_page_values("page_edit_batch")

    # --------------End of Click Events------------------
    # ---------------------------------------------------

    def update_item_list(self, new_item: dict):
        self.items_list.append(new_item)
        row_count = self.table_item.rowCount()
        self.table_item.insertRow(row_count)
        for i, column in enumerate(new_item.values()):
            self.table_item.setItem(row_count, i, QTableWidgetItem(column))
        self.table_item.resizeColumnsToContents()
        self.input_batch_filter_code.addItem(new_item.get("code"), new_item.get("code"))
        self.input_item_code.addItem(new_item.get("code"), (new_item.get("life_cycle"), new_item.get("price")))
        self.input_edit_code.addItem(new_item.get("code"), new_item.get("code"))
        self.input_edit_item_code.addItem(new_item.get("code"), new_item.get("code"))

    def reset_page_values(self, page_name: str):
        self.current_lifecycle = 0
        match page_name:
            case "page_get_all_items":
                pass

            case "page_get_batches":
                self.input_batch_filter_code.setCurrentIndex(0)
                self.input_batch_filter_date.setDate(QDate.currentDate())
                self.batch_reset_button_clicked()

            case "page_get_all_bills":
                self.table_bill.setRowCount(0)
                for row in get_bills():
                    row_count = self.table_bill.rowCount()
                    self.table_bill.insertRow(row_count)
                    self.table_bill.setItem(row_count, 0, QTableWidgetItem(row.get("id")))
                    self.table_bill.setItem(row_count, 1, QTableWidgetItem(row.get("customer_name")))
                    self.table_bill.setItem(row_count, 2, QTableWidgetItem(row.get("bill_date")))
                    self.table_bill.setItem(row_count, 3, QTableWidgetItem(row.get("total_amount")))
                    self.table_bill.setItem(row_count, 4, QTableWidgetItem(row.get("discount")))
                    self.table_bill.setItem(row_count, 5, QTableWidgetItem(row.get("net_amount")))
                self.table_bill.resizeColumnsToContents()

            case "page_add_item":
                self.input_item_name.setText("")
                self.input_price.setValue(0)
                self.input_lifecycle.setValue(0)

            case "page_add_batch":
                self.input_item_code.setCurrentIndex(0)
                self.input_batch_no.setText("")
                self.input_quantity.setValue(0)
                self.input_batch_price.setValue(0)
                self.input_mfg_date.setDate(QDate.currentDate())
                self.input_exp_date.setDate(QDate.currentDate())

            case "page_add_bill":
                pass

            case "page_edit_item":
                self.input_edit_code.setCurrentIndex(0)
                self.input_edit_item_name.setText("")
                self.input_edit_price.setValue(0)
                self.input_edit_lifecycle.setValue(0)

            case "page_edit_batch":
                self.input_edit_item_code.setCurrentIndex(0)
                self.input_edit_batch_no.clear()
                self.input_edit_quantity.setValue(0)
                self.input_edit_batch_price.setValue(0)
                self.input_edit_mfg_date.setDate(QDate.currentDate())
                self.input_edit_exp_date.setDate(QDate.currentDate())

            case _:
                pass
