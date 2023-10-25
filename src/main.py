import calculator
import VerifyNewUpdate
import sys
import os
import subprocess
import json
import time
from PyQt5.QtWidgets import QApplication, QMessageBox


__version__ = "v0.0.3"
latest_version = __version__
repo_owner = "MarcosYonamine963"
repo_name = "python-auto-update"

def ask_for_update(version):
    msg = QMessageBox()
    msg.setWindowTitle("Updater")
    msg.setIcon(QMessageBox.Question)
    msg.setText(f"New version found: {version}. Update?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return msg.exec()


def run_main_app():
    app = QApplication(sys.argv)
    window = calculator.CalculatorApp(__version__)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    latest_version = VerifyNewUpdate.verify_new_update(__version__, repo_owner, repo_name)
    
    if latest_version != __version__ and latest_version != 0:
        result = ask_for_update(latest_version)

        if(result == QMessageBox.Yes):

            # update json file
            json_data = {
                "current_version": f"{__version__}"
            }

            with open('version.json', 'w') as v_file:
                json.dump(json_data, v_file, indent=4)

            # Start updater
            try:
                subprocess.Popen("./updater")
               
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Updater not Found")
                msg.exec()
                run_main_app()
                try:
                    os.remove('version.json')
                except:
                    pass


        else:
            run_main_app()
    
    else:
        run_main_app()