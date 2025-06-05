import os
from unittest import TestCase
from unittest import main
from clinic.controller import Controller
from clinic.patient import Patient
from clinic.patient_record import PatientRecord
from clinic.note import Note
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class IntegrationTest(TestCase):

	def setUp(self):
		# set autosave to False to avoid testing persistence
		# self.controller = Controller(autosave=False)

		# set autosave to True to test persistence
		self.controller = Controller(autosave=True)

	# comment the tearDown method to see the file when the test ends.
	def tearDown(self):
		patients_file = 'clinic/patients.json'
		patients_file_exists = os.path.exists(patients_file)
		records_path = 'clinic/records'
		if os.path.exists(records_path):
			filenames = os.listdir(records_path)
			for filename in filenames:
				record_file_path = os.path.join(records_path, filename)
				if os.path.isfile(record_file_path):
					os.remove(record_file_path)
		# removing the patients file later to avoid concurrency issues
		if patients_file_exists:
			os.remove(patients_file)

	def reset_persistence(self):
		# reset persistence will be ignored if autosave is False
		# otherwise it will reinstantiate the controller and reload every file
		if self.controller.autosave:
			self.controller = Controller(autosave=True)
			self.controller.login("user", "123456")       

	def test_login_logout(self):

		with self.assertRaises(InvalidLogoutException, msg="log out only after being logged in"):
			self.controller.logout()

		with self.assertRaises(InvalidLoginException, msg="login in with incorrect username"):
			self.controller.login("incorrectuser", "123456")

		with self.assertRaises(InvalidLoginException, msg="login in with incorrect password"):
			self.controller.login("user", "abadpassword")

		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		with self.assertRaises(DuplicateLoginException, msg="cannot login again while still logged in"):
			self.controller.login("user", "123456")


		self.assertTrue(self.controller.logout(), "log out correctly")

		self.assertTrue(self.controller.login("user", "123456"), "can login again")

		self.assertTrue(self.controller.logout(), "can log out again")

		self.assertTrue(self.controller.login("ali", "@G00dPassw0rd"), "another user logging in")

		self.assertTrue(self.controller.logout(), "can log out again")


	def test_create_search_patient(self):
		# some patients that will be created
		expected_patient_1 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		expected_patient_2 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		expected_patient_3 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# cannot do create and search operations without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot search patient without logging in"):
			self.controller.search_patient(9790012000)
		with self.assertRaises(IllegalAccessException, msg="cannot create patient without logging in"):
			self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")

		# add one patient
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")
		actual_patient = self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		self.assertIsNotNone(actual_patient, "patient created cannot be null")

		# implement __eq__(self, other) in Patient to compare patients based on their attributes
		self.assertEqual(actual_patient, expected_patient_1, "patient John Doe was created and their data are correct")

		# after creating a patient, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		# after creating the patient, one should be able to search them
		actual_patient = self.controller.search_patient(9790012000)
		self.assertIsNotNone(actual_patient, "patient created and retrieved cannot be null")
		self.assertEqual(actual_patient, expected_patient_1, "patient John Doe was created, retrieved and their data are correct")


		# should not allow to create another patient with same phn
		with self.assertRaises(IllegalOperationException, msg="cannot add a patient with a phn that is already registered"):
			self.controller.create_patient(9790012000, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")

		# add a second patient
		actual_patient = self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		self.assertIsNotNone(actual_patient, "second patient created cannot be null")
		self.assertEqual(actual_patient, expected_patient_2, "second patient, Mary Doe, was created and their data are correct")

		# after creating a patient, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		actual_patient = self.controller.search_patient(9790014444)
		self.assertIsNotNone(actual_patient, "patient created and retrieved cannot be null")
		self.assertEqual(actual_patient, expected_patient_2, "second patient, Mary Doe, was created, retrieved and their data are correct")

		# add a third patient
		actual_patient = self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")
		self.assertIsNotNone(actual_patient, "patient created cannot be null")
		self.assertEqual(actual_patient, expected_patient_3, "patient Joe Hancock was created and their data are correct")

		# after creating a patient, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		actual_patient = self.controller.search_patient(9792225555)
		self.assertIsNotNone(actual_patient, "patient created and retrieved cannot be null")
		self.assertEqual(actual_patient, expected_patient_3, "third patient, Joe Hancock, was created, retrieved and their data are correct")

		# creating new patients should not affect previous patients
		actual_patient = self.controller.search_patient(9790014444)
		self.assertIsNotNone(actual_patient, "patient created and retrieved cannot be null regardless of search order")
		self.assertEqual(actual_patient, expected_patient_2, "patient Mary Doe was created, retrieved and their data are correct regardless of search order")
		actual_patient = self.controller.search_patient(9790012000)
		self.assertIsNotNone(actual_patient, "patient created and retrieved cannot be null regardless of search order")
		self.assertEqual(actual_patient, expected_patient_1, "patient John Doe was created, retrieved and their data are correct regardless of search order")

	def test_retrieve_patients(self):
		# some patients that will be retrieved
		expected_patient_1 = Patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
		expected_patient_2 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
		expected_patient_3 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		expected_patient_4 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		expected_patient_5 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot retrieve patients without logging in"):
			self.controller.retrieve_patients("John Doe")

		# login and create some patients
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")
		self.controller.create_patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
		self.controller.create_patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
		self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# retrieve one patient
		retrieved_list = self.controller.retrieve_patients("Mary Doe")
		self.assertEqual(len(retrieved_list), 1, "retrieved list of patients has size 1")
		actual_patient = retrieved_list[0]
		self.assertEqual(actual_patient, expected_patient_4, "retrieved patient in the list is Mary Doe")

		# retrieve two patients
		retrieved_list = self.controller.retrieve_patients("Doe")
		self.assertEqual(len(retrieved_list), 2, "retrieved list of patients with Doe surname has size 2")
		self.assertEqual(retrieved_list[0], expected_patient_3, "first patient in the retrieved list is John Doe")
		self.assertEqual(retrieved_list[1], expected_patient_4, "second patient in the retrieved list is Mary Doe")

		# retrieve zero patients
		retrieved_list = self.controller.retrieve_patients("Smith")
		self.assertEqual(len(retrieved_list), 0)

	def test_update_patient(self):
		# some patients that may be updated
		expected_patient_1 = Patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
		expected_patient_2 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
		expected_patient_3 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		expected_patient_4 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		expected_patient_5 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot update patient without logging in"):
			self.controller.update_patient(9790012000, 9790012000, "John Doe", "2000-10-10", "278 999 4041", "john.doe@hotmail.com", "205 Foul Bay Rd, Oak Bay")

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# create some patients
		self.controller.create_patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
		self.controller.create_patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
		self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# after creating patients, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		# try to update a patient with a phn that is not registered in the system
		with self.assertRaises(IllegalOperationException, msg="cannot update patient with a phn that is not registered"):
			self.controller.update_patient(9790017777, 9798887777, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")

		# update one patient, but keep the Patient key (personal health number) unchanged
		self.assertTrue(self.controller.update_patient(9790012000, 9790012000, "John Doe", "2000-10-10", "278 999 4041", "john.doe@hotmail.com", "205 Foul Bay Rd, Oak Bay"), 
			"update patient data and keep the PHN unchanged")

		# after updating a patient, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		actual_patient = self.controller.search_patient(9790012000)
		self.assertNotEqual(actual_patient, expected_patient_3, "patient has updated data, cannot be equal to the original data")
		expected_patient_3a = Patient(9790012000, "John Doe", "2000-10-10", "278 999 4041", "john.doe@hotmail.com", "205 Foul Bay Rd, Oak Bay")
		self.assertEqual(actual_patient, expected_patient_3a, "patient was updated, their data has to be updated and correct")

		# update one patient, and change the Patient key (personal health number) as well
		self.assertTrue(self.controller.update_patient(9792225555, 9793334444, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@gmail.com", "200 Quadra St, Victoria"), 
			"update patient data and also change the PHN")

		# after updating a patient, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		actual_patient = self.controller.search_patient(9793334444)
		self.assertNotEqual(actual_patient, expected_patient_5, "patient has updated data, cannot be equal to the original data")
		expected_patient_5a = Patient(9793334444, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@gmail.com", "200 Quadra St, Victoria")
		self.assertEqual(actual_patient, expected_patient_5a, "patient was updated, their data has to be updated and correct")

		# update one patient with a conflicting existing personal health number
		with self.assertRaises(IllegalOperationException, msg="cannot update patient and give them a registered phn"):
			self.controller.update_patient(9790014444, 9798884444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")



	def test_delete_patient(self):
		# some patients that may be deleted
		expected_patient_1 = Patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
		expected_patient_2 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
		expected_patient_3 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		expected_patient_4 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		expected_patient_5 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot delete patient without logging in"):
			self.controller.delete_patient(9798884444)

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# add some patients
		self.controller.create_patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
		self.controller.create_patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
		self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# after creating patients, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		# try to delete a patient with a phn that is not registered in the system
		with self.assertRaises(IllegalOperationException, msg="cannot delete patient with a phn that is not registered"):
			self.controller.delete_patient(9790017777)

		# delete one patient at the start of the collection
		self.assertTrue(self.controller.delete_patient(9798884444), "delete patient from the start of the collection")

		# after deleting a patient, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		self.assertIsNone(self.controller.search_patient(9798884444), "deleted patient cannot be found in the system")

		# delete one patient at the middle of the collection
		self.assertTrue(self.controller.delete_patient(9790012000), "delete patient from the middle of the collection")

		# after deleting a patient, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		self.assertIsNone(self.controller.search_patient(9790012000), "deleted patient cannot be found in the system")

		# delete one patient at the end of the collection
		self.assertTrue(self.controller.delete_patient(9792225555), "delete patient from the end of the collection")

		# after deleting a patient, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		self.assertIsNone(self.controller.search_patient(9792225555), "deleted patient cannot be found in the system")


	def test_list_patients(self):
		# some patients that may be listed
		expected_patient_1 = Patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
		expected_patient_2 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
		expected_patient_3 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		expected_patient_4 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		expected_patient_5 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot list patients without logging in"):
			self.controller.list_patients()

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# listing patients when there are no patients in the system
		patients_list = self.controller.list_patients()
		self.assertEqual(len(patients_list), 0, "list of patients has size 0")

		# add one patient
		self.controller.create_patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")

		# listing patients in a singleton list
		patients_list = self.controller.list_patients()
		self.assertEqual(len(patients_list), 1, "list of patients has size 1")
		self.assertEqual(patients_list[0], expected_patient_1, "patient Ali Mesbah is the only one in the list of patients")

		# add some more patients
		self.controller.create_patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
		self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# after creating patients, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		# listing patients in a larger list
		patients_list = self.controller.list_patients()
		self.assertEqual(len(patients_list), 5, "list of patients has size 5")
		self.assertEqual(patients_list[0], expected_patient_1, "patient 1 is the first in the list of patients")
		self.assertEqual(patients_list[1], expected_patient_2, "patient 2 is the second in the list of patients")
		self.assertEqual(patients_list[2], expected_patient_3, "patient 3 is the third in the list of patients")
		self.assertEqual(patients_list[3], expected_patient_4, "patient 4 is the fourth in the list of patients")
		self.assertEqual(patients_list[4], expected_patient_5, "patient 5 is the fifth in the list of patients")

		# deleting some patients
		self.controller.delete_patient(9790012000)
		self.controller.delete_patient(9798884444)
		self.controller.delete_patient(9792225555)

		# after deleting patients, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		# listing patients after deleting some patients
		patients_list = self.controller.list_patients()
		self.assertEqual(len(patients_list), 2, "list of patients has size 2")
		self.assertEqual(patients_list[0], expected_patient_2, "patient 2 is the first in the list of patients")
		self.assertEqual(patients_list[1], expected_patient_4, "patient 4 is the second in the list of patients")

	def test_set_get_current_patient(self):
		# one of these patients will be set as the current patient
		expected_patient_1 = Patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
		expected_patient_2 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
		expected_patient_3 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		expected_patient_4 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		expected_patient_5 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# cannot do operations without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot get current patient without logging in"):
			self.controller.get_current_patient()
		with self.assertRaises(IllegalAccessException, msg="cannot set current patient without logging in"):
			self.controller.set_current_patient(9790010001)
		with self.assertRaises(IllegalAccessException, msg="cannot unset current patient without logging in"):
			self.controller.unset_current_patient()

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# add some patients
		self.controller.create_patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
		self.controller.create_patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
		self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# after creating patients, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		# cannot get current patient without setting them first
		self.assertIsNone(self.controller.get_current_patient(), "cannot get current patient without setting them first")

		# cannot set a non-existent patient to be the current patient
		with self.assertRaises(IllegalOperationException, msg="cannot set non-existent patient as the current patient"):
			self.controller.set_current_patient(9790010001)

		# set one patient to be the current patient
		self.controller.set_current_patient(9790012000)
		actual_current_patient = self.controller.get_current_patient()
		self.assertIsNotNone(actual_current_patient)
		self.assertEqual(actual_current_patient, expected_patient_3, "expected current patient is patient 3")

		# cannot delete the current patient, unset current patient first
		with self.assertRaises(IllegalOperationException, msg="cannot delete the current patient"):
			self.controller.delete_patient(9790012000)

		# cannot update the current patient, unset current patient first
		with self.assertRaises(IllegalOperationException, msg="cannot update the current patient"):
			self.controller.update_patient(9790012000, 9790012000, "John Doe", "2000-10-10", "278 999 4041", "john.doe@hotmail.com", "205 Foul Bay Rd, Oak Bay")

		# unset current patient
		self.controller.unset_current_patient()
		actual_current_patient = self.controller.get_current_patient()
		self.assertIsNone(actual_current_patient)

		# handle log out
		self.controller.set_current_patient(9790012000)
		self.controller.logout()
		with self.assertRaises(IllegalAccessException, msg="cannot get current patient without logging in"):
			self.controller.get_current_patient()


	def test_create_search_note(self):
		# some notes that may be created
		expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
		expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
		expected_note_3 = Note(3, "Patient says high BP is controlled, 120x80 in general.")

		# cannot do create and search operations without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot search note for a patient without logging in"):
			self.controller.search_note(1)
		with self.assertRaises(IllegalAccessException, msg="cannot add note for a patient without logging in"):
			self.controller.create_note("Patient comes with headache and high blood pressure.")

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# cannot do operation without a valid current patient
		with self.assertRaises(NoCurrentPatientException, msg="cannot search note without a valid current patient"):
			self.controller.search_note(1)
		with self.assertRaises(NoCurrentPatientException, msg="cannot add note without a valid current patient"):
			self.controller.create_note("Patient comes with headache and high blood pressure.")

		# add one patient and make it the current patient
		self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# after creating a patient, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		self.controller.set_current_patient(9792225555)

		# add one note
		actual_note = self.controller.create_note("Patient comes with headache and high blood pressure.")
		self.assertIsNotNone(actual_note, "note 1 was created and is valid")

		# implement __eq__(self, other) in Note to compare notes based on their code and text
		self.assertEqual(actual_note, expected_note_1, "note 1 was created and its data are correct")

		# after creating a note, reset persistence to assure that persistence is working well 
		self.reset_persistence()
		self.controller.set_current_patient(9792225555)

		# after creating the note, one should be able to search it
		actual_note = self.controller.search_note(1)
		self.assertIsNotNone(actual_note, "note created and retrieved cannot be null")
		self.assertEqual(actual_note, expected_note_1, "note 1 was created, retrieved and its data are correct")

		# add a second note
		actual_note = self.controller.create_note("Patient complains of a strong headache on the back of neck.")
		self.assertIsNotNone(actual_note, "note 2 was created and is valid")
		self.assertEqual(actual_note, expected_note_2, "note 2 was created and its data are correct")

		# after creating a note, reset persistence to assure that persistence is working well 
		self.reset_persistence()
		self.controller.set_current_patient(9792225555)

		# after creating the note, one should be able to search it
		actual_note = self.controller.search_note(2)
		self.assertIsNotNone(actual_note, "note created and retrieved cannot be null")
		self.assertEqual(actual_note, expected_note_2, "note 2 was created, retrieved and its data are correct")

		# add a third note
		actual_note = self.controller.create_note("Patient says high BP is controlled, 120x80 in general.")
		self.assertIsNotNone(actual_note, "note 3 was created and is valid")
		self.assertEqual(actual_note, expected_note_3, "note 3 was created and its data are correct")

		# after creating a note, reset persistence to assure that persistence is working well 
		self.reset_persistence()
		self.controller.set_current_patient(9792225555)

		# after creating the note, one should be able to search it
		actual_note = self.controller.search_note(3)
		self.assertIsNotNone(actual_note, "note created and retrieved cannot be null")
		self.assertEqual(actual_note, expected_note_3, "note 3 was created, retrieved and its data are correct")

		# creating new notes should not affect previous notes
		actual_note = self.controller.search_note(2)
		self.assertIsNotNone(actual_note, "note created and retrieved cannot be null regardless of search order")
		self.assertEqual(actual_note, expected_note_2, "note 2 was created, retrieved and its data are correct regardless of search order")
		actual_note = self.controller.search_note(1)
		self.assertIsNotNone(actual_note, "note created and retrieved cannot be null regardless of search order")
		self.assertEqual(actual_note, expected_note_1, "note 1 was created, retrieved and its data are correct regardless of search order")


	def test_retrieve_notes(self):
		# some notes that may be retrieved
		expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
		expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
		expected_note_3 = Note(3, "Patient is taking medicines to control blood pressure.")
		expected_note_4 = Note(4, "Patient feels general improvement and no more headaches.")
		expected_note_5 = Note(5, "Patient says high BP is controlled, 120x80 in general.")

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot retrieve notes for a patient without logging in"):
			self.controller.retrieve_notes("headache")

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# cannot do operation without a valid current patient
		with self.assertRaises(NoCurrentPatientException, msg="cannot retrieve notes without a valid current patient"):
			self.controller.retrieve_notes("headache")

		# add one patient and make it the current patient
		self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")
		self.controller.set_current_patient(9792225555)

		# add somes notes
		actual_note = self.controller.create_note("Patient comes with headache and high blood pressure.")
		actual_note = self.controller.create_note("Patient complains of a strong headache on the back of neck.")
		actual_note = self.controller.create_note("Patient is taking medicines to control blood pressure.")
		actual_note = self.controller.create_note("Patient feels general improvement and no more headaches.")
		actual_note = self.controller.create_note("Patient says high BP is controlled, 120x80 in general.")

		# retrieve one note
		retrieved_list = self.controller.retrieve_notes("neck")
		self.assertEqual(len(retrieved_list), 1, "retrieved list of notes has size 1")
		actual_note = retrieved_list[0]
		self.assertEqual(actual_note, expected_note_2, "retrieved note in the list is note 2")

		# retrieve three notes
		retrieved_list = self.controller.retrieve_notes("headache")
		self.assertEqual(len(retrieved_list), 3, "retrieved list of headache notes from Joe Hancock has size 3")
		self.assertEqual(retrieved_list[0], expected_note_1, "first retrieved note in the list is note 1")
		self.assertEqual(retrieved_list[1], expected_note_2, "second retrieved note in the list is note 2")
		self.assertEqual(retrieved_list[2], expected_note_4, "third retrieved note in the list is note 4")

		# retrieve zero notes
		retrieved_list = self.controller.retrieve_notes("lungs")
		self.assertEqual(len(retrieved_list), 0)

	def test_update_note(self):
		# some notes that may be updated
		expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
		expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
		expected_note_3 = Note(3, "Patient is taking medicines to control blood pressure.")
		expected_note_4 = Note(4, "Patient feels general improvement and no more headaches.")
		expected_note_5 = Note(5, "Patient says high BP is controlled, 120x80 in general.")

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot update note for a patient without logging in"):
			self.controller.update_note(3, "Patient is taking Losartan 50mg to control blood pressure.")

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# cannot do operation without a valid current patient
		with self.assertRaises(NoCurrentPatientException, msg="cannot update note without a valid current patient"):
			self.controller.update_note(3, "Patient is taking Losartan 50mg to control blood pressure.")

		# add one patient and make it the current patient
		self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# after creating a patient, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		self.controller.set_current_patient(9792225555)

		# try to update a note when there are no notes taken for that patient record in the system
		self.assertFalse(self.controller.update_note(3, "Patient is taking Losartan 50mg to control blood pressure."),
			"cannot update note when there are no notes for that patient record in the system")

		# add somes notes
		actual_note = self.controller.create_note("Patient comes with headache and high blood pressure.")
		actual_note = self.controller.create_note("Patient complains of a strong headache on the back of neck.")
		actual_note = self.controller.create_note("Patient is taking medicines to control blood pressure.")
		actual_note = self.controller.create_note("Patient feels general improvement and no more headaches.")
		actual_note = self.controller.create_note("Patient says high BP is controlled, 120x80 in general.")

		# after creating notes, reset persistence to assure that persistence is working well 
		self.reset_persistence()
		self.controller.set_current_patient(9792225555)

		# update one existing note
		self.assertTrue(self.controller.update_note(3, "Patient is taking Losartan 50mg to control blood pressure."), 
			"update patient record's note")

		# after updating a note, reset persistence to assure that persistence is working well 
		self.reset_persistence()
		self.controller.set_current_patient(9792225555)

		actual_note = self.controller.search_note(3)
		self.assertNotEqual(actual_note, expected_note_3, "note has updated data, cannot be equal to the original data")
		expected_note_3a = Note(3, "Patient is taking Losartan 50mg to control blood pressure.")
		self.assertEqual(actual_note, expected_note_3a, "patient was updated, their data has to be updated and correct")
		# notice we have not checked the timestamp. 
		# You should check that manually.
		# some parts of code are not simple to test. How can anyone fix that in general?

		# update another existing note
		self.assertTrue(self.controller.update_note(5, "Patient says high BP is controlled, 120x80 every morning."), 
			"update patient record's note")
		actual_note = self.controller.search_note(5)
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

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot delete note for a patient without logging in"):
			self.controller.delete_note(3)

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# cannot do operation without a valid current patient
		with self.assertRaises(NoCurrentPatientException, msg="cannot delete note without a valid current patient"):
			self.controller.delete_note(3)

		# add one patient and make it the current patient
		self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

		# after creating a patient, reset persistence to assure that persistence is working well 
		self.reset_persistence()

		self.controller.set_current_patient(9792225555)

		# try to delete a note when there are no notes taken for that patient record in the system
		self.assertFalse(self.controller.delete_note(3), "cannot delete note when there are no notes for that patient record in the system")

		# add somes notes
		actual_note = self.controller.create_note("Patient comes with headache and high blood pressure.")
		actual_note = self.controller.create_note("Patient complains of a strong headache on the back of neck.")
		actual_note = self.controller.create_note("Patient is taking medicines to control blood pressure.")
		actual_note = self.controller.create_note("Patient feels general improvement and no more headaches.")
		actual_note = self.controller.create_note("Patient says high BP is controlled, 120x80 in general.")

		# after creating notes, reset persistence to assure that persistence is working well 
		self.reset_persistence()
		self.controller.set_current_patient(9792225555)

		# delete one existing note
		self.assertTrue(self.controller.delete_note(3), "delete patient record's note")

		# after deleting a note, reset persistence to assure that persistence is working well 
		self.reset_persistence()
		self.controller.set_current_patient(9792225555)

		self.assertIsNone(self.controller.search_note(3))

		# delete the remaining existing notes regardless of deleting order
		self.assertTrue(self.controller.delete_note(1), "delete patient record's note")

		# after deleting a note, reset persistence to assure that persistence is working well 
		self.reset_persistence()
		self.controller.set_current_patient(9792225555)

		self.assertIsNone(self.controller.search_note(1))
		self.assertTrue(self.controller.delete_note(5), "delete patient record's note")

		# after deleting a note, reset persistence to assure that persistence is working well 
		self.reset_persistence()
		self.controller.set_current_patient(9792225555)

		self.assertIsNone(self.controller.search_note(5))
		self.assertTrue(self.controller.delete_note(4), "delete patient record's note")

		# after deleting a note, reset persistence to assure that persistence is working well 
		self.reset_persistence()
		self.controller.set_current_patient(9792225555)

		self.assertIsNone(self.controller.search_note(4))
		self.assertTrue(self.controller.delete_note(2), "delete patient record's note")

		# after deleting a note, reset persistence to assure that persistence is working well 
		self.reset_persistence()
		self.controller.set_current_patient(9792225555)

		self.assertIsNone(self.controller.search_note(2))

	def test_list_notes(self):
		# some notes that may be listed
		expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
		expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
		expected_note_3 = Note(3, "Patient is taking medicines to control blood pressure.")
		expected_note_4 = Note(4, "Patient feels general improvement and no more headaches.")
		expected_note_5 = Note(5, "Patient says high BP is controlled, 120x80 in general.")

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot list notes for a patient without logging in"):
			self.controller.list_notes()

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# cannot do operation without a valid current patient
		with self.assertRaises(NoCurrentPatientException, msg="cannot list notes without a valid current patient"):
			self.controller.list_notes()

		# add one patient and make it the current patient
		self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")
		self.controller.set_current_patient(9792225555)

		# listing notes when the current patient has no notes
		notes_list = self.controller.list_notes()
		self.assertEqual(len(notes_list), 0, "list of notes for patient has size 0")

		# listing notes in a singleton list
		actual_note = self.controller.create_note("Patient comes with headache and high blood pressure.")
		notes_list = self.controller.list_notes()
		self.assertEqual(len(notes_list), 1, "list of notes for patient has size 1")
		self.assertEqual(notes_list[0], expected_note_1, "Patient comes with headache and high blood pressure.")

		# add some more notes
		actual_note = self.controller.create_note("Patient complains of a strong headache on the back of neck.")
		actual_note = self.controller.create_note("Patient is taking medicines to control blood pressure.")
		actual_note = self.controller.create_note("Patient feels general improvement and no more headaches.")
		actual_note = self.controller.create_note("Patient says high BP is controlled, 120x80 in general.")

		# listing notes in a larger list
		notes_list = self.controller.list_notes()
		self.assertEqual(len(notes_list), 5, "list of notes has size 5")
		self.assertEqual(notes_list[0], expected_note_5, "note 5 is the first in the list of patients")
		self.assertEqual(notes_list[1], expected_note_4, "note 4 is the second in the list of patients")
		self.assertEqual(notes_list[2], expected_note_3, "note 3 is the third in the list of patients")
		self.assertEqual(notes_list[3], expected_note_2, "note 2 is the fourth in the list of patients")
		self.assertEqual(notes_list[4], expected_note_1, "note 1 is the fifth in the list of patients")

		# deleting some notes
		self.controller.delete_note(3)
		self.controller.delete_note(1)
		self.controller.delete_note(5)

		# listing notes for a patient with deleted notes
		notes_list = self.controller.list_notes()
		self.assertEqual(len(notes_list), 2, "list of notes has size 2")
		self.assertEqual(notes_list[0], expected_note_4, "note 4 is the first in the list of notes")
		self.assertEqual(notes_list[1], expected_note_2, "note 2 is the second in the list of notes")


if __name__ == '__main__':
	main()