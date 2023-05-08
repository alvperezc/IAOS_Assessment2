import requests
import os
import nltk
import xml.etree.ElementTree as ET
import json
nltk.download('brown')
nltk.download('punkt')



# Construir la URL completa
# En caso de estar corriendolo en local sustituir grobid por localhost
grobid_url = "http://localhost:8070/api/processFulltextDocument"

params = {
    'input': 'processFulltextDocument',
    'consolidateHeader': '1',
    'consolidateCitations': '1',
    'includeRawCitations': '0',
    'teiCoordinates': '0'
}

# Definir la carpeta que contiene los archivos PDF
folder_path = "./Assesment2/resources"

# Obtener la lista de archivos en la carpeta
file_list = os.listdir(folder_path)

text = ""
num_images_list = []
all_data = []
i=1

# Definir la carpeta que contiene los archivos PDF
for filename in file_list:
    if filename.endswith(".pdf"):
        # Construir la ruta completa del archivo
        filepath = os.path.join(folder_path, filename)

        # Leer el contenido del archivo
        with open(filepath, 'rb') as pdf_file:
            file_content = pdf_file.read()

        # Enviar la solicitud a Grobid
        response = requests.post(grobid_url, files={'input': file_content}, params=params)
        # Procesar la respuesta
        if response.status_code == 200:
            # La respuesta es un documento TEI en XML
            texto = response.content
            root = ET.fromstring(texto)
            pdf_data = {}
            
            #--------------Titulo-------------
            #print("\nTítulo:")
            title_txt="None"
            title = root.find('.//{http://www.tei-c.org/ns/1.0}title[@type="main"]')
            if title is not None: title_txt=title.text
            pdf_data["Title"] = title_txt
            #all_data.append(pdf_data)
            #print("\t",title_txt)

            #--------------Abstract-------------
            #print("\nAbstract:")
            abstract_txt="None"
            abstract = root.find('.//{http://www.tei-c.org/ns/1.0}profileDesc/{http://www.tei-c.org/ns/1.0}abstract/{http://www.tei-c.org/ns/1.0}div/{http://www.tei-c.org/ns/1.0}p')
            if abstract is not None: abstract_txt=abstract.text
            data={"Abstract":abstract_txt}
            pdf_data["Abstract"] = abstract_txt
            #all_data.append(pdf_data)
            #print(abstract_txt)

            #--------------Author-------------
            #print("\nAutores:")
            authors=root.findall('.//{http://www.tei-c.org/ns/1.0}teiHeader/{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}sourceDesc/{http://www.tei-c.org/ns/1.0}biblStruct/{http://www.tei-c.org/ns/1.0}analytic/{http://www.tei-c.org/ns/1.0}author/{http://www.tei-c.org/ns/1.0}persName')
            authors_data=[]
            for author in authors:
                forename_text="None"
                surname_text="None"
                forename=author.find('.//{http://www.tei-c.org/ns/1.0}forename[@type="first"]')
                if forename is not None: forename_text=forename.text
                surname=author.find('.//{http://www.tei-c.org/ns/1.0}surname')
                if surname is not None: surname_text=surname.text
                author_data = {"Forename": forename_text, "Surname": surname_text}
                authors_data.append(author_data)
            pdf_data["Author"] = authors_data
            #all_data.append(pdf_data)
                #print("\t",forename_text,surname_text)
            #--------------KeyWords-------------
            #print("\nKeywords:")
            keywords = root.findall('.//{http://www.tei-c.org/ns/1.0}keywords/{http://www.tei-c.org/ns/1.0}term')
            keywords_data = []
            for keyword in keywords:
                keyword_txt="None"
                if keyword is not None: keyword_txt=keyword.text
                keyword_data = {"KeyWords":keyword_txt}
                keywords_data.append(keyword_data)
            pdf_data["KeyWords"] = keywords_data
            #all_data.append(pdf_data)
                #print("\t",keyword_txt)

            #--------------Published Date-------------
            #print("\nPublisher:") 
            publisherStmt = root.find('.//{http://www.tei-c.org/ns/1.0}publicationStmt')
            publishers_data = []
            if publisherStmt is not None:
                date_txt="None"
                publisher_txt="None"
                date=publisherStmt.find('.//{http://www.tei-c.org/ns/1.0}date[@type="published"]')
                if date is not None: date_txt=date.text
                publisher=publisherStmt.find('.//{http://www.tei-c.org/ns/1.0}publisher')
                if publisher is not None: publisher_txt=publisher.text
                publisher_data = {"Publisher": publisher_txt, "Date": date_txt}
                publishers_data.append(publisher_data)



                publisher = root.find('./availability[1]')
                print(publisher)



            pdf_data["Publisher"] = publishers_data
        all_data.append(pdf_data)
    print(i)
    i=i+1
#json_data = json.dumps(all_data, indent=4)
#with open('datos.json', 'w') as f:
    #f.write(json_data)




            
