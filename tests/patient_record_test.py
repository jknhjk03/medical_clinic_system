from unittest import TestCase
from unittest import main
from clinic.patient_record import PatientRecord
from clinic.note import Note
import datetime

class PatientRecordTest(TestCase):
	def setUp(self):
		self.patient_record = PatientRecord()

	def test_create_note(self):
		# some notes that may be created
		expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
		expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
		expected_note_3 = Note(3, "Patient says high BP is controlled, 120x80 in general.")

		# add one note
		actual_note = self.patient_record.create_note("Patient comes with headache and high blood pressure.")
		self.assertIsNotNone(actual_note, "note 1 was created and is valid")

		# implement __eq__(self, other) in Note to compare notes based on their code and text
		self.assertEqual(expected_note_1, actual_note, "note 1 was created and its data are correct")

		# after creating the note, one should be able to search it
		actual_note = self.patient_record.search_note(1)
		self.assertIsNotNone(actual_note, "note created and retrieved cannot be null")
		self.assertEqual(expected_note_1, actual_note, "note 1 was created, retrieved and its data are correct")

		# add a second note
		actual_note = self.patient_record.create_note("Patient complains of a strong headache on the back of neck.")
		self.assertIsNotNone(actual_note, "note 2 was created and is valid")
		self.assertEqual(expected_note_2, actual_note, "note 2 was created and its data are correct")

		# after creating the note, one should be able to search it
		actual_note = self.patient_record.search_note(2)
		self.assertIsNotNone(actual_note, "note created and retrieved cannot be null")
		self.assertEqual(expected_note_2, actual_note, "note 2 was created, retrieved and its data are correct")

		# add a third note
		actual_note = self.patient_record.create_note("Patient says high BP is controlled, 120x80 in general.")
		self.assertIsNotNone(actual_note, "note 3 was created and is valid")
		self.assertEqual(expected_note_3, actual_note, "note 3 was created and its data are correct")

		# after creating the note, one should be able to search it
		actual_note = self.patient_record.search_note(3)
		self.assertIsNotNone(actual_note, "note created and retrieved cannot be null")
		self.assertEqual(expected_note_3, actual_note, "note 3 was created, retrieved and its data are correct")

		# creating new notes should not affect previous notes
		actual_note = self.patient_record.search_note(2)
		self.assertIsNotNone(actual_note, "note created and retrieved cannot be null regardless of search order")
		self.assertEqual(expected_note_2, actual_note, "note 2 was created, retrieved and its data are correct regardless of search order")
		actual_note = self.patient_record.search_note(1)
		self.assertIsNotNone(actual_note, "note created and retrieved cannot be null regardless of search order")
		self.assertEqual(expected_note_1, actual_note, "note 1 was created, retrieved and its data are correct regardless of search order")


	def test_retrieve_notes(self):
		# some notes that may be retrieved
		expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
		expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
		expected_note_3 = Note(3, "Patient is taking medicines to control blood pressure.")
		expected_note_4 = Note(4, "Patient feels general improvement and no more headaches.")
		expected_note_5 = Note(5, "Patient says high BP is controlled, 120x80 in general.")

		# add somes notes
		actual_note = self.patient_record.create_note("Patient comes with headache and high blood pressure.")
		actual_note = self.patient_record.create_note("Patient complains of a strong headache on the back of neck.")
		actual_note = self.patient_record.create_note("Patient is taking medicines to control blood pressure.")
		actual_note = self.patient_record.create_note("Patient feels general improvement and no more headaches.")
		actual_note = self.patient_record.create_note("Patient says high BP is controlled, 120x80 in general.")

		# retrieve one note
		retrieved_list = self.patient_record.retrieve_notes("neck")
		self.assertEqual(len(retrieved_list), 1, "retrieved list of notes has size 1")
		actual_note = retrieved_list[0]
		self.assertEqual(actual_note, expected_note_2, "retrieved note in the list is note 2")

		# retrieve three notes
		retrieved_list = self.patient_record.retrieve_notes("headache")
		self.assertEqual(len(retrieved_list), 3, "retrieved list of headache notes from Joe Hancock has size 3")
		self.assertEqual(retrieved_list[0], expected_note_1, "first retrieved note in the list is note 1")
		self.assertEqual(retrieved_list[1], expected_note_2, "second retrieved note in the list is note 2")
		self.assertEqual(retrieved_list[2], expected_note_4, "third retrieved note in the list is note 4")

		# retrieve zero notes
		retrieved_list = self.patient_record.retrieve_notes("lungs")
		self.assertEqual(len(retrieved_list), 0)

	def test_update_note(self):
		# some notes that may be updated
		expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
		expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
		expected_note_3 = Note(3, "Patient is taking medicines to control blood pressure.")
		expected_note_4 = Note(4, "Patient feels general improvement and no more headaches.")
		expected_note_5 = Note(5, "Patient says high BP is controlled, 120x80 in general.")

		# try to update a note when there are no notes taken for that patient record in the system
		self.assertFalse(self.patient_record.update_note(3, "Patient is taking Losartan 50mg to control blood pressure."),
			"cannot update note when there are no notes for that patient record in the system")

		# add somes notes
		actual_note = self.patient_record.create_note("Patient comes with headache and high blood pressure.")
		actual_note = self.patient_record.create_note("Patient complains of a strong headache on the back of neck.")
		actual_note = self.patient_record.create_note("Patient is taking medicines to control blood pressure.")
		actual_note = self.patient_record.create_note("Patient feels general improvement and no more headaches.")
		actual_note = self.patient_record.create_note("Patient says high BP is controlled, 120x80 in general.")

		# update one existing note
		self.assertTrue(self.patient_record.update_note(3, "Patient is taking Losartan 50mg to control blood pressure."), 
			"update patient record's note")
		actual_note = self.patient_record.search_note(3)
		self.assertNotEqual(actual_note, expected_note_3, "note has updated data, cannot be equal to the original data")
		expected_note_3a = Note(3, "Patient is taking Losartan 50mg to control blood pressure.")
		self.assertEqual(actual_note, expected_note_3a, "patient was updated, their data has to be updated and correct")
		# notice we have not checked the timestamp. 
		# You should check that manually.
		# some parts of code are not simple to test. How can anyone fix that in general?

		# update another existing note
		self.assertTrue(self.patient_record.update_note(5, "Patient says high BP is controlled, 120x80 every morning."), 
			"update patient record's note")
		actual_note = self.patient_record.search_note(5)
		self.assertNotEqual(actual_note, expected_note_5, "note has updated data, cannot be equal to the original data")
		expected_note_5a = Note(5, "Patient says high BP is controlled, 120x80 every morning.")
		self.assertEqual(actual_note, expected_note_5a, "patient was updated, their data has to be updated and correct")

	def test_delete_note(self):
		# some notes that may be deleted
		expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
		expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
		expected_note_3 = Note(3, "Patient is taking medicines to control blood pressure.")
		expected_note_4 = Note(4, "Patient feels general improvement and no more headaches.")
		expected_note_5 = Note(5, "Patient says high BP is controlled, 120x80 in general.")

		# try to delete a note when there are no notes taken for that patient record in the system
		self.assertFalse(self.patient_record.delete_note(3), "cannot delete note when there are no notes for that patient record in the system")

		# add somes notes
		actual_note = self.patient_record.create_note("Patient comes with headache and high blood pressure.")
		actual_note = self.patient_record.create_note("Patient complains of a strong headache on the back of neck.")
		actual_note = self.patient_record.create_note("Patient is taking medicines to control blood pressure.")
		actual_note = self.patient_record.create_note("Patient feels general improvement and no more headaches.")
		actual_note = self.patient_record.create_note("Patient says high BP is controlled, 120x80 in general.")

		# delete one existing note
		self.assertTrue(self.patient_record.delete_note(3), "delete patient record's note")
		self.assertIsNone(self.patient_record.search_note(3))

		# delete the remaining existing notes regardless of deleting order
		self.assertTrue(self.patient_record.delete_note(1), "delete patient record's note")
		self.assertIsNone(self.patient_record.search_note(1))
		self.assertTrue(self.patient_record.delete_note(5), "delete patient record's note")
		self.assertIsNone(self.patient_record.search_note(5))
		self.assertTrue(self.patient_record.delete_note(4), "delete patient record's note")
		self.assertIsNone(self.patient_record.search_note(4))
		self.assertTrue(self.patient_record.delete_note(2), "delete patient record's note")
		self.assertIsNone(self.patient_record.search_note(2))

	def test_list_notes(self):
		# some notes that may be listed
		expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
		expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
		expected_note_3 = Note(3, "Patient is taking medicines to control blood pressure.")
		expected_note_4 = Note(4, "Patient feels general improvement and no more headaches.")
		expected_note_5 = Note(5, "Patient says high BP is controlled, 120x80 in general.")

		# listing notes when the current patient has no notes
		notes_list = self.patient_record.list_notes()
		self.assertEqual(len(notes_list), 0, "list of notes for patient has size 0")

		# listing notes in a singleton list
		actual_note = self.patient_record.create_note("Patient comes with headache and high blood pressure.")
		notes_list = self.patient_record.list_notes()
		self.assertEqual(len(notes_list), 1, "list of notes for patient has size 1")
		self.assertEqual(notes_list[0], expected_note_1, "Patient comes with headache and high blood pressure.")

		# add some more notes
		actual_note = self.patient_record.create_note("Patient complains of a strong headache on the back of neck.")
		actual_note = self.patient_record.create_note("Patient is taking medicines to control blood pressure.")
		actual_note = self.patient_record.create_note("Patient feels general improvement and no more headaches.")
		actual_note = self.patient_record.create_note("Patient says high BP is controlled, 120x80 in general.")

		# listing notes in a larger list
		notes_list = self.patient_record.list_notes()
		self.assertEqual(len(notes_list), 5, "list of notes has size 5")
		self.assertEqual(notes_list[0], expected_note_5, "note 5 is the first in the list of patients")
		self.assertEqual(notes_list[1], expected_note_4, "note 4 is the second in the list of patients")
		self.assertEqual(notes_list[2], expected_note_3, "note 3 is the third in the list of patients")
		self.assertEqual(notes_list[3], expected_note_2, "note 2 is the fourth in the list of patients")
		self.assertEqual(notes_list[4], expected_note_1, "note 1 is the fifth in the list of patients")

		# deleting some notes
		self.patient_record.delete_note(3)
		self.patient_record.delete_note(1)
		self.patient_record.delete_note(5)

		# listing notes for a patient with deleted notes
		notes_list = self.patient_record.list_notes()
		self.assertEqual(len(notes_list), 2, "list of notes has size 2")
		self.assertEqual(notes_list[0], expected_note_4, "note 4 is the first in the list of notes")
		self.assertEqual(notes_list[1], expected_note_2, "note 2 is the second in the list of notes")


if __name__ == '__main__':
	main()