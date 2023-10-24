import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMessageBox

class CalculatorApp(QWidget):
    def __init__(self, version):
        super().__init__()
        self.version = version
        self.setWindowTitle(f"Calculadora Básica {self.version}")
        self.setGeometry(100, 100, 300, 400)

        self.layout = QVBoxLayout()

        self.result_display = QLineEdit()
        self.result_display.setFixedHeight(50)
        self.layout.addWidget(self.result_display)

        button_grid = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]

        for row in button_grid:
            button_row = QHBoxLayout()
            for button_text in row:
                button = QPushButton(button_text)
                button.clicked.connect(self.on_button_click)
                if button_text == '=':
                    button.setStyleSheet("background-color: green; font-size: 20px; height: 50px;")
                else:
                    button.setStyleSheet("font-size: 20px; height: 50px;")
                button_row.addWidget(button)
            self.layout.addLayout(button_row)

        clear_button = QPushButton('C')
        clear_button.clicked.connect(self.clear_display)
        clear_button.setStyleSheet("background-color: red; font-size: 20px; height: 50px;")
        self.layout.addWidget(clear_button)

        self.setLayout(self.layout)
        self.current_input = ""

    def on_button_click(self):
        sender = self.sender()
        if sender.text() == '=':
            try:
                result = str(eval(self.current_input))
                self.result_display.setText(result)
                self.current_input = result
            except Exception as e:
                self.result_display.setText("Erro")
                self.current_input = ""
        else:
            self.current_input += sender.text()
            self.result_display.setText(self.current_input)

    def clear_display(self):
        self.current_input = ""
        self.result_display.clear()

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(
    #         self, "Wanna close?", "Are you sure you want to exit?",
    #         QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    #     )

    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()



if __name__ == "__main__":
    
    version = "v0.0.0"
    app = QApplication(sys.argv)
    window = CalculatorApp(version)
    window.show()
    sys.exit(app.exec_())