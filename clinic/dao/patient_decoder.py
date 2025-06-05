from json import JSONDecoder
from clinic.patient import Patient

class PatientDecoder(JSONDecoder):
  ''' Decodes a patient from a JSON '''

  def __init__(self, *args, **kwargs):
    ''' constructs a patient decoder '''
    super().__init__(object_hook=self.object_hook, *args, **kwargs)

  def object_hook(self, dct):
    ''' returns a patient as a JSON dictionary '''
    if '__type__' in dct and dct['__type__'] == 'Patient':
      return Patient(dct['phn'], dct['name'], dct['birth_date'], 
        dct['phone'], dct['email'], dct['address'], dct['autosave'])
    return dct
