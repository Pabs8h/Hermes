import json
import os
import pytesseract
from django.http import HttpResponse
from django.shortcuts import render, redirect
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
from pymongo import MongoClient
from bson import ObjectId
import datetime
from .forms import Guardar
# Create your views here.

#def prueba(request):

resp2 = None
nombre = ""
fecha = ""


def creaciontexto(request):
    #if request.method =='POST':
    direccion = os.path.join(BASE_DIR, 'analisis\data\dummy.pdf')
    dirTxt = 'analisis\data\info2.txt'
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
    #paginas =  convert_from_path(direccion,500)

    base ='analisis\data\\'
    contador=3
    #     for pagina in paginas:
    #         nombredoc='pagina_'+str(contador)+'.jpg'
    #         nombredoc =os.path.join(BASE_DIR, base ,nombredoc)
    #         pagina.save(nombredoc,'JPEG')
    #         contador = contador +1
         #ESTO TIENE QUE SER OTRO METODO
    limite =contador -1
    f=open(os.path.join(BASE_DIR,'analisis\data\info2.txt'),'a',encoding='utf-8')
    for i in range(1,limite +1):
        nombredoc='pagina_'+str(i)+'.jpg'
        nombredoc=os.path.join(BASE_DIR, base ,nombredoc)
        contenido=str(((pytesseract.image_to_string(Image.open(nombredoc)))))
        contenido = contenido.replace('-\n','')
        f.write(contenido)
    f.close()
    return render(request,"analisis/creacion.html",{'direc':dirTxt})

def analizar(request):
    global resp2
    if request.method == 'GET':
        form = Guardar()
        autenticador= IAMAuthenticator('Iy9P79mRg9q5zFqpKmpXydkbizYEyAs8w7AxXvmxg6kZ')
        natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2020-08-01',
        authenticator=autenticador)
        f=open(os.path.join(BASE_DIR,'analisis\data\info.txt'),'r', encoding='utf-8')
        contenido= f.read()
        #print(contenido)
        f.close()
        natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/17bf7417-a159-4992-8526-751d92eb4f9c')
        response = natural_language_understanding.analyze(
            text=contenido,
            features=Features(categories=CategoriesOptions(limit=10),concepts=ConceptsOptions(limit=10),entities=EntitiesOptions(limit=10),keywords=KeywordsOptions(sentiment=True,emotion=True,limit=10))).get_result()
        #resp = json.dumps()
        # print(response)
        resp2 = dictresponse(response)
        return render(request, "analisis/analizar.html", {"resp2": resp2, "form": form})
    else:
        return documentoPost(request)

def dictresponse(resp):
    finResp = {
        "People":[],
        "Organizations":[],
        "Cities":[],
        "Keywords":[]
    }
    for ent in resp["entities"]:
        if ent["type"] == "Person":
            finResp["People"].append(ent)
        elif ent["type"] == "Organization":
            finResp["Organizations"].append(ent)
        elif ent["type"] == "Location":
            finResp["Cities"].append(ent["text"])
    for keyw in resp["keywords"]:
        finResp["Keywords"].append(keyw["text"])

    # print(finResp)
    return finResp

def guardarDoc(nombre, doc):
    client = MongoClient('mongodb://3.87.218.6:27017/')
    db = client["testPMC"]
    myCol = db["test1"]
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    documentoFinal = {'nombre':nombre, 'documento':doc, 'fecha': fecha}
    myCol.insert_one(documentoFinal)


def documentosActuales(request):
    client = MongoClient('mongodb://3.87.218.6:27017/')
    db = client["testPMC"]
    col = db["test1"]
    cant = col.count()
    results = col.find({})
    if cant == 0:
        results = ""
    return render(request, "analisis/documentos.html", {"results": results})

def documentoPost(request):
    global resp2
    if request.method == 'POST':
        form = Guardar(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            guardarDoc(nombre, resp2)
    form = Guardar()
    return redirect('documentos')

def documentoActual(request, pk):
    client = MongoClient('mongodb://3.87.218.6:27017/')
    db = client["testPMC"]
    col = db["test1"]
    result = col.find_one({'_id': ObjectId(pk)})
    print (result)
    return render(request, "analisis/documentoA.html", {'resp2': result})