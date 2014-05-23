#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import re
import urllib2
from Tkinter import *
from ttk import Frame, Button, Style

#Nuestro token global... por ahora lo obtendremos asi...
token = "1320147380.b4a3796.86fc6de63606444e9e34e795a6793606"

def ParseFeed():
    p = re.compile("^(\"data\")")
    lista = re.findall(p, "{\"data\": [{\"location\": {\"id\": \"833\"}}]}")
    for i in lista:
        print i
    print "{\"data\": [{\"location\": {\"id\": \"833\"}}]}"


class Post():
    def __init__(self, author_id, author_name, desc, media_id):
        self.author_id = author_id
        self.author_name = author_name
        self.desc = desc
        self.media_id = media_id
        self.comments = []

class MainWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.canvas = Canvas(width = 700, height = 400)
        self.objects = []
        self.Draw()

    def Draw(self):
        self.master.title("Instagram Application")
        self.style = Style()
        self.style.theme_use("default")
        self.canvas.pack(fill=BOTH, expand=1)
        self.scroll = Scrollbar(self,orient=VERTICAL)
        self.scroll.pack(side=RIGHT,fill=Y)
        self.scroll.config(command=self.canvas.yview)
        self.canvas.create_line(200, 0, 200, 700)
        self.canvas.create_line(50, 40, 150, 40)
        self.canvas.create_line(50, 140, 150, 140)
        self.canvas.create_line(150, 40, 150, 140)
        self.canvas.create_line(50, 40, 50, 140)
        self.canvas.create_text(100, 90, text = "foto")
        self.exit = Button(text = "Salir", command = self.Exit)
        self.canvas.create_window(100, 375, window = self.exit)
        self.i1 = Button(text = "Ver Perfil", width = 23)
        self.i2 = Button(text = "Seguidores", width = 23)
        self.i3 = Button(text = "Seguidos", width = 23)
        self.i4 = Button(text = "Buscar Personas", width = 23)
        self.back = Button(text = "Atras")
        self.next = Button(text = "Siguiente", command = self.ClearPost)
        self.canvas.create_text(450, 15, text = "Este bloque corresponde a una publicacion")

        self.objects.append(self.canvas.create_text(450, 150, text = "foto persona"))
        self.objects.append(self.canvas.create_line(350, 50, 550, 50))
        self.objects.append(self.canvas.create_line(350, 250, 550, 250))
        self.objects.append(self.canvas.create_line(550, 50, 550, 250))
        self.objects.append(self.canvas.create_line(350, 50, 350, 250))

        self.objects.append(self.canvas.create_text(450, 300, text = "Aqui iran los comentarios de la gente"))

        self.canvas.create_window(100, 200, window = self.i1)
        self.canvas.create_window(100, 225, window = self.i2)
        self.canvas.create_window(100, 250, window = self.i3)
        self.canvas.create_window(100, 275, window = self.i4)
        self.canvas.create_window(650, 375, window = self.next)

    #def RefreshPost(self, post):
    def ClearPost(self):
        for i in self.objects:
            self.canvas.delete(i)
    def Exit(self):
        self.destroy()




#Hacer !!
#class LoginWindow(Frame)


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
        #response = urllib2.urlopen('https://instagram.com/oauth/authorize/?client_id='+CLIENTID+'&redirect_uri='+REDIRECT-URII+'&response_type=token')
        #print response.info()
        #print response
        #print response.geturl()
        print "hola"
        #html = response.read()
        #print html
        #1320147380.b4a3796.86fc6de63606444e9e34e795a6793606
        url = 'https://instagram.com/oauth/authorize/?client_id=b4a37965871b48f79e5365fa097f8e24&redirect_uri=http://neopixel.org&response_type=token'
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



#No podemos usar QtGui porque es una libreria externa!
'''
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
'''
    
    
    


    


def main():
    ParseFeed()
    #root = Tk()
    #w = MainWindow(master = root)
    #w.mainloop()


if __name__ == '__main__':
    main()
