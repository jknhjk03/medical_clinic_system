from clinic.note import Note
from clinic.dao.note_dao_pickle import NoteDAOPickle
from pickle import load, dump

class PatientRecord():
	''' class that represents a patient's medical record '''

	def __init__(self, phn=None, autosave=False):
		''' construct a patient record '''
		self.note_dao = NoteDAOPickle(phn, autosave)

	def search_note(self, code):
		''' search a note in the patient's record '''
		return self.note_dao.search_note(code)

	def create_note(self, text):
		''' create a note in the patient's record '''
		return self.note_dao.create_note(text)

	def retrieve_notes(self, search_string):
		''' retrieve notes in the patient's record that satisfy a search string '''
		return self.note_dao.retrieve_notes(search_string)

	def update_note(self, code, new_text):
		''' update a note from the patient's record '''
		return self.note_dao.update_note(code, new_text)

	def delete_note(self, code):
		''' delete a note from the patient's record '''
		return self.note_dao.delete_note(code)

	def list_notes(self):
		''' list all notes from the patient's record from the 
			more recently added to the least recently added'''
		return self.note_dao.list_notes()
