from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QSpacerItem, QSizePolicy, QVBoxLayout, QLineEdit, QPlainTextEdit, QDialog, QLabel, QMessageBox, QTableView, QHBoxLayout, QAbstractItemView, QInputDialog
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException

class MainDashboard(QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Main Dashboard")
        self.resize(600, 600)

        # Center the window on the screen
        frame_geometry = self.frameGeometry()
        center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(center)
        self.move(frame_geometry.topLeft())

        # Set up central widget and layout
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout()

        # Add spacer to push the "Logout" button to the bottom
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Add "Logout" button at the bottom
        self.logout_button = QPushButton("Logout", self)
        layout.addWidget(self.logout_button, alignment=Qt.AlignmentFlag.AlignBottom)
        self.logout_button.clicked.connect(self.handle_logout)
        centralWidget.setLayout(layout)

        # Search Section
        search_section = QVBoxLayout()
        search_section.addWidget(QLabel("Search for Patient:"))
        search_layout = QHBoxLayout()

        # Input for PHN
        self.phn_input = QLineEdit(self)
        self.phn_input.setPlaceholderText("Enter PHN")
        search_layout.addWidget(self.phn_input)

        self.search_phn_button = QPushButton("Search by PHN", self)
        self.search_phn_button.clicked.connect(self.open_search_patient_window)
        search_layout.addWidget(self.search_phn_button)

        # Input for name
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Enter Name")
        search_layout.addWidget(self.search_input)

        self.search_name_button = QPushButton("Search by Name", self)
        self.search_name_button.clicked.connect(self.open_retrieve_patients_window)
        search_layout.addWidget(self.search_name_button)

        layout.addLayout(search_layout)

        # Add "Create Patient" button
        self.create_patient_button = QPushButton("Create Patient", self)
        layout.addWidget(self.create_patient_button, alignment=Qt.AlignmentFlag.AlignTop)
        self.create_patient_button.clicked.connect(self.open_create_patient_window)

        # Add a button to list all patients
        self.list_patients_button = QPushButton("List All Patients", self)
        self.list_patients_button.clicked.connect(self.open_list_patients_dialog)
        layout.addWidget(self.list_patients_button)

        # Add a button to choose a patient
        self.choose_patient_button = QPushButton("Choose Patient", self)
        self.choose_patient_button.clicked.connect(self.start_appointment)
        layout.addWidget(self.choose_patient_button)

        # Add a "Manage Notes" button
        self.manage_notes_button = QPushButton("Manage Notes")
        self.manage_notes_button.setEnabled(False)  # Initially disabled
        #self.manage_notes_button.clicked.connect(self.start_appointment)
        if self.start_appointment:
            self.manage_notes_button.setEnabled(True)
        self.manage_notes_button.clicked.connect(self.open_appointment_menu)
        layout.addWidget(self.manage_notes_button)

    def open_appointment_menu(self):
        """Open the Appointment Menu window."""
        from clinic.gui.appointment_menu import AppointmentMenu  # Import the class
        self.appointment_menu = AppointmentMenu(self.controller)
        self.appointment_menu.show()

    def open_create_patient_window(self):
        """Open the 'Create Patient' dialog."""
        self.create_patient_window = self.CreatePatientWindow(self.controller)
        self.create_patient_window.exec()  # Show the dialog modally

    def open_search_patient_window(self):
        """Open the 'Search Patient' dialog with the PHN from the input field."""
        phn = self.phn_input.text().strip()
        if not phn:
            QMessageBox.warning(self, "Input Error", "Please enter a PHN to search.")
            return

        try:
            # Validate PHN as an integer
            phn = int(phn)
            # Open the search patient dialog with the PHN
            self.search_patient_window = self.SearchPatientWindow(self.controller, phn)
            self.search_patient_window.exec()  # Show the dialog modally
        except ValueError:
            QMessageBox.warning(self, "Input Error", "PHN must be a valid number.")

    def open_retrieve_patients_window(self):
        name = self.search_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a correct name to search.")
            return

        """Open the 'Retrieve Patients' dialog."""
        self.retrieve_patients_window = self.RetrievePatientsWindow(self.controller, name)
        self.retrieve_patients_window.show()  # Show the dialog modally

    def handle_logout(self):
        try:
            from clinic.gui.clinic_gui import ClinicGUI
            self.controller.logout()
            self.login_window = ClinicGUI()
            self.login_window.show()
            self.close()
        except InvalidLogoutException: # This should never happen as the only way that the logout button should be accessed is when one is logged in
            print("Invalid Logout Exception")

    def open_list_patients_dialog(self):
        """Open a dialog showing all patients."""
        try:
            # Get the list of patients from the controller
            patients = self.controller.list_patients()

            if not patients:
                QMessageBox.warning(self, "No Patients", "There are no patients registered in the clinic.")
                return

            # Create the dialog
            dialog = QDialog(self)
            dialog.setWindowTitle("List of Patients")
            dialog.setModal(True)
            dialog.resize(600, 400)

            # Create the table view and model
            table_view = QTableView(dialog)
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(['PHN', 'Name', 'Date of Birth', 'Phone Number', 'Email', 'Home Address'])

            # Populate the model with patient data
            for patient in patients:
                phn_item = QStandardItem(str(patient.phn))
                name_item = QStandardItem(patient.name)
                dob_item = QStandardItem(patient.birth_date)
                phone_item = QStandardItem(patient.phone)
                email_item = QStandardItem(patient.email)
                address_item = QStandardItem(patient.address)
                model.appendRow([phn_item, name_item, dob_item, phone_item, email_item, address_item])

            table_view.setModel(model)
            table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

            # Add the table view to the dialog layout
            layout = QVBoxLayout(dialog)
            layout.addWidget(table_view)
            dialog.setLayout(layout)

            # Show the dialog
            dialog.exec()

        except IllegalAccessException:
            self.show_message("Login Required", "Please log in to view the patients.")

    def start_appointment(self):
        """Start an appointment for the selected patient."""
        try:
            #Prompt the user to enter the PHN
            phn, ok = QInputDialog.getText(self, "Choose Patient", "Enter Personal Health Number (PHN):")
            if not ok:
                return  # User pressed cancel or entered nothing

            phn = phn.strip()

            if not phn.isdigit():
                QMessageBox.warning(self, "Invalid Input", "PHN must be a numeric value.")
                return
            
            phn = int(phn)

            # Set the current patient in the controller
            self.controller.set_current_patient(phn)
            current_patient = self.controller.get_current_patient()
            #self.manage_notes_button.setEnabled(True)

            # Show patient data in a dialog
            self.show_patient_data_dialog(current_patient)
            return True

        except IllegalAccessException:
            self.show_message("Login Required", "Please log in to choose a patient.")
        except IllegalOperationException:
            self.show_message("Error", f"No patient is registered with PHN {phn}.")
        except ValueError:
            self.show_message("Invalid Input", "PHN must be a valid number.")

    def show_patient_data_dialog(self, patient):
        """Display the patient's data in a dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Patient Information")
        dialog.setModal(True)

        # Display patient details
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(f"PHN: {patient.phn}"))
        layout.addWidget(QLabel(f"Name: {patient.name}"))
        layout.addWidget(QLabel(f"Date of Birth: {patient.birth_date}"))
        layout.addWidget(QLabel(f"Phone Number: {patient.phone}"))
        layout.addWidget(QLabel(f"Email Address: {patient.email}"))
        layout.addWidget(QLabel(f"Home Address: {patient.address}"))
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec()

    def show_message(self, title, message):
        """Utility to show message boxes."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec()
    
    class SearchPatientWindow(QDialog):                         # Opens a separate window when the user inputs a phn
        def __init__(self, controller, phn=None):
            super().__init__()
            self.controller = controller
            self.phn = phn
            self.setWindowTitle("Patient Profile")
            self.setGeometry(200, 200, 400, 400)

            self.fields = {}
            self.update_patient_button = None
            self.patient_display = None
            self.current_patient = None  # To store the selected patient's data

            # Layout for the form
            layout = QVBoxLayout(self)

            # Displaying the patient with the inputed phn
            self.patient_display = QPlainTextEdit(self)
            self.patient_display.setReadOnly(True)
            layout.addWidget(self.patient_display)

            # Add "Delete Patient" button after the correct phn is inputed
            self.delete_patient_button = QPushButton("Delete Patient")
            self.delete_patient_button.setEnabled(False)
            self.delete_patient_button.clicked.connect(self.delete_patient)
            layout.addWidget(self.delete_patient_button)

            if phn is not None:
                self.handle_search_patient(phn)

        def handle_search_patient(self, phn):
            try:
                patient = self.controller.search_patient(phn)
                self.current_patient = patient
                if patient:
                    self.patient_display.setPlainText(self.format_patient_information(patient))
                    self.delete_patient_button.setEnabled(True)
                    for field in self.fields.values():
                            field.setEnabled(True)
                else:
                    self.patient_display.setPlainText("There is no patient registered with this phn. Please try again.")
            except IllegalAccessException:
                    self.patient_data_display.setPlainText("Must login first.")

        def format_patient_information(self, patient):
            return f"PHN: {patient.phn}\nName: {patient.name}\nDate of Birth: {patient.birth_date}\nPhone Number: {patient.phone}\nEmail Address: {patient.email}\nHome Address: {patient.address}"

        def delete_patient(self):
            """Delete the current patient."""
            if not self.current_patient:
                QMessageBox.warning(self, "Delete Error", "No patient is currently selected for deletion.")
                return

            phn = self.current_patient.phn
            confirm = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete patient {self.current_patient.name} (PHN: {phn})?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )

            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    # Attempt to delete the patient
                    success = self.controller.delete_patient(phn)
                    if success:
                        QMessageBox.information(self, "Success", f"Patient {self.current_patient.name} has been deleted.")
                        self.close()  # Close the window or reset the form
                    else:
                        QMessageBox.critical(self, "Delete Failed", "Failed to delete the patient. Please try again.")
                except IllegalAccessException:
                    QMessageBox.critical(self, "Access Denied", "You must be logged in to delete a patient.")
                except IllegalOperationException:
                    QMessageBox.critical(self, "Operation Not Allowed", "Cannot delete the current patient during an appointment.")
            else:
                QMessageBox.information(self, "Cancelled", "Patient deletion canceled.")


    class CreatePatientWindow(QDialog):
        def __init__(self, controller):
            super().__init__()
            self.controller = controller
            self.setWindowTitle("Add New Patient")
            self.setGeometry(200, 200, 400, 400)

            # Layout for the form
            layout = QVBoxLayout(self)

            # Input fields
            self.phn_input = QLineEdit(self)
            self.phn_input.setPlaceholderText("Personal Health Number (PHN)")
            layout.addWidget(QLabel("PHN:"))
            layout.addWidget(self.phn_input)

            self.name_input = QLineEdit(self)
            self.name_input.setPlaceholderText("Full Name")
            layout.addWidget(QLabel("Name:"))
            layout.addWidget(self.name_input)

            self.birth_date_input = QLineEdit(self)
            self.birth_date_input.setPlaceholderText("Birth Date (YYYY-MM-DD)")
            layout.addWidget(QLabel("Birth Date:"))
            layout.addWidget(self.birth_date_input)

            self.phone_input = QLineEdit(self)
            self.phone_input.setPlaceholderText("Phone Number")
            layout.addWidget(QLabel("Phone:"))
            layout.addWidget(self.phone_input)

            self.email_input = QLineEdit(self)
            self.email_input.setPlaceholderText("Email Address")
            layout.addWidget(QLabel("Email:"))
            layout.addWidget(self.email_input)

            self.address_input = QLineEdit(self)
            self.address_input.setPlaceholderText("Home Address")
            layout.addWidget(QLabel("Address:"))
            layout.addWidget(self.address_input)

            # Submit button
            submit_button = QPushButton("Create Patient", self)
            submit_button.clicked.connect(self.handle_create_patient)
            layout.addWidget(submit_button)

        def handle_create_patient(self):
            try:
                phn = int(self.phn_input.text().strip())
                name = self.name_input.text().strip()
                birth_date = self.birth_date_input.text().strip()
                phone = self.phone_input.text().strip()
                email = self.email_input.text().strip()
                address = self.address_input.text().strip()

                # Call the controller to create the patient
                self.controller.create_patient(phn, name, birth_date, phone, email, address)

                # Show success message and close dialog
                QMessageBox.information(self, "Success", "Patient added successfully!")
                self.accept()  # Close the dialog
            except ValueError:
                QMessageBox.critical(self, "Error", "PHN must be a valid number.")
            except IllegalAccessException:
                QMessageBox.critical(self, "Error", "You must log in first.")
            except IllegalOperationException:
                QMessageBox.critical(self, "Error", f"A patient with PHN {phn} already exists.")


    class RetrievePatientsWindow(QWidget):                  # Opens a separate window when the user inputs a name and the corresponding patients appear
        def __init__(self, controller, name = None):
            super().__init__()
            self.controller = controller
            self.setWindowTitle("Retrieve Patients by Name")
            self.resize(800, 600)

            # Layout setup
            layout = QVBoxLayout()

            # Input field for name search
            layout.addWidget(QLabel("Enter Name:"))
            self.name_input = QLineEdit(self)
            layout.addWidget(self.name_input)

            # Search button
            self.search_button = QPushButton("Search", self)
            self.search_button.clicked.connect(self.retrieve_patients_by_name)
            layout.addWidget(self.search_button)

            # QTableView to display search results
            self.patients_table = QTableView(self)
            layout.addWidget(self.patients_table)

            # Set layout
            self.setLayout(layout)

            if name:
                self.name_input.setText(name)
                self.retrieve_patients_by_name()

        def retrieve_patients_by_name(self):
            """Handle the search button click."""
            search_string = self.name_input.text().strip()
            if not search_string:
                QMessageBox.warning(self, "Input Error", "Please enter a name to search.")
                return

            try:
                found_patients = self.controller.retrieve_patients(search_string)
                if found_patients:
                    # Set up the QTableView with the results
                    self.patients_table.setModel(PatientsTableModel(found_patients))
                else:
                    QMessageBox.information(self, "No Results", f"No patients found with name: {search_string}")
                    self.patients_table.setModel(None)  # Clear the table
            except IllegalAccessException:
                QMessageBox.critical(self, "Access Error", "You must log in first.")


class PatientsTableModel(QAbstractTableModel):                                      # Opens a table when the List all Patients button is pressed
    """Custom table model for displaying patients in QTableView."""
    def __init__(self, patients):
        super().__init__()
        self.patients = patients
        self.headers = ["PHN", "Name", "Date of Birth", "Phone", "Email", "Address"]

    def rowCount(self, parent=None):
        return len(self.patients)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        patient = self.patients[index.row()]
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            # Return the appropriate field for each column
            if column == 0: return patient.phn
            if column == 1: return patient.name
            if column == 2: return patient.birth_date
            if column == 3: return patient.phone
            if column == 4: return patient.email
            if column == 5: return patient.address

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
            if orientation == Qt.Orientation.Vertical:
                return str(section + 1)
        return None