import os
import sys
#from clinic.cli.clinic_cli import ClinicCLI
import clinic.gui.clinic_gui
from PyQt6.QtWidgets import QApplication
from clinic.gui.clinic_gui import ClinicGUI

def main():
	# You can run either a command-line interface (CLI) 
	# or a graphical user interface (GUI) to your clinic.
	if len(sys.argv) != 2:
		print('ERROR: wrong number of arguments')
		print('\nCorrect Command usage:')
		print('python -m clinic option')
		print('where option is either cli or gui')
		sys.exit()

	if sys.argv[1] == 'gui':
		clinic.gui.clinic_gui.main()
	else:
		print('ERROR: Wrong argument')
		print('\nCorrect Command usage:')
		print('python -m clinic option')
		print('where option is either cli or gui')

if __name__ == '__main__':
	main()