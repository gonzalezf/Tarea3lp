#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import re
import urllib2
from Tkinter import *
from ttk import Frame, Button, Style

#Nuestro token global... por ahora lo obtendremos asi...
token = "1320147380.b4a3796.86fc6de63606444e9e34e795a6793606"
client_id = "b4a37965871b48f79e5365fa097f8e24"
profile_id = "1320147380"

def ParseFeed():
    query = "https://api.instagram.com/v1/users/"+profile_id+"/media/recent?access_token="+token
    response = urllib2.urlopen(query)
    the_page = response.read()
    feed = {}
    feed['images'] = []
    feed['captions'] = []
    feed['comments'] = []
    matchImage = re.findall(r'"standard_resolution":{"url":"(.*?)"', the_page)
    matchCaption = re.findall(r'"caption":(.*?),(.*?),', the_page)
    matchComment = re.findall(r'"comments":(.*?)\]}', the_page)
    if len(matchImage) > 0:
        for x in xrange(0,len(matchImage)):
            image = matchImage[x].replace('\\','')
            if matchCaption[x][0] == 'null':
                feed['images'].append(image)
                feed['captions'].append('No Caption')
            else:
                caption = re.search(r'"text":"(.*?)"', matchCaption[x][1])
                caption = caption.group(1).replace('\\','')
                feed['images'].append(image)
                feed['captions'].append(caption)

            comment_list = []
            print matchComment
            matchCommentText = re.findall(r'"text":"(.*?)"', matchComment[x][0])
            matchCommentUser = re.findall(r'"username":"(.*?)"', matchComment[x][0])
            if len(matchCommentText) > 0:
                for y in xrange(0, len(matchCommentText)):
                    text = matchCommentText.group(1).replace('\\', '')
                    user = matchCommentUser.group(1).replace('\\', '')
                comment_list.append( (text, user) )
            feed['comments'].append(comment_list)
            '''
    for i in xrange(0, len(feed['images'])):
        print "---------------POST--------------------"
        print feed['images'][i]
        print feed['captions'][i]
        print "----COMENTARIOS"
        for j in xrange(0, len(feed['comments'][i])):
            print feed['comments'][i][j][0]+": "+feed['comments'][i][j][1]
            '''

        


#Clase post: La idea es tener una lista de instancias de esta clase en
#e ir iterando una a una a medida que el usuario pide mas paginas
#Para poder probar esto es necesario realizar el parseo del objeto JSON
class Post():
    def __init__(self, author_id, author_name, desc, img_url):
        self.author_id = author_id
        self.author_name = author_name
        self.desc = desc
        self.media_id = media_id
        self.comments = []

#Ventana principal, la idea es tener un sidebar a la izquierda que se mantenga
#igual, y solo variar el contenido de adentro.
class MainWindow(Frame):
    #Esta es la ventana que contiene a todo, es similar al a tarea anterior

    #Constructor
    def __init__(self, master=None):
        #Inicializamos el frame
        Frame.__init__(self, master)

        #Dejamos la ventana Tk como maestra o root
        self.master = master

        #Diseñamos un canvas en el cual podemos insertar o remover elementos
        #Es como una especie de panel al que se le agregan distintos elementos
        self.canvas = Canvas(width = 700, height = 400)

        #Lista de objetos en el canvas (para poder borrarlos)
        #Esta lista no incluye los elementos del sidebar!!
        self.objects = []

        #Dibujar!
        self.Initialize()

    #Dibujar
    def Initialize(self):
        #Titulo de la ventana
        self.master.title("Instagram Application")

        #El estilo se puede cambiar despues, por ahora lo dejaremos
        #en gris (defecto)
        self.style = Style()
        self.style.theme_use("default")

        #Añadimos el canvas al frame
        self.canvas.pack(fill=BOTH, expand=1)

        #esto aun no funciona bien, la idea de esto es un scrollbar
        #que nos permita bajar para ver todos los comentarios. Aun no
        #esta listo!
        self.scroll = Scrollbar(self, orient=VERTICAL)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.scroll.config(command=self.canvas.yview)

        #Sidebar + Post de prueba, aca deberiamos realizar la llamada usando el API de instagram
        #llenar una lista de posts y comenzar a iterar...
        self.DrawSideBar()
        self.DrawPost()

    #Deberia ser llamado solo una vez
    def DrawSideBar(self):
        #Linea que separa el side bar (izquierda) del contenido (derecha)
        self.canvas.create_line(200, 0, 200, 700)

        #Esto es solo temporal, una linea que simula en donde estara la foto de la persona
        self.canvas.create_line(50, 40, 150, 40)
        self.canvas.create_line(50, 140, 150, 140)
        self.canvas.create_line(150, 40, 150, 140)
        self.canvas.create_line(50, 40, 50, 140)
        self.canvas.create_text(100, 90, text = "foto")

        #Creamos los botones para cerrar el programa, aun no funciona
        self.exit = Button(text = "Salir", command = self.Exit)
        self.canvas.create_window(100, 375, window = self.exit)

        #Creamos los botones del sidebar
        self.i1 = Button(text = "Ver Perfil", width = 23)
        self.i2 = Button(text = "Seguidores", width = 23)
        self.i3 = Button(text = "Seguidos", width = 23)
        self.i4 = Button(text = "Buscar Personas", width = 23)
        self.canvas.create_window(100, 200, window = self.i1)
        self.canvas.create_window(100, 225, window = self.i2)
        self.canvas.create_window(100, 250, window = self.i3)
        self.canvas.create_window(100, 275, window = self.i4)

    #Deberia recibir un objeto de clase Post, pero por mientras
    #solo lo haremos asi...
    def DrawPost(self):
        self.ClearContent()

        #Esto ya es una publicacion!!
        self.canvas.create_text(450, 15, text = "Este bloque corresponde a una publicacion")

        self.objects.append(self.canvas.create_text(450, 150, text = "foto persona"))
        self.objects.append(self.canvas.create_line(350, 50, 550, 50))
        self.objects.append(self.canvas.create_line(350, 250, 550, 250))
        self.objects.append(self.canvas.create_line(550, 50, 550, 250))
        self.objects.append(self.canvas.create_line(350, 50, 350, 250))
        self.objects.append(self.canvas.create_text(450, 300, text = "usuario1: genial la foto!\nusuario2: de donde la sacaste?\nusuario 3: buena buenaaa"))
        #self.scrollb = Scrollbar(txt_frm, command=self.txt.yview)
        #self.scrollb.grid(row=0, column=1, sticky='nsew')
        #txt = Label
        #txt['yscrollcommand'] = self.scrollb.set


        #Estos botones van en el lugar del post
        self.back = Button(text = "Atras", command = self.DrawPost) #Aca deberiamos pasar algun Id de post o lo que sea
        self.next = Button(text = "Siguiente", command = self.DrawPost)
        self.canvas.create_window(650, 375, window = self.next)
        self.canvas.create_window(560, 375, window = self.back)

    #Borrar los elementos del canvas para, generalmente, poner otros
    #No borra los del sidebar
    def ClearContent(self):
        for i in self.objects:
            self.canvas.delete(i)

    #Morir!!
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
