import os
import datetime
from pickle import load, dump
from clinic.dao.note_dao import NoteDAO
from clinic.note import Note

class NoteDAOPickle(NoteDAO):
	''' DAO class that handles note persistence '''


	def __init__(self, phn=None, autosave=False):
		''' constructs a DAO for notes '''

		self.counter = 0

		self.autosave = autosave
		if self.autosave:
			records_directory = 'clinic/records'
			filename = str(phn) + '.dat'
			self.filename = os.path.join(records_directory, filename)
			try:
				with open(self.filename, 'rb') as file:
					self.notes = load(file)
					self.counter = self.notes[-1].code
			except:
				self.notes = []
		else:
			self.notes = []

	def search_note(self, key):
		''' searches a note in a patient record '''

		for note in self.notes:
			if note.code == key:
				return note
		return None
 
	def create_note(self, text):
		''' creates a note in a patient record '''

		self.counter += 1
		current_time = datetime.datetime.now()
		new_note = Note(self.counter, text, current_time)
		self.notes.append(new_note)

		# if persistence is set, save all notes
		if self.autosave:
			with open(self.filename, 'wb') as file:
				dump(self.notes, file)

		return new_note

	def retrieve_notes(self, search_string):
		''' retrieves notes by text in a patient record '''

		# retrieve existing notes
		retrieved_notes = []
		for note in self.notes:
			if search_string in note.text:
				retrieved_notes.append(note)
		return retrieved_notes
 
	def update_note(self, key, new_text):
		''' updates a note in a patient record '''

		updated_note = None

		# first, search the note by code
		for note in self.notes:
			if note.code == key:
				updated_note = note
				break

		# note does not exist
		if not updated_note:
			return False

		# note exists, update fields
		updated_note.text = new_text
		updated_note.timestamp = datetime.datetime.now()

		# if persistence is set, save all notes
		if self.autosave:
			with open(self.filename, 'wb') as file:
				dump(self.notes, file)

		return True

	def delete_note(self, key):
		''' deletes a note in a patient record '''

		note_to_delete_index = -1

		# first, search the note by code
		for i in range(len(self.notes)):
			if self.notes[i].code == key:
				note_to_delete_index = i
				break

		# note does not exist
		if note_to_delete_index == -1:
			return False

		# note exists, delete note
		self.notes.pop(note_to_delete_index)

		# if persistence is set, save all notes
		if self.autosave:
			with open(self.filename, 'wb') as file:
				dump(self.notes, file)

		return True
 
	def list_notes(self):
		''' lists all notes from a patient record '''

 		# list existing notes
		notes_list = []
		for i in range(-1, -len(self.notes)-1, -1):
			notes_list.append(self.notes[i])
		return notes_list
