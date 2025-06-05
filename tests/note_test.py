from unittest import TestCase
from unittest import main
from clinic.note import Note
import datetime

class NoteTest(TestCase):
	def setUp(self):
		self.note = Note(1, "Patient shows up with chest pain", datetime.datetime.now())

	def test_eq(self):
		same_note = Note(1, "Patient shows up with chest pain", datetime.datetime.now())
		different_note_1 = Note(2, "Patient shows up with chest pain", datetime.datetime.now())
		different_note_2 = Note(1, "Patient has dizziness", datetime.datetime.now())
		self.assertTrue(self.note == self.note)
		self.assertTrue(self.note == same_note)
		self.assertFalse(self.note == different_note_1)
		self.assertFalse(self.note == different_note_2)

	def test_str(self):
		same_note = Note(1, "Patient shows up with chest pain", datetime.datetime.now())
		different_note_1 = Note(2, "Patient shows up with chest pain", datetime.datetime.now())
		different_note_2 = Note(1, "Patient has dizziness", datetime.datetime.now())
		self.assertEqual("1; " + str(self.note.timestamp) + "; Patient shows up with chest pain", str(self.note))
		self.assertEqual("1; " + str(self.note.timestamp) + "; Patient shows up with chest pain", str(same_note))
		self.assertEqual("2; " + str(self.note.timestamp) + "; Patient shows up with chest pain", str(different_note_1))
		self.assertEqual("1; " + str(self.note.timestamp) + "; Patient has dizziness", str(different_note_2))
		self.assertEqual(str(same_note), str(self.note))
		self.assertNotEqual(str(different_note_1), str(self.note))
		self.assertNotEqual(str(different_note_2), str(self.note))

	def test_repr(self):
		same_note = Note(1, "Patient shows up with chest pain", datetime.datetime.now())
		different_note_1 = Note(2, "Patient shows up with chest pain", datetime.datetime.now())
		different_note_2 = Note(1, "Patient has dizziness", datetime.datetime.now())
		self.assertEqual("Note(1, " + repr(self.note.timestamp) + ", 'Patient shows up with chest pain')", repr(self.note))
		self.assertEqual("Note(1, " + repr(same_note.timestamp) + ", 'Patient shows up with chest pain')", repr(same_note))
		self.assertEqual("Note(2, " + repr(different_note_1.timestamp) + ", 'Patient shows up with chest pain')", repr(different_note_1))
		self.assertEqual("Note(1, " + repr(different_note_2.timestamp) + ", 'Patient has dizziness')", repr(different_note_2))
		self.assertEqual(repr(same_note), repr(self.note))
		self.assertNotEqual(repr(different_note_1), repr(self.note))
		self.assertNotEqual(repr(different_note_2), repr(self.note))

if __name__ == '__main__':
	main()