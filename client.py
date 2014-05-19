#!/usr/bin/python
# -*- coding: utf-8 -*-

import PyQt4 #instalacion via... sudo apt-get install python-qt4 sudo apt-get install libqt4-designer"""
import sys
from PyQt4 import QtGui

class Example(QtGui.QWidget): #clase que maneja la interfaz
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI() #llamamos al metodo initUI
    
    def initUI(self): #aqui va el codigo de la ventana
        
 		QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
 		self.setToolTip('This is a <b>QWidget</b> widget')
 		

 		btn = QtGui.QPushButton('Iniciar Sesion', self)
 		btn.setToolTip('Haga click para <b>iniciar sesion </b> ')
 		btn.resize(btn.sizeHint())
 		btn.move(50, 50)
 		btn.clicked.connect(self.loguearse)
 		
 		#redirigir al usuario a https://instagram.com/oauth/authorize/?client_id=CLIENT-ID&redirect_uri=REDIRECT-URI&response_type=token
 		#en ese lugar debe loguearse!

      	#propiedades de ventana
 		self.setGeometry(500, 300, 250, 150) #posicion x, posicion y, ancho, altura
 		self.setWindowTitle('Webgram')
 		self.setWindowIcon(QtGui.QIcon('instagram1.png'))     #reparar, verificar porque no se ve el icono.    
 		self.show()

    
    
    
	def loguearse(self):
		print "holi"    

    


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
