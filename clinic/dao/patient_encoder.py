from json import JSONEncoder
from clinic.patient import Patient

class PatientEncoder(JSONEncoder):
  ''' Encodes a patient as a JSON '''

  def default(self, obj):
    ''' returns the JSON patient as a Patient object '''
    if isinstance(obj, Patient):
      return {"__type__": "Patient", 
       "phn": obj.phn, "name": obj.name, "birth_date": obj.birth_date, "phone": obj.phone, 
       "email": obj.email, "address": obj.address, "autosave": obj.autosave}
    return super().default(obj)
