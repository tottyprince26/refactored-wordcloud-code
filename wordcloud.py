"""
refactored wordcloud code
author: Austin_Salguero
"""
from io import BytesIO
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud,ImageColorGenerator
join = list ()
npag = list ()
lbls = list ()
nmbrs = list ()
labels = list ()
numbers = list ()
class user:
  def _init_(self, join, npag, lbls, nmbrs, labels, numbers):
    self.join = join
    self.npag = npag
    self.lbls = lbls
    self.nmbrs = nmbrs
    self.labels = labels 
    self.numbers = numbers 
print ("PROYECTO:")
print ("NUBE DE PALABRAS CON ETIQUETAS DE USUARIOS EN STACK OVERFLOW ESPAÑOL")
print ("*AUSTIN ADRIAN SALGUERO ZAMBRANO")
id = input("\n\nDigite el ID del usuario para mostrar la nube de palabras: \n")
print("\n")
id = id.strip()
if id.isdigit() is False:
    print ("\n\nError 404 Not Found: Usuario no encontrado.")
else:
    url = 'https://es.stackoverflow.com/users/' + id + "/?tab=tags"
    page = requests.get (url)
    if page.status_code == 404:
        print ("\n\nError",page.status_code,"Not Found: Usuario no encontrado.")
    else:
        print ("\n\nUsuario Encontrado: \n", url)
        soup = BeautifulSoup (page.content, "html.parser")
        for f in soup.find_all ('a', class_='m0 badge-tag js-rep-box-next-badge'):
            join.append (f.text)
        for a in soup.find_all ('a', class_='s-pagination--item js-pagination-item'):
            npag.append (a.text)
        if len (npag) == 0:
            for c in soup.find_all ('a', class_='post-tag'):
                lbls.append (c.text)
            if int (len (join)) == 0 and len (lbls) != 0:
                lbls.pop(0)
            for d in soup.find_all ('div', class_='answer-votes'):
                nmbrs.append (d.text)
            CONT=0
            for g in nmbrs:
                if int (len (nmbrs[CONT])) > 1:
                    if nmbrs[CONT][-1] == 'k':
                        nmbrs[CONT] = nmbrs[CONT][:-1]
                        nmbrs[CONT] = nmbrs[CONT]+'000'
                CONT=CONT+1
            COUNTER=0
            for e in nmbrs:
                if int (e) > 0:
                    numbers.append (int (e))
                    labels.append (lbls[COUNTER])
                COUNTER=COUNTER+1
            lbls.clear ()
            nmbrs.clear ()
        else:
            print ("\n")
            for b in range (int (npag [int (len (npag))-2])):
                num = b+1
                url = 'https://es.stackoverflow.com/users/' + id + '/?tab=tags&sort=votes&page=' + str (num)
                page = requests.get (url)
                soup = BeautifulSoup (page.content, 'html.parser')
                for c in soup.find_all ('a', class_='post-tag'):
                    lbls.append (c.text)
                if int (len (join)) == 0:
                    lbls.pop(0)
                for d in soup.find_all ('div', class_='answer-votes'):
                    nmbrs.append (d.text)
                CONT=0
                for g in nmbrs:
                    if int (len (nmbrs[CONT])) > 1:
                        if nmbrs[CONT][-1] == 'k':
                            nmbrs[CONT] = nmbrs[CONT][:-1]
                            nmbrs[CONT] = nmbrs[CONT]+'000'
                    CONT=CONT+1
                COUNTER=0
                for e in nmbrs:
                    if int (e) > 0:
                        numbers.append (int (e))
                        labels.append (lbls[COUNTER])
                    COUNTER=COUNTER+1
                lbls.clear ()
                nmbrs.clear ()
        print ('\n')
        if len (labels) == 0:
            print ("\nEste usuario no tiene etiquetas")
        else:
            URL = "https://image.shutterstock.com/image-photo/image-260nw-593485994.jpg"
            CLR = "white"
            CW = 0
            #formato de la nube de palabras
            print ("\n")
            dic = dict (zip (tuple (labels), tuple (numbers)))
            response = requests.get (URL)
            creation = np.asarray (Image.open (BytesIO (response.content)))
            wordcloud = WordCloud (background_color = CLR, mask=creation,
                                    contour_width = CW, max_words=1000).generate_from_frequencies (dic)
            colors = ImageColorGenerator (creation)
            wordcloud.recolor (color_func = colors)
            plt.figure (figsize = (15, 8))
            plt.imshow (wordcloud)
            plt.axis ("off")
            plt.show ()
            plt.close ()
