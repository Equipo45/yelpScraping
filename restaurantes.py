from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import os
import pandas as pd

s=HTMLSession()
url_base='https://www.yelp.es/search?find_desc=Restaurantes%20y%20bares&find_loc=Madrid&ns=11&start='
def getData(url_base,paginas):
    lista=[]
    for pagina in range(paginas):
        url=url_base+str(pagina*10)
        r=s.get(url)
        r.html.render(sleep=1)
    
        soup=bs(r.html.html,'html.parser')


        restaurantes=soup.find_all('li',{'class':'border-color--default__09f24__R1nRO'})

        for restaurante in restaurantes:

            try:
                name=restaurante.find('h4',{'class':'heading--h4__09f24__2ijYq alternate__09f24__39r7c'}).text.strip()
            except:
                name='Restaurante no disponible'

            try:
                reviews=restaurante.find('div',{'class':'attribute__09f24__3znwq display--inline-block__09f24__FsgS4 border-color--default__09f24__R1nRO'}).text.strip()
            except:
                reviews='Reviews no disponible'

            try:
                dinero=restaurante.find('span',{'class':'text__09f24__2tZKC priceRange__09f24__2O6le text-color--black-extra-light__09f24__38DtK text-align--left__09f24__3Drs0 text-bullet--after__09f24__1MWoX'}).text.strip()
            except:
                dinero='Dinero no disponible'

            try:
                link='yelp.es'+restaurante.find('a',{'class':'link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95'})['href']
            except:
                link='Link no disponible'


            if name=='Restaurante no disponible':
                pass
            else:
                dict={
                    'Nombre':name,'Reviews':reviews,'Dinero':dinero,'Link':link
                }

                lista.append(dict)
            
            
    
    
    
    return lista
        
    
    
def dataframe(lista):
    df=pd.DataFrame(lista) 
    df.to_csv('Restaurantes.csv',index=False)
            
dataframe(getData(url_base,10))
