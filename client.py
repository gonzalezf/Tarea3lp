#!/usr/bin/python
# -*- coding: utf-8 -*-

import PyQt4 #instalacion via... sudo apt-get install python-qt4 sudo apt-get install libqt4-designer"""
import sys
from PyQt4 import QtGui
import urllib2


def loguearse(): #recibir access token
    #username (varchar)
    #name (varchar)
    #bio (text)
    #website (varchar)
    #instagram_id   (int)
    #instagram_acces_token  (varchar 200)

    CLIENTID = "9119878932724a62af94b0725cd415f7"
    CLIENTSECRET= "a8e0ad3201bc496187049e194c18614e"
    REDIRECTURI = "http://neopixel.org"
    WEBSITEURL= "http://neopixel.org"

    try:
        #response = urllib2.urlopen('https://instagram.com/oauth/authorize/?client_id='+CLIENTID+'&redirect_uri='+REDIRECTURI+'&response_type=token')
        #print response.info()
        #print response
        #print response.geturl()
        print "hola"
        #html = response.read()
        #print html
        url = 'https://instagram.com/oauth/authorize/?client_id=9119878932724a62af94b0725cd415f7&redirect_uri=http://neopixel.org&response_type=token'
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        #extraer respuesta
        html = response.read()
        print html
    except urllib2.HTTPError:
        print "No se pudo redireccionar" #Ejemplo claro esta,...
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise




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

    
    
    


    


def main():
    
    """app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())"""

    loguearse()

if __name__ == '__main__':
    main()
