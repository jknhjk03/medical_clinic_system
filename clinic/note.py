import datetime

class Note():
	''' class that represents a note '''

	def __init__(self, code, text, timestamp=datetime.datetime.now()):
		''' constructs a note '''
		self.code = code
		self.text = text
		self.timestamp = timestamp

	def __eq__(self, other):
		''' checks whether this note is the same as other note '''
		return self.code == other.code and self.text == other.text

	def __str__(self):
		''' converts the note object to a string representation '''
		return str(self.code) + "; " + str(self.timestamp) + "; " + self.text

	def __repr__(self):
		''' converts the note object to a string representation for debugging '''
		return "Note(%r, %r, %r)" % (self.code, self.timestamp, self.text)