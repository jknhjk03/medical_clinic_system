from clinic.patient_record import PatientRecord

class Patient():
	''' class that represents a patient '''

	def __init__(self, phn, name, birth_date, phone, email, address, autosave=False):
		''' constructs a patient '''
		self.phn = phn
		self.name = name
		self.birth_date = birth_date
		self.phone = phone
		self.email = email
		self.address = address
		self.autosave = autosave

		self.record = PatientRecord(self.phn, self.autosave)

	def get_patient_record(self):
		''' get the patient's record '''
		return self.record

	def __eq__(self, other):
		''' checks whether this patient is the same as other patient '''
		return self.phn == other.phn and self.name == other.name \
		and self.birth_date == other.birth_date and self.phone == other.phone \
		and self.email == other.email and self.address == other.address

	def __str__(self):
		''' converts the patient object to a string representation '''
		return str(self.phn) + "; " + self.name + "; " + self.birth_date + \
		"; " + self.phone + "; " + self.email + "; " + self.address

	def __repr__(self):
		''' converts the patient object to a string representation for debugging '''
		return "Patient(%r, %r, %r, %r, %r, %r)" % (self.phn, self.name, self.birth_date, self.phone, self.email, self.address)

	def search_note(self, code):
		''' delegates note search to the patient's record '''
		return self.record.search_note(code)

	def create_note(self, text):
		''' delegates note creation to the patient's record '''
		return self.record.create_note(text)

	def retrieve_notes(self, search_string):
		''' delegates note retrieval to the patient's record '''
		return self.record.retrieve_notes(search_string)

	def update_note(self, code, new_text):
		''' delegates note updating to the patient's record '''
		return self.record.update_note(code, new_text)

	def delete_note(self, code):
		''' delegates note deletion to the patient's record '''
		return self.record.delete_note(code)

	def list_notes(self):
		''' delegates note listing to the patient's record '''
		return self.record.list_notes()
