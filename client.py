#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import re
import urllib
import urllib2
from Tkinter import *
import Tkinter as tk
from ttk import Frame, Button, Style
import os
from PIL import Image, ImageTk

#Nuestro token global... por ahora lo obtendremos asi...
#token = "1320147380.b4a3796.86fc6de63606444e9e34e795a6793606"
client_id = "b4a37965871b48f79e5365fa097f8e24"

OUR_PROFILE_ID = "1320147380"

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
        self.token = 'invalid'

        #Diseñamos un canvas en el cual podemos insertar o remover elementos
        #Es como una especie de panel al que se le agregan distintos elementos
        self.canvas = Canvas(width = int(700*radio), height = int(400*radio))

        #Lista de objetos en el canvas (para poder borrarlos)
        #Esta lista no incluye los elementos del sidebar!!
        self.objects = []
        self.view_profile = {}
        self.profile = {}
        self.feed = {}
        self.following = {}
        self.followers = {}
        self.search_reply = {}

        #Dibujar!
        self.Initialize()


    def OnFollowButton(self, profile):
        action = ""
        if(self.view_profile['is_followed'] == 'none'):
            action = "follow"
        else:
            action = "unfollow"
        request = "https://api.instagram.com/v1/users/"+profile+"/relationship"
        data = urllib.urlencode({"action": action, "access_token": self.token})
        response = urllib.urlopen(request, data)
        the_page = response.read()
        self.DrawOtherProfile(profile, 1)

    def ParseSearch(self, name):
        request = "https://api.instagram.com/v1/users/search?q="+name+"&access_token="+self.token
        print request
        response = urllib2.urlopen(request)
        the_page = response.read()

        self.search_reply['pictures'] = []
        self.search_reply['ids'] = []
        self.search_reply['names'] = []
        matchImage = re.findall(r'"profile_picture"[^,}]*', the_page)
        matchId = re.findall(r'"id"[^,}]*', the_page)
        matchName = re.findall(r'"username"[^,}]*', the_page)
        self.search_reply['pictures'].append('NULL')
        self.search_reply['ids'].append('NULL')
        self.search_reply['names'].append('NULL')
        if len(matchImage) > 0:
            for x in xrange(0,len(matchImage)):
                image = matchImage[x].replace('\\','').split(':', 1)[1][1:-1]
                
                #Descargo la imagen
                s = image.split('/')
                image_file = s[len(s)-1]
                
                if not os.path.exists("img"):
                    os.makedirs("img")
                if(not os.path.isfile("img/"+image_file)):
                    urllib.urlretrieve(image, "img/"+image_file)
                self.search_reply['pictures'].append(image_file)
                print image_file
                self.search_reply['ids'].append(matchId[x].split(':', 1)[1][1:-1].replace('\\',''))
                self.search_reply['names'].append(matchName[x].split(':', 1)[1][1:-1].replace('\\',''))
                print matchId[x].split(':', 1)[1][1:-1].replace('\\','')



    def ParseFollowers(self):
        request = "https://api.instagram.com/v1/users/"+OUR_PROFILE_ID+"/followed-by?access_token="+self.token
        response = urllib2.urlopen(request)
        the_page = response.read()


        self.followers['pictures'] = []
        self.followers['ids'] = []
        matchImage = re.findall(r'"profile_picture"[^,}]*', the_page)
        matchId = re.findall(r'"id"[^,}]*', the_page)
        self.followers['pictures'].append('NULL')
        self.followers['ids'].append('NULL')
        if len(matchImage) > 0:
            for x in xrange(0,len(matchImage)):
                image = matchImage[x].replace('\\','').split(':', 1)[1][1:-1]
                
                #Descargo la imagen
                s = image.split('/')
                image_file = s[len(s)-1]
                
                if not os.path.exists("img"):
                    os.makedirs("img")
                if(not os.path.isfile("img/"+image_file)):
                    urllib.urlretrieve(image, "img/"+image_file)
                self.followers['pictures'].append(image_file)
                print image_file
                self.followers['ids'].append(matchId[x].split(':', 1)[1][1:-1].replace('\\',''))
                print matchId[x].split(':', 1)[1][1:-1].replace('\\','')

    def ParseFollowing(self):
        request = "https://api.instagram.com/v1/users/"+OUR_PROFILE_ID+"/follows?access_token="+self.token
        response = urllib2.urlopen(request)
        the_page = response.read()


        self.following['pictures'] = []
        self.following['ids'] = []
        matchImage = re.findall(r'"profile_picture"[^,}]*', the_page)
        matchId = re.findall(r'"id"[^,}]*', the_page)
        self.following['pictures'].append('NULL')
        self.following['ids'].append('NULL')
        if len(matchImage) > 0:
            for x in xrange(0,len(matchImage)):
                image = matchImage[x].replace('\\','').replace('\\','').split(':', 1)[1][1:-1]
                
                #Descargo la imagen
                s = image.split('/')
                image_file = s[len(s)-1]
                
                if not os.path.exists("img"):
                    os.makedirs("img")
                if(not os.path.isfile("img/"+image_file)):
                    urllib.urlretrieve(image, "img/"+image_file)
                


                self.following['pictures'].append(image_file)
                print image_file
                self.following['ids'].append(matchId[x].split(':', 1)[1][1:-1].replace('\\',''))
                print matchId[x].split(':', 1)[1][1:-1].replace('\\','')



    def ParseProfile(self):
        request = "https://api.instagram.com/v1/users/"+OUR_PROFILE_ID+"?access_token="+self.token
        response = urllib2.urlopen(request)
        the_page = response.read()

        #Leer el jason oe sixd
        matchUser = re.search(r'"username":[^\n,}]*', the_page)
        matchBio = re.search(r'"bio":[^\n,}]*', the_page)
        matchWebsite = re.search(r'"website":[^\n,}]*', the_page)
        matchPicture = re.search(r'"profile_picture":[^\n,}]*', the_page)
        matchName = re.search(r'"full_name":[^\n,}]*', the_page)
        matchMedia = re.search(r'"media":[^\n,}]*', the_page)
        matchFollowedBy = re.search(r'"followed_by":[^\n,}]*', the_page)
        matchFollows = re.search(r'"follows":[^\n,}]*', the_page)
        self.profile['username'] = matchUser.group(0).split(':', 1)[1][1:-1].replace('\\','')
        self.profile['bio'] = matchBio.group(0).split(':', 1)[1][1:-1].replace('\\','')
        self.profile['website'] = matchWebsite.group(0).split(':', 1)[1][1:-1].replace('\\','')
        self.profile['picture'] = matchPicture.group(0).split(':', 1)[1][1:-1].replace('\\','')
        s = self.profile['picture'].split('/')
        image_file = s[len(s)-1]

        if not os.path.exists("img"):
            os.makedirs("img")
        if(not os.path.isfile("img/"+image_file)):
            urllib.urlretrieve(self.profile['picture'], "img/"+image_file)
        self.profile['picture'] = image_file


        self.profile['name'] = matchName.group(0).split(':', 1)[1][1:-1].replace('\\','')
        self.profile['media'] = matchMedia.group(0).split(':', 1)[1]
        self.profile['followed_by'] = matchFollowedBy.group(0).split(':', 1)[1]
        self.profile['follows'] = matchFollows.group(0).split(':', 1)[1]

    def ParseOtherProfile(self, profile):
        request = "https://api.instagram.com/v1/users/"+profile+"?access_token="+self.token
        response = urllib2.urlopen(request)
        the_page = response.read()

        #Leer el jason oe sixd
        matchUser = re.search(r'"username":[^\n,}]*', the_page)
        matchBio = re.search(r'"bio":[^\n,}]*', the_page)
        matchWebsite = re.search(r'"website":[^\n,}]*', the_page)
        matchPicture = re.search(r'"profile_picture":[^\n,}]*', the_page)
        matchName = re.search(r'"full_name":[^\n,}]*', the_page)
        matchMedia = re.search(r'"media":[^\n,}]*', the_page)
        matchFollowedBy = re.search(r'"followed_by":[^\n,}]*', the_page)
        matchFollows = re.search(r'"follows":[^\n,}]*', the_page)
        self.view_profile['profile_id'] = profile
        self.view_profile['username'] = matchUser.group(0).split(':', 1)[1][1:-1].replace('\\','')
        self.view_profile['bio'] = matchBio.group(0).split(':', 1)[1][1:-1].replace('\\','')
        self.view_profile['website'] = matchWebsite.group(0).split(':', 1)[1][1:-1].replace('\\','')
        self.view_profile['picture'] = matchPicture.group(0).split(':', 1)[1][1:-1].replace('\\','')
        s = self.view_profile['picture'].split('/')
        image_file = s[len(s)-1]

        if not os.path.exists("img"):
            os.makedirs("img")
        if(not os.path.isfile("img/"+image_file)):
            urllib.urlretrieve(self.view_profile['picture'], "img/"+image_file)
        self.view_profile['picture'] = image_file

        self.view_profile['name'] = matchName.group(0).split(':', 1)[1][1:-1].replace('\\','')
        self.view_profile['media'] = matchMedia.group(0).split(':', 1)[1]
        self.view_profile['followed_by'] = matchFollowedBy.group(0).split(':', 1)[1]
        self.view_profile['follows'] = matchFollows.group(0).split(':', 1)[1]
        request = "https://api.instagram.com/v1/users/"+profile+"/relationship?access_token="+self.token
        response = urllib2.urlopen(request)
        the_page = response.read()

        matchRelationship = re.search(r'"outgoing_status":[^\n,}]*', the_page)
        self.view_profile['is_followed'] = matchRelationship.group(0).split(':', 1)[1][1:-1].replace('\\','')


    def ParseOwnRecentPhotos(self):
        request = "https://api.instagram.com/v1/users/"+OUR_PROFILE_ID+"/media/recent?access_token="+self.token
        response = urllib2.urlopen(request)
        the_page = response.read()

        #Guardaremos aqui las cosas
        self.view_profile['images'] = []
        matchImage = re.findall(r'"standard_resolution":{"url":"(.*?)"', the_page)

        #Buscar videos y eliminarlos de la lista
        delete_list = []
        if len(matchImage) > 0:
            for x in xrange(0, len(matchImage)):
                image = matchImage[x].replace('\\','')
                s2 = image.split('.')
                print s2[len(s2)-1]
                if(s2[len(s2)-1] == "mp4"):
                    delete_list.append(x)
        removed = 0
        for d in delete_list:
            print "Removing: "+str(d-removed)
            del matchImage[d-removed]
            removed+=1
        #Comenzar a obtener la informacion
        self.view_profile['images'].append('NULL')
        if len(matchImage) > 0:
            for x in xrange(0,len(matchImage)):
                image = matchImage[x].replace('\\','')
                
                #Descargo la imagen
                s = image.split('/')
                image_file = s[len(s)-1]

                if not os.path.exists("img"):
                    os.makedirs("img")
                if(not os.path.isfile("img/"+image_file)):
                    urllib.urlretrieve(image, "img/"+image_file)


                self.view_profile['images'].append(image_file)

    def ParseOtherRecentPhotos(self, profile):
        request = "https://api.instagram.com/v1/users/"+profile+"/media/recent?access_token="+self.token
        response = urllib2.urlopen(request)
        the_page = response.read()
        #Guardaremos aqui las cosas
        self.view_profile['images'] = []
        matchImage = re.findall(r'"standard_resolution":{"url":"(.*?)"', the_page)

        #Buscar videos y eliminarlos de la lista
        delete_list = []
        if len(matchImage) > 0:
            for x in xrange(0, len(matchImage)):
                image = matchImage[x].replace('\\','')
                s2 = image.split('.')
                print s2[len(s2)-1]
                if(s2[len(s2)-1] == "mp4"):
                    delete_list.append(x)
        removed = 0
        for d in delete_list:
            print "Removing: "+str(d-removed)
            del matchImage[d-removed]
            removed+=1
        #Comenzar a obtener la informacion
        self.view_profile['images'].append('NULL')
        if len(matchImage) > 0:
            for x in xrange(0,len(matchImage)):
                image = matchImage[x].replace('\\','')
                
                #Descargo la imagen
                s = image.split('/')
                image_file = s[len(s)-1]

                if not os.path.exists("img"):
                    os.makedirs("img")
                if(not os.path.isfile("img/"+image_file)):
                    urllib.urlretrieve(image, "img/"+image_file)


                self.view_profile['images'].append(image_file)



    #Para expresiones regulares esta pagina es muy buena!
    #http://regexpal.com/
    def ParseFeed(self):
        #Con esto obtenemos la respuesta de instagram
        #query = "https://api.instagram.com/v1/users/"+OUR_PROFILE_ID+"/media/recent?access_token="+token
        request = "https://api.instagram.com/v1/users/self/feed?access_token="+self.token
        response = urllib2.urlopen(request)
        the_page = response.read()
        self.feed = {}

        #Guardaremos aqui las cosas
        self.feed['images'] = []
        self.feed['captions'] = []
        self.feed['comments'] = []
        self.feed['image_file'] = []
        self.feed['userid'] = []
        self.feed['username'] = []
        matchImage = re.findall(r'"standard_resolution":{"url":"(.*?)"', the_page)
        matchCaption = re.findall(r'"caption":(.*?),(.*?),', the_page)
        matchComment = re.findall(r'"comments":(.*?)\]}', the_page)
        matchUser1 = re.findall(r'",[^{]*"user"[^}]*', the_page)

        #Buscar videos y eliminarlos de la lista
        delete_list = []
        if len(matchImage) > 0:
            for x in xrange(0, len(matchImage)):
                image = matchImage[x].replace('\\','')
                s2 = image.split('.')
                print s2[len(s2)-1]
                if(s2[len(s2)-1] == "mp4"):
                    delete_list.append(x)
        removed = 0
        for d in delete_list:
            print "Removing: "+str(d-removed)
            del matchImage[d-removed]
            removed+=1
        #Comenzar a obtener la informacion
        if len(matchImage) > 0:
            for x in xrange(0,len(matchImage)):
                image = matchImage[x].replace('\\','')
                
                #Descargo la imagen
                s = image.split('/')
                image_file = s[len(s)-1]

                if not os.path.exists("img"):
                    os.makedirs("img")
                if(not os.path.isfile("img/"+image_file)):
                    urllib.urlretrieve(image, "img/"+image_file)


                self.feed['image_file'].append(image_file)
                caption = re.search(r'"text":"(.*?)"', matchCaption[x][1])


                if matchCaption[x][0] == 'null' or caption == None:
                    self.feed['images'].append(image)
                    self.feed['captions'].append('')
                else:
                    
                    caption = caption.group().replace('\\','')
                    self.feed['images'].append(image)
                    self.feed['captions'].append(caption)

                #le expression: "id":(.*)
                matchUser = re.search(r'"user"[^}]*', matchUser1[x])
                matchId = re.search(r'"id":[^},\n]*', matchUser.group(0))
                matchUsername = re.search(r'"username":[^},\n]*', matchUser.group(0))
                self.feed['userid'].append(matchId.group(0).split(':', 1)[1][1:-1])
                self.feed['username'].append(matchUsername.group(0).split(':', 1)[1][1:-1])

                comment_list = []
                matchCommentText = re.findall(r'"text":"(.*?)"', matchComment[x])
                matchCommentUser = re.findall(r'"username":"(.*?)"', matchComment[x])
                if len(matchCommentText) > 0:
                    for y in xrange(0, len(matchCommentText)):
                        text = matchCommentText[y]
                        user = matchCommentUser[y]
                        comment_list.append( (text, user) )
                self.feed['comments'].append(comment_list)

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

        
        self.GetToken()

    def GetToken(self):
        self.token_entry = Entry(width = int(60*radio))
        self.token_button = Button(text = "Ingresar", command = lambda:self.OnTokenObtained())
        self.objects.append(self.canvas.create_window(int(350*radio), int(100*radio), window = self.token_entry))
        self.objects.append(self.canvas.create_window(int(350*radio), int(120*radio), window = self.token_button))
        self.objects.append(self.canvas.create_text(int(350*radio), int(80*radio), text = "Ingrese el token"))

    def OnTokenObtained(self):
        #Sidebar + Post de prueba, aca deberiamos realizar la llamada usando el API de instagram
        #llenar una lista de posts y comenzar a iterar...
        self.token = self.token_entry.get()
        print "Cargando..."
        self.ParseFeed()
        self.ParseProfile()
        self.DrawSideBar()
        self.DrawPost(0)

    def DrawFollowers(self, page):
        if(page == 1):
            self.ParseFollowers()
        self.ClearContent()

        pages = (len(self.followers['pictures'])/12)+1
        if(page > pages):
            page = pages
        print pages
        x = 230
        y = 30
        elements_per_page = 12
        self.view_profile_im = []
        self.view_profile_tkimg = []
        #Imagen por imagen
        for i in range(1, elements_per_page+1):
            if(i+elements_per_page*(page-1) >= len(self.followers['pictures'])):
                break
            print "img/"+self.followers['pictures'][i+elements_per_page*(page-1)]
            self.view_profile_im.append(Image.open("img/"+self.followers['pictures'][i+elements_per_page*(page-1)]))
            self.view_profile_im[i-1] = self.view_profile_im[i-1].resize((int(70*radio) , int(70*radio)), Image.ANTIALIAS)
            self.view_profile_tkimg.append(ImageTk.PhotoImage(self.view_profile_im[i-1]))
            self.objects.append(self.canvas.create_image(int(x*radio), int(y*radio), image=self.view_profile_tkimg[i-1], anchor = NW))
            btn = Button(text = "Ver Perfil", command = self.DrawOtherProfile_CB(self.followers['ids'][i+elements_per_page*(page-1)], 1))
            self.objects.append(self.canvas.create_window(int((x+35)*radio), int(y+80)*radio, window=btn))
            x += 110
            if(i % 4 == 0):
                x = 230
                y += 105
        if(page > 1):
            self.back = Button(text = "Atras", command = lambda: self.DrawFollowers(page-1)) #Aca deberiamos pasar algun Id de post o lo que sea
            self.objects.append(self.canvas.create_window(int(560*radio), int(375*radio), window = self.back))
        if page < pages:
            self.next = Button(text = "Siguiente", command = lambda: self.DrawFollowers(page+1))
            self.objects.append(self.canvas.create_window(int(650*radio), int(375*radio), window = self.next))

    def DrawOtherProfile_CB(self, profile, page):
        return lambda:self.DrawOtherProfile(profile, page);

    def DrawFollowing(self, page):
        if(page == 1):
            self.ParseFollowing()

        self.ClearContent()

        pages = (len(self.following['pictures'])/12)+1
        if(page > pages):
            page = pages
        print pages
        x = 230
        y = 30
        elements_per_page = 12
        self.view_profile_im = []
        self.view_profile_tkimg = []
        #Imagen por imagen
        for i in range(1, elements_per_page+1):
            if(i+elements_per_page*(page-1) >= len(self.following['pictures'])):
                break
            print "img/"+self.following['pictures'][i+elements_per_page*(page-1)]
            self.view_profile_im.append(Image.open("img/"+self.following['pictures'][i+elements_per_page*(page-1)]))
            self.view_profile_im[i-1] = self.view_profile_im[i-1].resize((int(70*radio) , int(70*radio)), Image.ANTIALIAS)
            self.view_profile_tkimg.append(ImageTk.PhotoImage(self.view_profile_im[i-1]))
            self.objects.append(self.canvas.create_image(int(x*radio), int(y*radio), image=self.view_profile_tkimg[i-1], anchor = NW))
            print str(i+elements_per_page*(page-1)) +"|"+ str(len(self.following['ids']))+"|"+str(len(self.following['pictures']))
            btn = Button(text = "Ver Perfil", command = self.DrawOtherProfile_CB(self.following['ids'][i+elements_per_page*(page-1)], 1))
            self.objects.append(self.canvas.create_window(int((x+35)*radio), int(y+80)*radio, window=btn))
            x += 110
            if(i % 4 == 0):
                x = 230
                y += 105
        if(page > 1):
            self.back = Button(text = "Atras", command = lambda: self.DrawFollowing(page-1)) #Aca deberiamos pasar algun Id de post o lo que sea
            self.objects.append(self.canvas.create_window(int(560*radio), int(375*radio), window = self.back))
        if page < pages:
            self.next = Button(text = "Siguiente", command = lambda: self.DrawFollowing(page+1))
            self.objects.append(self.canvas.create_window(int(650*radio), int(375*radio), window = self.next))

    def DrawSearchInput(self):
        self.ClearContent();
        self.search_entry = Entry()
        self.objects.append(self.canvas.create_window(int(450*radio), int(40*radio), window = self.search_entry))
        self.objects.append(self.canvas.create_text(int(450*radio), int(20*radio), text = "Ingrese nombre: "))
        self.search_button = Button(text = "Buscar", command = lambda: self.DrawSearchReply(1, True))
        self.objects.append(self.canvas.create_window(int(450*radio), int(60*radio), window = self.search_button))

    def DrawSearchReply(self, page, parse):
        if(parse == True):
            self.ParseSearch(self.search_entry.get())
        self.ClearContent();
        self.search_entry = Entry()
        self.objects.append(self.canvas.create_window(int(450*radio), int(40*radio), window = self.search_entry))
        self.objects.append(self.canvas.create_text(int(450*radio), int(20*radio), text = "Ingrese nombre: "))
        self.search_button = Button(text = "Buscar", command = lambda: self.DrawSearchReply(1, True))
        self.objects.append(self.canvas.create_window(int(450*radio), int(60*radio), window = self.search_button))
        
        pages = (len(self.search_reply['pictures'])/8)+1
        if(page > pages):
            page = pages
        print pages
        x = 230
        y = 100
        elements_per_page = 8
        self.view_profile_im = []
        self.view_profile_tkimg = []
        #Imagen por imagen
        for i in range(1, elements_per_page+1):
            if(i+elements_per_page*(page-1) >= len(self.search_reply['pictures'])):
                break
            print "img/"+self.search_reply['pictures'][i+elements_per_page*(page-1)]
            self.view_profile_im.append(Image.open("img/"+self.search_reply['pictures'][i+elements_per_page*(page-1)]))
            self.view_profile_im[i-1] = self.view_profile_im[i-1].resize((int(70*radio) , int(70*radio)), Image.ANTIALIAS)
            self.view_profile_tkimg.append(ImageTk.PhotoImage(self.view_profile_im[i-1]))
            self.objects.append(self.canvas.create_image(int(x*radio), int(y*radio), image=self.view_profile_tkimg[i-1], anchor = NW))
            btn = Button(text = "Ver Perfil", command = self.DrawOtherProfile_CB(self.search_reply['ids'][i+elements_per_page*(page-1)], 1))
            self.objects.append(self.canvas.create_text(int((x+35)*radio), int((y+80)*radio), text = self.search_reply['names'][i+elements_per_page*(page-1)]))
            self.objects.append(self.canvas.create_window(int((x+35)*radio), int(y+100)*radio, window=btn))
            x += 110
            if(i % 4 == 0):
                x = 230
                y += 120
        if(page > 1):
            self.back = Button(text = "Atras", command = lambda: self.DrawSearchReply(page-1)) #Aca deberiamos pasar algun Id de post o lo que sea
            self.objects.append(self.canvas.create_window(int(560*radio), int(375*radio), window = self.back))
        if page < pages:
            self.next = Button(text = "Siguiente", command = lambda: self.DrawSearchReply(page+1))
            self.objects.append(self.canvas.create_window(int(650*radio), int(375*radio), window = self.next))



    #Deberia ser llamado solo una vez
    def DrawSideBar(self):
        #Linea que separa el side bar (izquierda) del contenido (derecha)
        self.canvas.create_line(int(200*radio), 0, int(200*radio), int(700*radio))

        #Esto es solo temporal, una linea que simula en donde estara la foto de la persona
        print "img/"+self.profile['picture']
        self.sidebar_im = Image.open("img/"+self.profile['picture'])
        self.sidebar_im = self.sidebar_im.resize((int(80*radio)    , int(80*radio)), Image.ANTIALIAS)
        self.sidebar_tkimg = ImageTk.PhotoImage(self.sidebar_im)
        self.canvas.create_image(int(58*radio), int(40*radio), image=self.sidebar_tkimg, anchor = NW)
        self.sidebar_user = Label(text = self.profile['username'])
        self.canvas.create_window(int(100*radio), int(130*radio), window = self.sidebar_user)

        #Creamos los botones para cerrar el programa, aun no funciona
        self.exit = Button(text = "Salir", command = self.Exit)
        self.canvas.create_window(int(100*radio), int(375*radio), window = self.exit)
        self.update = Button(text = "Update", command = self.Update)
        self.canvas.create_window(int(100*radio), int(350*radio), window = self.update)

        #Creamos los botones del sidebar
        self.i1 = Button(text = "Inicio", width = int(23*radio), command = lambda:self.DrawPost(0))
        self.i2 = Button(text = "Ver Perfil", width = int(23*radio), command = lambda:self.DrawOwnProfile(1))
        self.i3 = Button(text = "Seguidores", width = int(23*radio), command = lambda:self.DrawFollowers(1))
        self.i4 = Button(text = "A los que sigo", width = int(23*radio), command = lambda:self.DrawFollowing(1))
        self.i5 = Button(text = "Buscar Personas", width = int(23*radio), command = lambda:self.DrawSearchInput())
        self.canvas.create_window(int(100*radio), int(200*radio), window = self.i1)
        self.canvas.create_window(int(100*radio), int(225*radio), window = self.i2)
        self.canvas.create_window(int(100*radio), int(250*radio), window = self.i3)
        self.canvas.create_window(int(100*radio), int(275*radio), window = self.i4)
        self.canvas.create_window(int(100*radio), int(300*radio), window = self.i5)

    #Deberia recibir un objeto de clase Post, pero por mientras
    #solo lo haremos asi...
    def DrawOwnProfile(self, page):
        if(page == 1):
            self.ParseOwnRecentPhotos()
        self.ClearContent()

        #Separador horizontal
        self.objects.append(self.canvas.create_line(int(200*radio), int(100*radio), int(700*radio), int(100*radio)))

        #Foto de perfil
        self.view_profile_im = []
        self.view_profile_tkimg = []
        print "img/"+self.profile['picture']
        self.view_profile_im.append(Image.open("img/"+self.profile['picture']))
        self.view_profile_im[0] = self.view_profile_im[0].resize((int(80*radio) , int(80*radio)), Image.ANTIALIAS)
        self.view_profile_tkimg.append(ImageTk.PhotoImage(self.view_profile_im[0]))
        self.objects.append(self.canvas.create_image(int(210*radio), int(10*radio), image=self.view_profile_tkimg[0], anchor = NW))
        username = self.profile['username']
        bio = self.profile['bio']
        website = self.profile['website']
        follows = self.profile['follows']
        followed_by = self.profile['followed_by']
        self.objects.append(self.canvas.create_text(int(450*radio), int(25*radio), text = username))
        self.objects.append(self.canvas.create_text(int(450*radio), int(45*radio), text = bio, width = int(300*radio)))
        self.objects.append(self.canvas.create_text(int(450*radio), int(65*radio), text = website))
        self.objects.append(self.canvas.create_text(int(650*radio), int(35*radio), text = "Sigues: "+follows))
        self.objects.append(self.canvas.create_text(int(650*radio), int(55*radio), text = "Seguidores: "+followed_by))



        pages = (len(self.view_profile['images'])/8)+1
        if(page > pages):
            page = pages
        print pages
        x = 230
        y = 120

        if(page > 1):
            self.back = Button(text = "Atras", command = lambda: self.DrawOwnProfile(page-1)) #Aca deberiamos pasar algun Id de post o lo que sea
            self.objects.append(self.canvas.create_window(int(560*radio), int(375*radio), window = self.back))
        if page < pages:
            self.next = Button(text = "Siguiente", command = lambda: self.DrawOwnProfile(page+1))
            self.objects.append(self.canvas.create_window(int(650*radio), int(375*radio), window = self.next))

        #Imagen por imagen
        for i in range(1, 9):
            if(i+8*(page-1) >= len(self.view_profile['images'])):
                break
            print "img/"+self.view_profile['images'][i+8*(page-1)]
            self.view_profile_im.append(Image.open("img/"+self.view_profile['images'][i+8*(page-1)]))
            self.view_profile_im[i] = self.view_profile_im[i].resize((int(100*radio) , int(100*radio)), Image.ANTIALIAS)
            self.view_profile_tkimg.append(ImageTk.PhotoImage(self.view_profile_im[i]))
            self.objects.append(self.canvas.create_image(int(x*radio), int(y*radio), image=self.view_profile_tkimg[i], anchor = NW))
            x += 110
            if(i % 4 == 0):
                x = 230
                y += 110

    


    def DrawOtherProfile(self, profile, page):
        if(profile == OUR_PROFILE_ID):
            self.DrawOwnProfile(1)
            return
        if(page == 1):
            self.ParseOtherProfile(profile)
            self.ParseOtherRecentPhotos(profile)
        self.ClearContent()

        #Separador horizontal
        self.objects.append(self.canvas.create_line(int(200*radio), int(100*radio), int(700*radio), int(100*radio)))

        #Foto de perfil
        self.view_profile_im = []
        self.view_profile_tkimg = []
        print "img/"+self.view_profile['picture']
        self.view_profile_im.append(Image.open("img/"+self.view_profile['picture']))
        self.view_profile_im[0] = self.view_profile_im[0].resize((int(80*radio) , int(80*radio)), Image.ANTIALIAS)
        self.view_profile_tkimg.append(ImageTk.PhotoImage(self.view_profile_im[0]))
        self.objects.append(self.canvas.create_image(int(210*radio), int(10*radio), image=self.view_profile_tkimg[0], anchor = NW))
        username = self.view_profile['username']
        bio = self.view_profile['bio']
        website = self.view_profile['website']
        follows = self.view_profile['follows']
        followed_by = self.view_profile['followed_by']
        self.objects.append(self.canvas.create_text(int(450*radio), int(25*radio), text = username))
        self.objects.append(self.canvas.create_text(int(450*radio), int(45*radio), text = bio, width = int(300*radio)))
        self.objects.append(self.canvas.create_text(int(450*radio), int(65*radio), text = website))
        self.objects.append(self.canvas.create_text(int(650*radio), int(35*radio), text = "Siguiendo: "+follows))
        self.objects.append(self.canvas.create_text(int(650*radio), int(55*radio), text = "Seguidores: "+followed_by))



        pages = (len(self.view_profile['images'])/8)+1
        if(page > pages):
            page = pages
        print pages
        x = 230
        y = 120
        print self.view_profile['is_followed'] == 'follows'
        if self.view_profile['is_followed'] == 'follows':
            self.follow_button = Button(text = "Unfollow", command = lambda:self.OnFollowButton(self.view_profile['profile_id']))
        elif self.view_profile['is_followed'] == 'requested':
            self.follow_button = Button(text = "Unrequest", command = lambda: self.OnFollowButton(self.view_profile['profile_id']))
        else:
            self.follow_button = Button(text = "Follow", command = lambda: self.OnFollowButton(self.view_profile['profile_id']))
        self.objects.append(self.canvas.create_window(int(600*radio), int(80*radio), window = self.follow_button))
        if(page > 1):
            self.back = Button(text = "Atras", command = lambda: self.DrawOtherProfile(profile, page-1)) #Aca deberiamos pasar algun Id de post o lo que sea
            self.objects.append(self.canvas.create_window(int(560*radio), int(375*radio), window = self.back))
        if page < pages:
            self.next = Button(text = "Siguiente", command = lambda: self.DrawOtherProfile(profile, page+1))
            self.objects.append(self.canvas.create_window(int(650*radio), int(375*radio), window = self.next))

        #Imagen por imagen
        for i in range(1, 9):
            if(i+8*(page-1) >= len(self.view_profile['images'])):
                break
            print "img/"+self.view_profile['images'][i+8*(page-1)]
            self.view_profile_im.append(Image.open("img/"+self.view_profile['images'][i+8*(page-1)]))
            self.view_profile_im[i] = self.view_profile_im[i].resize((int(100*radio) , int(100*radio)), Image.ANTIALIAS)
            self.view_profile_tkimg.append(ImageTk.PhotoImage(self.view_profile_im[i]))
            self.objects.append(self.canvas.create_image(int(x*radio), int(y*radio), image=self.view_profile_tkimg[i], anchor = NW))
            x += 110
            if(i % 4 == 0):
                x = 230
                y += 110

    def DrawPost(self, post_id):
        print "DRAW:"+str(post_id)+"/"+str(len(self.feed['images']))
        if(post_id < 0 or post_id >= len(self.feed['images'])):
            return
        current_post = post_id
        self.ClearContent()

        #Esto ya es una publicacion!!
        self.objects.append(self.canvas.create_text(int(450*radio), int(15*radio), text = "Publicaciones Recientes"))
        print "img/"+self.feed['image_file'][post_id]
        self.im = Image.open("img/"+self.feed['image_file'][post_id])
        self.im = self.im.resize((int(150*radio), int(150*radio)), Image.ANTIALIAS)
        self.tkimg = ImageTk.PhotoImage(self.im)
        print self.feed['userid'][post_id] + " (total"+str(len(self.feed['userid']))+")"
        self.imgbtn = Button(width = int(5*radio), text = "Ver perfil", command =  lambda:self.DrawOtherProfile(self.feed['userid'][post_id], 1))
        self.objects.append(self.canvas.create_window(int(290*radio), int(120*radio), window = self.imgbtn))
        self.objects.append(self.canvas.create_text(int(450*radio), int(42*radio), text=self.feed['username'][post_id]))
        self.objects.append(self.canvas.create_image(int(375*radio), int(50*radio), image=self.tkimg, anchor = NW, tags = "bg_img"))
        #self.objects.append(self.canvas.create_text(450, 150, text = "foto persona"))
        #self.objects.append(self.canvas.create_line(350, 50, 550, 50))
        #self.objects.append(self.canvas.create_line(350, 250, 550, 250))
        #self.objects.append(self.canvas.create_line(550, 50, 550, 250))
        #self.objects.append(self.canvas.create_line(350, 50, 350, 250))
        comments = ""
        for j in xrange(0, len(self.feed['comments'][post_id])):
            comments += self.feed['comments'][post_id][j][1]+": "+self.feed['comments'][post_id][j][0]+"\n"

        self.cmt = Label(text = comments, width = int(50*radio), height = int(7*radio), bg = "white", wraplength = int(350*radio), relief = RIDGE)
        self.objects.append(self.canvas.create_window(int(450*radio), int(300*radio), window = self.cmt))
        self.caption = Label(text = self.feed['captions'][post_id], width = int(50*radio), height = int(2*radio), wraplength = int(350*radio))
        self.objects.append(self.canvas.create_window(int(450*radio), int(210*radio), window = self.caption))
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

    def ClearAll(self):
        self.canvas.delete('all')

    def Update(self):
        self.ClearAll()
        temp = Label(text = "Cargando...")
        self.objects.append(self.canvas.create_window(int(350*radio), int(200*radio), window=temp))
        self.ParseProfile()
        self.ParseFeed()
        self.DrawSideBar()
        self.DrawPost(0)

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
        print request
        response = urllib2.urlopen(request)
        print response
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
