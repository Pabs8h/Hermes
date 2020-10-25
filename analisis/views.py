import json
import os
import pytesseract
from django.http import HttpResponse
from django.shortcuts import render
from hermes.settings import BASE_DIR
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import (CategoriesOptions,
                                                          ConceptsOptions,
                                                          EntitiesOptions,
                                                          Features,
                                                          KeywordsOptions)
from pdf2image import convert_from_path
from PIL import Image

# Create your views here.


def prueba(request):

        

def creaciontexto(request):
    if request.method =='POST':
        direccion = os.path.join(BASE_DIR, 'analisis\data\dummy.pdf')
        paginas =  convert_from_path(direccion,500)
        
        base ='analisis\data\\'
        contador=1
        for pagina in paginas:
            nombredoc='pagina_'+str(contador)+'.jpg'
            nombredoc =os.path.join(BASE_DIR, base ,nombredoc)
            pagina.save(nombredoc,'JPEG')
            contador = contador +1
        #ESTO TIENE QUE SER OTRO METODO 
        limite =contador -1
        f=open(os.path.join(BASE_DIR,'analisis\data\info.txt'),'a')
        for i in range(1,limite +1):
            nombredoc='pagina_'+str(i)+'.jpg'
            nombredoc=os.path.join(BASE_DIR, base ,nombredoc)
            contenido=str(((pytesseract.image_to_string(Image.open(nombredoc)))))
            contenido = contenido.replace('-\n','')
            f.write(contenido)
        f.close()
        return HttpResponse(direccion)

def analizar(request):
    autenticador= IAMAuthenticator('Iy9P79mRg9q5zFqpKmpXydkbizYEyAs8w7AxXvmxg6kZ')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=autenticador)
    f=open(os.path.join(BASE_DIR,'analisis\data\info.txt'),'r')
    contenido= f.read()
    f.close()
    natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/17bf7417-a159-4992-8526-751d92eb4f9c')
    response = natural_language_understanding.analyze(
    text=contenido,
    features=Features(categories=CategoriesOptions(limit=3),concepts=ConceptsOptions(limit=3),entities=EntitiesOptions(sentiment=True,limit=1),keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2))).get_result()

    print(json.dumps(response, indent=2))
    return HttpResponse('uwu')
