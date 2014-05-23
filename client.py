#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import re
import urllib
import urllib2
from Tkinter import *
from ttk import Frame, Button, Style
import os
from PIL import Image, ImageTk

#Nuestro token global... por ahora lo obtendremos asi...
token = "1320147380.b4a3796.86fc6de63606444e9e34e795a6793606"
client_id = "b4a37965871b48f79e5365fa097f8e24"
profile_id = "1320147380" 

#usado para cambiar el tamaño de todas las cosas
radio = 1.5

#Ventana principal, la idea es tener un sidebar a la izquierda que se mantenga
#igual, y solo variar el contenido de adentro.
class MainWindow(Frame):
    current_post = 0
    #Esta es la ventana que contiene a todo, es similar al a tarea anterior
    #Constructor
    def __init__(self, master=None):
        #Inicializamos el frame
        Frame.__init__(self, master)

        #Dejamos la ventana Tk como maestra o root
        self.master = master

        #Diseñamos un canvas en el cual podemos insertar o remover elementos
        #Es como una especie de panel al que se le agregan distintos elementos
        self.canvas = Canvas(width = int(700*radio), height = int(400*radio))

        #Lista de objetos en el canvas (para poder borrarlos)
        #Esta lista no incluye los elementos del sidebar!!
        self.objects = []

        #Dibujar!
        self.Initialize()

    def ParseProfile(self):
        request = "https://api.instagram.com/v1/users/"+profile_id+"?access_token="+token
        response = urllib2.urlopen(request)
        the_page = response.read()

        #Leer el jason oe sixd
        self.profile = {}
        matchUser = re.search(r'"username":[^\n,}]*', the_page)
        matchBio = re.search(r'"bio":[^\n,}]*', the_page)
        matchWebsite = re.search(r'"website":[^\n,}]*', the_page)
        matchPicture = re.search(r'"profile_picture":[^\n,}]*', the_page)
        matchName = re.search(r'"full_name":[^\n,}]*', the_page)
        matchMedia = re.search(r'"media":[^\n,}]*', the_page)
        matchFollowedBy = re.search(r'"followed_by":[^\n,}]*', the_page)
        matchFollows = re.search(r'"follows":[^\n,}]*', the_page)
        self.profile['username'] = matchUser.group(0).split(':')[1][1:-1]
        self.profile['username'] = matchUser.group(0).split(':')[1][1:-1]
        self.profile['username'] = matchUser.group(0).split(':')[1][1:-1]
        self.profile['username'] = matchUser.group(0).split(':')[1][1:-1]
        self.profile['username'] = matchUser.group(0).split(':')[1][1:-1]
        self.profile['username'] = matchUser.group(0).split(':')[1][1:-1]
        self.profile['username'] = matchUser.group(0).split(':')[1][1:-1]
        self.profile['username'] = matchUser.group(0).split(':')[1][1:-1]

    #Para expresiones regulares esta pagina es muy buena!
    #http://regexpal.com/
    def ParseFeed(self):
        #Con esto obtenemos la respuesta de instagram
        #query = "https://api.instagram.com/v1/users/"+profile_id+"/media/recent?access_token="+token
        request = "https://api.instagram.com/v1/users/self/feed?access_token="+token
        response = urllib2.urlopen(request)
        the_page = response.read()
        self.feed = {}

        #Guardaremos aqui las cosas
        self.feed['images'] = []
        self.feed['captions'] = []
        self.feed['comments'] = []
        self.feed['image_file'] = []
        matchImage = re.findall(r'"low_resolution":{"url":"(.*?)"', the_page)
        matchCaption = re.findall(r'"caption":(.*?),(.*?),', the_page)
        matchComment = re.findall(r'"comments":(.*?)\]}', the_page)

        #Buscar videos y eliminarlos de la lista
        delete_list = []
        if len(matchImage) > 0:
            for x in xrange(0, len(matchImage)):
                image = matchImage[x].replace('\\','')
                s2 = image.split('.')
                if(s2[len(s2)-1] == "mp4"):
                    delete_list.append(x)
        for d in delete_list:
            del matchImage[d]

        #Comenzar a obtener la informacion
        if len(matchImage) > 0:
            for x in xrange(0,len(matchImage)):
                image = matchImage[x].replace('\\','')
                
                #Descargo la imagen
                s = image.split('/')
                image_file = s[len(s)-1]
               
                print image_file
                if not os.path.exists("img"):
                    os.makedirs("img")
                urllib.urlretrieve(image, "img/"+image_file)


                self.feed['image_file'].append(image_file)


                if matchCaption[x][0] == 'null':
                    self.feed['images'].append(image)
                    self.feed['captions'].append('No Caption')
                else:
                    caption = re.search(r'"text":"(.*?)"', matchCaption[x][1])
                    caption = caption.group(1).replace('\\','')
                    self.feed['images'].append(image)
                    self.feed['captions'].append(caption)

                comment_list = []
                matchCommentText = re.findall(r'"text":"(.*?)"', matchComment[x])
                matchCommentUser = re.findall(r'"username":"(.*?)"', matchComment[x])
                if len(matchCommentText) > 0:
                    for y in xrange(0, len(matchCommentText)):
                        text = matchCommentText[y]
                        user = matchCommentUser[y]
                        comment_list.append( (text, user) )
                self.feed['comments'].append(comment_list)
        
        for i in xrange(0, len(self.feed['images'])):
            print "---------------POST--------------------"
            print self.feed['images'][i]
            print self.feed['captions'][i]
            print "----COMENTARIOS"
            for j in xrange(0, len(self.feed['comments'][i])):
                print self.feed['comments'][i][j][1]+": "+self.feed['comments'][i][j][0]

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
        self.ParseFeed()
        self.ParseProfile()
        self.DrawPost(0)

    #Deberia ser llamado solo una vez
    def DrawSideBar(self):
        #Linea que separa el side bar (izquierda) del contenido (derecha)
        self.canvas.create_line(int(200*radio), 0, int(200*radio), int(700*radio))

        #Esto es solo temporal, una linea que simula en donde estara la foto de la persona
        self.canvas.create_line(int(50*radio), int(40*radio), int(150*radio), int(40*radio))
        self.canvas.create_line(int(50*radio), int(140*radio), int(150*radio), int(140*radio))
        self.canvas.create_line(int(150*radio), int(40*radio), int(150*radio), int(140*radio))
        self.canvas.create_line(int(50*radio), int(40*radio), int(50*radio), int(140*radio))
        self.canvas.create_text(int(100*radio), int(90*radio), text = "foto")

        #Creamos los botones para cerrar el programa, aun no funciona
        self.exit = Button(text = "Salir", command = self.Exit)
        self.canvas.create_window(int(100*radio), int(375*radio), window = self.exit)

        #Creamos los botones del sidebar
        self.i1 = Button(text = "Inicio", width = int(23*radio), command = lambda:self.DrawPost(0))
        self.i2 = Button(text = "Ver Perfil", width = int(23*radio))
        self.i3 = Button(text = "Seguidores", width = int(23*radio))
        self.i4 = Button(text = "Seguidos", width = int(23*radio))
        self.i5 = Button(text = "Buscar Personas", width = int(23*radio))
        self.canvas.create_window(int(100*radio), int(200*radio), window = self.i1)
        self.canvas.create_window(int(100*radio), int(225*radio), window = self.i2)
        self.canvas.create_window(int(100*radio), int(250*radio), window = self.i3)
        self.canvas.create_window(int(100*radio), int(275*radio), window = self.i4)
        self.canvas.create_window(int(100*radio), int(300*radio), window = self.i5)

    #Deberia recibir un objeto de clase Post, pero por mientras
    #solo lo haremos asi...
    def DrawPost(self, post_id):
        print "DRAW:"+str(post_id)+"/"+str(len(self.feed['images']))
        if(post_id < 0 or post_id >= len(self.feed['images'])):
            return
        current_post = post_id
        self.ClearContent()

        #Esto ya es una publicacion!!
        self.objects.append(self.canvas.create_text(int(450*radio), int(15*radio), text = "Este bloque corresponde a una publicacion"))
        self.im = Image.open(self.feed['image_file'][post_id])
        self.im = self.im.resize((int(150*radio)    , int(150*radio)), Image.ANTIALIAS)
        self.tkimg = ImageTk.PhotoImage(self.im)
        self.objects.append(self.canvas.create_image(int(375*radio), int(50*radio), image=self.tkimg, anchor = NW, tags = "bg_img"))
        #self.objects.append(self.canvas.create_text(450, 150, text = "foto persona"))
        #self.objects.append(self.canvas.create_line(350, 50, 550, 50))
        #self.objects.append(self.canvas.create_line(350, 250, 550, 250))
        #self.objects.append(self.canvas.create_line(550, 50, 550, 250))
        #self.objects.append(self.canvas.create_line(350, 50, 350, 250))
        comments = ""
        for j in xrange(0, len(self.feed['comments'][post_id])):
            comments += self.feed['comments'][post_id][j][1]+": "+self.feed['comments'][post_id][j][0]+"\n"

        tx = Label(text = comments, width = int(50*radio), height = int(7*radio), bg = "white", wraplength = 300*radio, relief = RIDGE)
        self.objects.append(self.canvas.create_window(int(450*radio), int(275*radio), window = tx))
        #s = Scrollbar(self, orient = VERTICAL)
        #s.pack(side = RIGHT, fill = Y)
        #s.config(command=comment_canvas.yview)
        #comment_canvas.create_window(400, 0, window = s)
        #comment_canvas.create_text(0, 0, text = comments)
        #comment_canvas.config(yscrollcommand=s.set)
        #self.scrollb = Scrollbar(txt_frm, command=self.txt.yview)
        #self.scrollb.grid(row=0, column=1, sticky='nsew')
        #txt = Label
        #txt['yscrollcommand'] = self.scrollb.set


        #Estos botones van en el lugar del post

        if(post_id > 0):
            self.back = Button(text = "Atras", command = lambda: self.DrawPost(current_post-1)) #Aca deberiamos pasar algun Id de post o lo que sea
            self.objects.append(self.canvas.create_window(int(560*radio), int(375*radio), window = self.back))
        if post_id < len(self.feed['images'])-1:
            self.next = Button(text = "Siguiente", command = lambda: self.DrawPost(current_post+1))
            self.objects.append(self.canvas.create_window(int(650*radio), int(375*radio), window = self.next))
        

    #Borrar los elementos del canvas para, generalmente, poner otros
    #No borra los del sidebar
    def ClearContent(self):
        for i in self.objects:
            self.canvas.delete(i)

    #Morir!!
    def Exit(self):
        self.master.destroy()




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
    root = Tk()
    w = MainWindow(master = root)
    w.mainloop()


if __name__ == '__main__':
    main()
