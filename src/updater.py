import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon, QColor, QTextCharFormat,QTextCursor
import requests

class Updater(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Updater")
        self.setGeometry(100,100,300,250)

    def update(self):

        # Create generic layout
        self.label = QLabel("Updating...")

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(1)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("background-color: grey")
        self.cancel_button.clicked.connect(self.cancel_on_clicked)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

        # verify if need to updtate func must be done at main.py, not here...
        # after verified that need to update, than, update here.
        # this file will be an external executable file, separated from mmain,
        # because the main will be replaced.

        self.appendColoredText("Connecting to server", QColor("black"))

        repo_owner = "MarcosYonamine963"
        repo_name = "python-auto-update"

        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

        request_info_response = requests.get(api_url)

        if request_info_response.status_code == 200:
            
            self.appendColoredText("Searching for updates", QColor("black"))
            
            release_data = request_info_response.json()
            latest_version = release_data["tag_name"]
            install_dir = os.getcwd()

            self.appendColoredText(f"Latest version: {latest_version}", QColor("black"))
            
            self.appendColoredText("Downloading files... this may take a while", QColor("black"))
            
            download_url = release_data["assets"][0]["browser_download_url"]
            download_path = os.path.join(install_dir, "new_version.zip")

            with open(download_path, "wb") as f:
                download_response = requests.get(download_url)
                f.write(download_response.content)

            self.appendColoredText("Downloading complete", QColor("green"))

            self.appendColoredText("Deleting calculator file", QColor("black"))
            self.cancel_button.setEnabled(False) # unable to click
            os.remove(install_dir + "/calculator") # TODO verify this

            self.appendColoredText("Extracting files", QColor("black"))
            subprocess.run(["unzip", download_path, "-d", install_dir])


            self.appendColoredText("Installing", QColor("black"))
            os.remove(install_dir + "/new_version.zip")

            self.appendColoredText("Updating successfull!", QColor("green"))
            self.appendColoredText("Please, restart the program", QColor("black"))

    def appendColoredText(self, text, color):
        cursor = self.text_edit.textCursor()
        format = QTextCharFormat()
        format.setForeground(color)
        cursor.insertText(text, format)
        cursor.insertText("\n")
        format.setForeground(QColor("black"))

    def cancel_on_clicked(self):
        sys.exit()

# Just call this func
def updater_main_func():
    app = QApplication(sys.argv)
    updaterWindow = Updater()
    updaterWindow.show()
    updaterWindow.update()
    sys.exit(app.exec_())



if __name__ == '__main__':
    updater_main_func()
