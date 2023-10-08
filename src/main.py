import calculator
import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon, QColor, QTextCharFormat,QTextCursor
import json


def ask_for_update():
    msg = QMessageBox()
    msg.setWindowTitle("Updater")
    msg.setIcon(QMessageBox.Question)
    msg.setText("Search for new updates?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return msg.exec()

if __name__ == "__main__":
    __version__ = "v0.0.2"

    app = QApplication(sys.argv)

    result = ask_for_update()

    if(result == QMessageBox.Yes):

        # update json file
        json_data = {
            "current_version": f"{__version__}"
        }

        with open('version.json', 'w') as v_file:
            json.dump(json_data, v_file, indent=4)

        # Start updater
        subprocess.Popen("./updater")
        sys.exit()

    else:
        pass

    window = calculator.CalculatorApp(__version__)
    window.show()
    sys.exit(app.exec_())
