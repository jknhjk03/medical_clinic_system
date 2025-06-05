import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableView, QPlainTextEdit, QLineEdit, QPushButton, QGridLayout
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.gui.main_dashboard import MainDashboard
from clinic.controller import Controller

class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.controller = Controller(autosave = True)
        # Continue here with your code!
        self.setWindowTitle("Clinic Management System Login")
        self.setGeometry(100, 100, 400, 300)  # Set the size of the window

        frame_geometry = self.frameGeometry()
        
        center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(center)
        self.move(frame_geometry.topLeft())

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        layout = QGridLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter Username")
        layout.addWidget(self.username_input, 0, 1)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input, 1, 1)

        self.login_button = QPushButton("Login", self)
        layout.addWidget(self.login_button, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.login_button.clicked.connect(self.authenticate)

        centralWidget.setLayout(layout)

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            self.controller.login(username, password)
            self.dashboard_window = MainDashboard(self.controller)
            self.dashboard_window.show()
            self.close()
        except InvalidLoginException:
            self.username_input.setText("")
            self.password_input.setText("")
            self.username_input.setPlaceholderText("Invalid credentials, try again.")

def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()