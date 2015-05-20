# PythonVoting Interface

import sys
from pythonvoting_dbModule import dbModule
from PyQt4 import QtGui, QtCore

class Login(QtGui.QWidget):
	"""Login Window"""
	def __init__(self):
		super(Login, self).__init__()

		self.initUI()

	def initUI(self):
		QtGui.QToolTip.setFont(QtGui.QFont('SansSerif'))

		self.setToolTip('This is a <b>QWidget</b> widget.')

		btn = QtGui.QPushButton('Quit', self)
		btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
		btn.setToolTip('This is a <b>QPushButton</b> widget.  Click to close.')
		btn.resize(btn.sizeHint())
		btn.move(50,50)

		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle('Welcome to Python Voting')
		self.show()

def main():
	app = QtGui.QApplication(sys.argv)
	login = Login()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
