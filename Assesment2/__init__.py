import requests
import os
import nltk
import xml.etree.ElementTree as ET
import json
from bs4 import BeautifulSoup
import re
nltk.download('brown')
nltk.download('punkt')



# Construir la URL completa
# En caso de estar corriendolo en local sustituir grobid por localhost
grobid_url = "http://localhost:8070/api/processFulltextDocument"

params = {
    #'input': 'processFulltextDocument',
    'consolidateHeader': '1',
    'output':'/home/alvaro/Documentos/IA/IAOS_Assessment2/Assesment2/resources'
    #'consolidatecitations': '1',
    #'includeRawcitations': '0',
    #'teiCoordinates': '0'
}

data={}
data["consolidateHeader"] = "1"

# Definir la carpeta que contiene los archivos PDF
#folder_path = "./Assesment2/resources"
folder_path ="./PapersIA"
#folder_path ="/home/alvaro/Documentos/res/"

# Obtener la lista de archivos en la carpeta
file_list = os.listdir(folder_path)

text = ""
num_images_list = []
all_data = []
i=1
ID_Paper=1
# Definir la carpeta que contiene los archivos PDF
for filename in file_list:
    if filename.endswith(".pdf"):
        # Construir la ruta completa del archivo
        filepath = os.path.join(folder_path, filename)

        # Leer el contenido del archivo
        with open(filepath, 'rb') as pdf_file:
            file_content = pdf_file.read()

        # Enviar la solicitud a Grobid
        response = requests.post(grobid_url, files={'input': file_content})#params=params
        # Procesar la respuesta
        if response.status_code == 200:
            # La respuesta es un documento TEI en XML
            texto = response.content
            root = ET.fromstring(texto)
            soup = BeautifulSoup(texto, 'lxml')
            pdf_data = {}

            pdf_data["ID_Paper"] = ID_Paper
            #--------------Titulo-------------
            #print("\nTítulo:")
            title_txt="None"
            title = root.find('.//{http://www.tei-c.org/ns/1.0}title[@type="main"]')
            if title is not None: title_txt=title.text
            pdf_data["Title"] = title_txt

            #--------------Abstract-------------
            #print("\nAbstract:")
            abstract_txt="None"
            abstract = root.find('.//{http://www.tei-c.org/ns/1.0}profileDesc/{http://www.tei-c.org/ns/1.0}abstract/{http://www.tei-c.org/ns/1.0}div/{http://www.tei-c.org/ns/1.0}p')
            if abstract is not None: abstract_txt=abstract.text
            data={"Abstract":abstract_txt}
            pdf_data["Abstract"] = abstract_txt

            #--------------Author-------------
            #print("\nAutores:")
            authors=root.findall('.//{http://www.tei-c.org/ns/1.0}teiHeader/{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}sourceDesc/{http://www.tei-c.org/ns/1.0}biblStruct/{http://www.tei-c.org/ns/1.0}analytic/{http://www.tei-c.org/ns/1.0}author')
            authors_data=[]
            affs_data=[]
            ID_Author=1
            author_data_ID=[]
            for author in authors:
                forename_text="None"
                surname_text="None"
                affiliation_text="None"
                forename=author.find('.//{http://www.tei-c.org/ns/1.0}persName/{http://www.tei-c.org/ns/1.0}forename[@type="first"]')
                if forename is not None: forename_text=forename.text
                surname=author.find('.//{http://www.tei-c.org/ns/1.0}persName/{http://www.tei-c.org/ns/1.0}surname')
                if surname is not None: surname_text=surname.text
                # affiliations=author.findall('.//{http://www.tei-c.org/ns/1.0}affiliation/{http://www.tei-c.org/ns/1.0}orgName')
                # if affiliations is not None:
                #     for affiliation in affiliations:
                #         if affiliation is not None: affiliation_text=affiliation.text
                #         aff_data = {"Organization Name": affiliation_text}
                #         affs_data.append(aff_data)
                # affs_data=[]
                author_data = {"Forename": forename_text, "Surname": surname_text}
                authors_data.append(author_data)
            pdf_data["Author"] = authors_data


            #print(author_data_ID)

            #--------------KeyWords-------------
            #print("\nKeywords:")
            keywords = root.findall('.//{http://www.tei-c.org/ns/1.0}keywords/{http://www.tei-c.org/ns/1.0}term')
            keywords_data = []
            for keyword in keywords:
                keyword_txt="None"
                if keyword is not None: keyword_txt=keyword.text
                #keyword_data = {"KeyWords":keyword_txt}
                keywords_data.append(keyword_txt)
            pdf_data["KeyWords"] = keywords_data

            #--------------DOI-------------
            doi_txt="None"
            doi=root.find('.//{http://www.tei-c.org/ns/1.0}idno[@type="DOI"]')
            if doi is not None: doi_txt=doi.text
            data={"DOI":abstract_txt}
            doi_struct="https://doi.org/"+doi_txt
            pdf_data["DOI"] = doi_struct


        all_data.append(pdf_data)
    ID_Paper=ID_Paper+1
    print(i)
    i=i+1
json_data = json.dumps(all_data, indent=4)
with open('datos.json', 'w') as f:
    f.write(json_data)
    print("JSON HECHO")




            
