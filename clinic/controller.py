import hashlib 
from clinic.patient import Patient
from clinic.patient_record import PatientRecord
from clinic.note import Note
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
from clinic.dao.patient_dao_json import PatientDAOJSON
from json import loads, dumps

class Controller():
	''' controller class that receives the system's operations '''

	def __init__(self, autosave=False):
		''' construct a controller class '''

		self.autosave = autosave

		self.username = None
		self.password = None
		self.logged = False

		self.current_patient = None

		if self.autosave:
			self.users = self.load_users()
		else:
			self.users = \
			{"user":"8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", \
			"ali":"6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810", \
			"kala":"e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"}

		self.patient_dao = PatientDAOJSON(self.autosave)


	def load_users(self):
		users = {}
		with open('clinic/users.txt', 'r') as file:
			for line in file:
				tokens = line.strip().split(',')
				users[tokens[0]] = tokens[1]
		return users

	def get_password_hash(self, password):
		encoded_password = password.encode('utf-8')     # Convert the password to bytes
		hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
		hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
		return hex_dig

	def login(self, username, password):
		''' user logs in the system '''
		if self.logged:
			raise DuplicateLoginException("Cannot login more than once in this system.")
			return False
		if self.users.get(username):
			password_hash = self.get_password_hash(password)
			if password_hash == self.users.get(username):
				self.username = username
				self.password = password
				self.logged = True
				return True
			else:
				raise InvalidLoginException("Invalid username or password.")
		else:
			raise InvalidLoginException("Invalid username or password.")

	def logout(self):
		''' user logs out from the system '''
		if not self.logged:
			raise InvalidLogoutException("Cannot logout without logging in first.")			
		else:
			self.username = None
			self.password = None
			self.logged = False
			self.current_patient = None
			return True

	def search_patient(self, phn):
		''' user searches a patient '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		return self.patient_dao.search_patient(phn)

	def create_patient(self, phn, name, birth_date, phone, email, address):
		''' user creates a patient '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		# patient already exists, do not create them
		if self.search_patient(phn):
			raise IllegalOperationException("Illegal Operation: Cannot add a patient with a PHN that is already registered.")

		# finally, create a new patient
		patient = Patient(phn, name, birth_date, phone, email, address, self.autosave)
		return self.patient_dao.create_patient(patient)

	def retrieve_patients(self, name):
		''' user retrieves the patients that satisfy a search criterion '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")
		return self.patient_dao.retrieve_patients(name)

	def update_patient(self, original_phn, phn, name, birth_date, phone, email, address):
		''' user updates a patient '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		patient = self.search_patient(original_phn)

		# patient does not exist, cannot update
		if not patient:
			raise IllegalOperationException("Illegal Operation: Cannot update an inexistent patient.")

		# patient is current patient, cannot update
		if self.current_patient:
			if patient == self.current_patient:
				raise IllegalOperationException("Illegal Operation: Cannot update the current patient, unset patient first.")

		if original_phn != phn:
			if self.search_patient(phn):
				raise IllegalOperationException("Illegal Operation: Cannot update a patient with a new PHN that is already registered.")

		patient = Patient(phn, name, birth_date, phone, email, address)
		return self.patient_dao.update_patient(original_phn, patient)
			
	def delete_patient(self, phn):
		''' user deletes a patient '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		# first, search the patient by key
		patient = self.search_patient(phn)

		# patient does not exist, cannot delete
		if not patient:
			raise IllegalOperationException("Illegal Operation: Cannot delete an inexistent patient.")

		# patient is current patient, cannot delete
		if self.current_patient:
			if patient == self.current_patient:
				raise IllegalOperationException("Illegal Operation: Cannot delete the current patient, unset patient first.")

		return self.patient_dao.delete_patient(phn)

	def list_patients(self):
		''' user lists all patients '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		return self.patient_dao.list_patients()

	def set_current_patient(self, phn):
		''' user sets the current patient '''

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		# first, search the patient by key
		patient = self.search_patient(phn)

		# patient does not exist
		if not patient:
			raise IllegalOperationException("Illegal Operation: Cannot set the current patient to an inexistent patient.")

		# patient exists, set them to be the current patient
		self.current_patient = patient


	def get_current_patient(self):
		''' get the current patient '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		# return current patient
		return self.current_patient

	def unset_current_patient(self):
		''' unset the current patient '''

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		# unset current patient
		self.current_patient = None


	def search_note(self, code):
		''' user searches a note from the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		# there must be a valid current patient
		if not self.current_patient:
			raise NoCurrentPatientException("Cannot handle notes without setting a current patient first.")

		# search a new note with the given code and return it 
		return self.current_patient.search_note(code)

	def create_note(self, text):
		''' user creates a note in the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		# there must be a valid current patient
		if not self.current_patient:
			raise NoCurrentPatientException("Cannot handle notes without setting a current patient first.")

		# create a new note and return it
		return self.current_patient.create_note(text)

	def retrieve_notes(self, search_string):
		''' user retrieves the notes from the current patient's record
			that satisfy a search string '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		# there must be a valid current patient
		if not self.current_patient:
			raise NoCurrentPatientException("Cannot handle notes without setting a current patient first.")

		# return the found notes
		return self.current_patient.retrieve_notes(search_string)

	def update_note(self, code, new_text):
		''' user updates a note from the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		# there must be a valid current patient
		if not self.current_patient:
			raise NoCurrentPatientException("Cannot handle notes without setting a current patient first.")

		# update note
		return self.current_patient.update_note(code, new_text)

	def delete_note(self, code):
		''' user deletes a note from the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		# there must be a valid current patient
		if not self.current_patient:
			raise NoCurrentPatientException("Cannot handle notes without setting a current patient first.")

		# delete note
		return self.current_patient.delete_note(code)

	def list_notes(self):
		''' user lists all notes from the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("Illegal Access: Must login first.")

		# there must be a valid current patient
		if not self.current_patient:
			raise NoCurrentPatientException("Cannot handle notes without setting a current patient first.")

		return self.current_patient.list_notes()

