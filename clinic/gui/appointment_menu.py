from PyQt6.QtWidgets import QWidget, QVBoxLayout, QWidget, QPushButton, QMessageBox, QInputDialog, QDialog, QPlainTextEdit, QListView
from PyQt6.QtCore import QStringListModel
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class AppointmentMenu(QWidget):
    
    def __init__(self, controller, parent = None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Appointment Menu")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Add buttons for each note-related function
        self.add_note_button = QPushButton("Add Note")
        self.add_note_button.clicked.connect(self.create_note)

        self.retrieve_notes_button = QPushButton("Retrieve Notes")
        self.retrieve_notes_button.clicked.connect(self.retrieve_notes)

        self.update_note_button = QPushButton("Update Note")
        self.update_note_button.clicked.connect(self.update_note)

        self.delete_note_button = QPushButton("Delete Note")
        self.delete_note_button.clicked.connect(self.delete_note)

        self.list_notes_button = QPushButton("List All Notes")
        self.list_notes_button.clicked.connect(self.list_all_notes)

        # Add buttons to the layout
        layout.addWidget(self.add_note_button)
        layout.addWidget(self.retrieve_notes_button)
        layout.addWidget(self.update_note_button)
        layout.addWidget(self.delete_note_button)
        layout.addWidget(self.list_notes_button)

        self.setLayout(layout)

    def create_note(self):
        """Add a note to the current patient's record."""
        try:
            text, ok = QInputDialog.getText(self, "Add Note", "Enter note for patient:")
            if not ok or not text.strip():
                return

            text = text.strip()
            self.controller.create_note(text)
            QMessageBox.information(self, "Success", "Note added to the patient's record.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Access Denied", "You must log in first to add a note.")
        except NoCurrentPatientException:
            QMessageBox.warning(self, "Error", "Cannot add a note without a valid current patient.")

    def retrieve_notes(self):
        """Retrieve notes for the current patient."""
        try:
            search_string, ok = QInputDialog.getText(self, "Retrieve Notes", "Enter text to search in notes:")
            if not ok or not search_string.strip():
                return

            search_string = search_string.strip()
            
            found_notes = self.controller.retrieve_notes(search_string)
            if not found_notes:
                QMessageBox.information(self, "No Results", f"No notes found for: {search_string}")
                return
            
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Notes Found for: {search_string}")
            dialog.resize(600, 400)
            layout = QVBoxLayout(dialog)

            # QPlainTextEdit to display notes
            notes_display = QPlainTextEdit(dialog)
            notes_display.setReadOnly(True)

            # Populate the QPlainTextEdit with note data
            for note in found_notes:
                # Assuming each note has attributes: id, date, and text
                note_text = f"Note ID: {note.code}\nDate: {note.timestamp}\nText: {note.text}\n\n"
                notes_display.appendPlainText(note_text)

            layout.addWidget(notes_display)

            # Show the dialog
            dialog.setLayout(layout)
            dialog.exec()

        except IllegalAccessException:
            QMessageBox.critical(self, "Error", "Please log in to retrieve notes.")
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "Cannot retrieve notes without a valid current patient.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}") 

    def update_note(self):
        """Update a note for the current patient."""
        code, ok = QInputDialog.getText(self, "Update Note", "Enter note code to update:")
        if not ok or not code.strip().isdigit():
            return

        dialog = QInputDialog(self)
        dialog.setWindowTitle("Update Note")
        dialog.setLabelText("Enter new note content:")
        dialog.setInputMode(QInputDialog.InputMode.TextInput)
        dialog.resize(600, 700)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_text = dialog.textValue().strip()
            if new_text:
                try:
                    self.controller.update_note(int(code), new_text)
                    QMessageBox.information(self, "Success", "Note updated successfully.")
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))
            else:
                QMessageBox.warning(self, "Error", "Updated note content cannot be empty.")


    def delete_note(self):
        """Remove a note from the patient's record."""
        if not self.controller.current_patient:
            QMessageBox.critical(self, "Error", "No patient selected to delete notes.")
            return

        try:
            # Prompt the user to enter the note number
            code, ok = QInputDialog.getInt(self, "Delete Note", "Enter Note Number:")
            if not ok:
                return  # User canceled

            # Search for the note with the given code
            note = self.controller.search_note(code)
            if not note:
                QMessageBox.warning(self, "Note Not Found", f"No note found with code #{code}.")
                return

            # Confirm the deletion
            confirm = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete note #{note.code}?\n\n{note.text}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm == QMessageBox.StandardButton.Yes:
                # Call the controller to delete the note
                self.controller.delete_note(code)
                QMessageBox.information(self, "Success", f"Note #{code} has been successfully deleted.")
            else:
                QMessageBox.information(self, "Cancelled", "Note deletion cancelled.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while deleting the note: {str(e)}")

    def list_all_notes(self):
        """Display the full record of the current patient, including all notes."""
        if not self.controller.current_patient:
            QMessageBox.critical(self, "Error", "No patient selected to list the record.")
            return

        try:
            # Get the list of notes for the current patient
            notes = self.controller.list_notes()
            
            if not notes:
                QMessageBox.information(self, "No Notes", "This patient has no notes in their record.")
                return

            # Create a dialog to display the notes
            dialog = QDialog(self)
            dialog.setWindowTitle("Patient Record")
            dialog.setModal(True)
            dialog.resize(600, 400)

            # Create the layout for the dialog
            layout = QVBoxLayout(dialog)

            # Create a QListView to display the notes
            list_view = QListView(dialog)
            list_model = QStringListModel()

            # Prepare the list of note strings to display
            note_strings = [f"Note #{note.code}: {note.text}" for note in notes]
            list_model.setStringList(note_strings)

            list_view.setModel(list_model)

            # Add the list view to the dialog layout
            layout.addWidget(list_view)

            # Show the dialog
            dialog.exec()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while retrieving the patient record: {str(e)}")