import sys
from PyQt6.QtWidgets import QApplication
from frontend.main_window import MainWindow


def window():
    app = QApplication(sys.argv)
    win = MainWindow()

    win.show()
    app.exec()


if __name__ == "__main__":
    window()
