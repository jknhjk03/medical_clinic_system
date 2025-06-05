from unittest import TestCase
from unittest import main
from clinic.patient import Patient

class PatientTest(TestCase):
	def setUp(self):
		self.patient = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")

	def test_eq(self):
		same_patient = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		different_patient_1 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		different_patient_2 = Patient(9790015555, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		different_patient_3 = Patient(9790012000, "John Smith", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		self.assertTrue(self.patient == self.patient)
		self.assertTrue(self.patient == same_patient)
		self.assertFalse(self.patient == different_patient_1)
		self.assertFalse(self.patient == different_patient_2)
		self.assertFalse(self.patient == different_patient_3)

	def test_str(self):
		same_patient = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		different_patient_1 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		different_patient_2 = Patient(9790015555, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		different_patient_3 = Patient(9790012000, "John Smith", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		self.assertEqual("9790012000; John Doe; 2000-10-10; 250 203 1010; john.doe@gmail.com; 300 Moss St, Victoria", str(self.patient))
		self.assertEqual("9790012000; John Doe; 2000-10-10; 250 203 1010; john.doe@gmail.com; 300 Moss St, Victoria", str(same_patient))
		self.assertEqual("9790014444; Mary Doe; 1995-07-01; 250 203 2020; mary.doe@gmail.com; 300 Moss St, Victoria", str(different_patient_1))
		self.assertEqual("9790015555; John Doe; 2000-10-10; 250 203 1010; john.doe@gmail.com; 300 Moss St, Victoria", str(different_patient_2))
		self.assertEqual("9790012000; John Smith; 2000-10-10; 250 203 1010; john.doe@gmail.com; 300 Moss St, Victoria", str(different_patient_3))
		self.assertEqual(str(same_patient), str(self.patient))
		self.assertNotEqual(str(different_patient_1), str(self.patient))
		self.assertNotEqual(str(different_patient_2), str(self.patient))
		self.assertNotEqual(str(different_patient_3), str(self.patient))

	def test_repr(self):
		same_patient = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		different_patient_1 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
		different_patient_2 = Patient(9790015555, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		different_patient_3 = Patient(9790012000, "John Smith", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
		self.assertEqual("Patient(9790012000, 'John Doe', '2000-10-10', '250 203 1010', 'john.doe@gmail.com', '300 Moss St, Victoria')", repr(self.patient))
		self.assertEqual("Patient(9790012000, 'John Doe', '2000-10-10', '250 203 1010', 'john.doe@gmail.com', '300 Moss St, Victoria')", repr(same_patient))
		self.assertEqual("Patient(9790014444, 'Mary Doe', '1995-07-01', '250 203 2020', 'mary.doe@gmail.com', '300 Moss St, Victoria')", repr(different_patient_1))
		self.assertEqual("Patient(9790015555, 'John Doe', '2000-10-10', '250 203 1010', 'john.doe@gmail.com', '300 Moss St, Victoria')", repr(different_patient_2))
		self.assertEqual("Patient(9790012000, 'John Smith', '2000-10-10', '250 203 1010', 'john.doe@gmail.com', '300 Moss St, Victoria')", repr(different_patient_3))
		self.assertEqual(repr(same_patient), repr(self.patient))
		self.assertNotEqual(repr(different_patient_1), repr(self.patient))
		self.assertNotEqual(repr(different_patient_2), repr(self.patient))
		self.assertNotEqual(repr(different_patient_3), repr(self.patient))

if __name__ == '__main__':
	main()