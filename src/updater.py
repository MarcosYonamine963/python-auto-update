import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QTextEdit, QMainWindow, QProgressBar
from PyQt5.QtGui import QIcon, QColor, QTextCharFormat,QTextCursor
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import requests
import time
import math


class Updater(QWidget):

    state = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.state.connect(self.on_state_changed)

        self.initUI()

    def initUI(self):

        self.setWindowTitle("Updater")
        self.setGeometry(500,100,600,500)

        # Create generic layout
        self.label = QLabel("Updating...")

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.label_download = QLabel("Download progress")

        self.progress_bar = QProgressBar()
        # self.progress_bar.setVisible(False)

        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("background-color: green")
        self.start_button.clicked.connect(self.start_on_clicked)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("background-color: grey")
        self.cancel_button.clicked.connect(self.cancel_on_clicked)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.label_download)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def cancel_on_clicked(self):
        self.text_edit.append("Update Canceled!")
        self.text_edit.repaint()
        print("Update Canceled")

        for x in range(3):
            self.text_edit.append(f"Leaving in {3 - x}")
            self.text_edit.repaint()
            print(f"Leaving in {x}")
            time.sleep(1)
        sys.exit()


        
    def start_on_clicked(self):
        self.output_message("Starting Updater")
        self.state.emit(1) # init state machine
        
    @pyqtSlot(int)
    def on_state_changed(self, state):
        match state:
            case 0:
                # TODO reenable buttons, reset states
                pass

            case 1: # Start of update

                self.output_message("Connecting to Server")
                
                self.repo_owner = "MarcosYonamine963"
                self.repo_name = "python-auto-update"

                self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"

                self.request_info_response = requests.get(self.api_url)

                if self.request_info_response.status_code == 200:

                    self.output_message("Connection Successful")
                    self.state.emit(2)

                else:
                    self.error("Connection FAIL")
                    
            case 2:

                self.output_message("Searching for Updates")
                
                self.release_data = self.request_info_response.json()
                latest_version = self.release_data["tag_name"]
                self.install_dir = os.getcwd()

                self.output_message(f"Latest version: {latest_version}")
                time.sleep(2)

                self.state.emit(3)

            case 3:

                self.output_message("Downloading files... this may take a while")
                
                download_url = self.release_data["assets"][0]["browser_download_url"]
                self.download_path = os.path.join(self.install_dir, "new_version.zip")
                
                self.output_message(f"Downloading to: {self.download_path}")
                self.output_message("Please, do not close the Updater")

                ## Test this during executable file
                # with open(self.download_path, "wb") as f:
                #     download_response = requests.get(download_url)
                #     f.write(download_response.content)

                response = requests.get(download_url, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024
                progress_bar_length = 50

                ######  This append is a bug fix  #######
                self.text_edit.append("DONT ERASE ME\n")
                #########################################

                with open(self.download_path, 'wb') as file:

                    for data in response.iter_content(block_size):
                        file.write(data)
                        downloaded = len(data)
                        total_downloaded = os.path.getsize(self.download_path)

                        percent = (total_downloaded / total_size) * 100
                        progress = int(progress_bar_length * percent / 100)

                        print(
                            f'Downloading [{chr(9608) * progress}{" " * (progress_bar_length - progress)}] {percent:.2f}%',
                            end='\r'
                        )
                        
                        self.text_cursor = self.text_edit.textCursor()
                        self.text_cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.KeepAnchor)
                        self.text_cursor.removeSelectedText()
                        self.text_edit.append(f'Downloading: {percent:.2f}%')
                        self.text_edit.repaint()

                        self.progress_bar.setValue(int(percent))
                        self.progress_bar.repaint()

                self.progress_bar.setValue(100)
                self.progress_bar.repaint()
                self.output_message("Download Complete")

                self.state.emit(4)

            case 4:

                self.output_message("Deleting main application file")
                self.output_message("Please, do not close the Updater")

                self.cancel_button.setEnabled(False)

                # os.remove(self.install_dir + "/main") # TODO verify this

                # self.appendColoredText("Extracting files", QColor("black"))
                # self.text_edit.append("testeee")
                # print("Extracting files")
                # subprocess.run(["unzip", self.download_path, "-d", self.install_dir])

                # self.appendColoredText("Installing", QColor("black"))
                # self.text_edit.append("testeee")
                # print("Installing")
                # os.remove(self.download_path)

                # self.appendColoredText("Updating successfull!", QColor("green"))
                # print("Updating successfull!")

                # self.appendColoredText("Please, restart the program", QColor("black"))
                # print("Please, restart the program")


    def output_message(self, message):
        self.text_edit.append(f"{message}")
        self.text_edit.repaint()
        print(f"{message}")

    def error(self, error_code):
        self.text_edit.append(f"ERROR: {error_code}")
        self.state.emit(0) # reset state machine



def main():


    app = QApplication(sys.argv)
    updaterWindow = Updater()
    updaterWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

