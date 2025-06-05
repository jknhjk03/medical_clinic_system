import os
from clinic.dao.patient_dao import PatientDAO
from clinic.patient import Patient
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder
from json import loads, dumps

class PatientDAOJSON(PatientDAO):
	''' DAO class that handles patient persistence '''

	def __init__(self, autosave=False):
		''' constructs a DAO for patients '''
		
		self.autosave = autosave

		if self.autosave:
			patients_file_directory = 'clinic'
			self.filename = os.path.join(patients_file_directory, 'patients.json')
			self.patients = {}
			try:
				with open(self.filename, 'r') as file:
					for patient_json in file:
						patient = loads(patient_json, cls=PatientDecoder)
						 
						self.patients[patient.phn] = patient
			except:
				pass
		else:
			self.patients = {}

	def search_patient(self, key):
		''' searches a patient '''

		return self.patients.get(key)

	def create_patient(self, patient):
		''' creates a patient '''

		self.patients[patient.phn] = patient

		# if persistence is set, save all patients
		if self.autosave:
			with open(self.filename, 'w') as file:
				for key in self.patients:
					patient_json = dumps(self.patients[key], cls=PatientEncoder)
					file.write('%s\n' % (patient_json))

		return patient

	def retrieve_patients(self, search_string):
		''' retrieves patients by text '''

		retrieved_patients = []
		for patient in self.patients.values():
			if search_string in patient.name:
				retrieved_patients.append(patient)
		return retrieved_patients

	def update_patient(self, key, patient):
		''' updates a patient '''

		# treat different keys as a separate case
		if key != patient.phn:
			self.patients.pop(key)
		self.patients[patient.phn] = patient

		# if persistence is set, save all patients
		if self.autosave:
			with open(self.filename, 'w') as file:
				for key in self.patients:
					patient_json = dumps(self.patients[key], cls=PatientEncoder)
					file.write('%s\n' % (patient_json))

		return True

	def delete_patient(self, key):
		''' deletes a patient '''

		# patient exists, delete patient
		self.patients.pop(key)

		# if persistence is set, save all patients
		if self.autosave:
			with open(self.filename, 'w') as file:
				for key in self.patients:
					patient_json = dumps(self.patients[key], cls=PatientEncoder)
					file.write('%s\n' % (patient_json))

		return True

	def list_patients(self):
		''' lists all patients '''

		patients_list = []
		for patient in self.patients.values():
			patients_list.append(patient)
		return patients_list
