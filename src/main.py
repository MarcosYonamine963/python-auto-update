import calculator
import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon, QColor, QTextCharFormat,QTextCursor
import requests


def ask_for_update():
    msg = QMessageBox()
    msg.setWindowTitle("Updater")
    msg.setIcon(QMessageBox.Question)
    msg.setText("Search for new updates?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return msg.exec()

    



if __name__ == "__main__":
    version = "v0.0.2"

    app = QApplication(sys.argv)

    result = ask_for_update()

    if(result == QMessageBox.Yes):
        # print("Yeeeeeesss")
        subprocess.Popen("./updater")
        sys.exit()

    else:
        # print("Nooooooooo")
        pass

    window = calculator.CalculatorApp(version)
    window.show()
    sys.exit(app.exec_())
