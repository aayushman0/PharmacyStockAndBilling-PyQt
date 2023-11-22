from dotenv import dotenv_values
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow

# For Type Hinting
from PyQt6 import QtWidgets, QtGui


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("UI/main.ui", self)

        self.load_top_layout()
        self.load_menubar_logic()

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

    def load_top_layout(self):
        env = dotenv_values(".env")
        self.pharmacy_name.setText(env.get("PHARMACY_NAME"))
        self.pharmacy_address.setText(env.get("PHARMACY_ADDRESS"))
        self.pan_no.setText(f'PAN No.: {env.get("PAN_NO")}')
        self.dda_no.setText(f'DDA No.: {env.get("DDA_NO")}')

    def load_menubar_logic(self):
        def change_screen(page_name):
            self.stacked_widget.setCurrentWidget(getattr(self, page_name))

        change_screen("page_add_bill")
        self.action_add_item.triggered.connect(lambda: change_screen("page_add_item"))
        self.action_add_batch.triggered.connect(lambda: change_screen("page_add_batch"))
        self.action_add_bill.triggered.connect(lambda: change_screen("page_add_bill"))
        self.action_get_all_items.triggered.connect(lambda: change_screen("page_get_all_items"))
        self.action_get_batches.triggered.connect(lambda: change_screen("page_get_batches"))
        self.action_get_all_bills.triggered.connect(lambda: change_screen("page_get_all_bills"))
        self.action_edit_item.triggered.connect(lambda: change_screen("page_edit_item"))
        self.action_edit_batch.triggered.connect(lambda: change_screen("page_edit_batch"))
