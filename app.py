import tkinter as tk
from tkinter import scrolledtext
from rdflib import Graph, Literal, URIRef

# Cargar el archivo .nt en un grafo RDF
g = Graph()
g.parse("./mapping/output.nt", format="nt")

publication_hosts = []
Author_result = []
Topic_result = []

# Crear la ventana principal
window = tk.Tk()
window.title("Consulta de publicaciones")


# Crear una etiqueta y un cuadro de texto para ingresar el valor de pubHost
label_pubHost = tk.Label(window, text="Ingrese pubHost:")
label_pubHost.pack()

pubHost_entry = tk.Entry(window)
pubHost_entry.pack()

# Crear una etiqueta y un cuadro de texto para ingresar el nombre del autor
label_author = tk.Label(window, text="Ingrese el nombre del autor:")
label_author.pack()

author_forename_entry = tk.Entry(window)
author_forename_entry.pack()

# Crear una etiqueta y un cuadro de texto para ingresar el nombre del autor
label_topic = tk.Label(window, text="Ingrese el numero de Topic:")
label_topic.pack()

topic_entry = tk.Entry(window)
topic_entry.pack()

def getPublicationHost(pubHost):
    global publication_hosts
    query = f"""
    SELECT ?title 
    WHERE {{ 
       ?id <http://www.semanticweb.org/IA_Assessment2#PublicationHost> "{pubHost}".
       ?id <http://www.semanticweb.org/IA_Assessment2#Title> ?title .
    }}
    """
    results = g.query(query)
    publication_hosts = [str(result["title"]) for result in results]
    show_results()

def getPapersByAuthor(forename):
    global Author_result
    query = f"""
    SELECT ?title
    WHERE {{ 
       ?idauthor <http://www.semanticweb.org/IA_Assessment2#Forename>  "{forename}".
       ?idpaper <http://www.semanticweb.org/IA_Assessment2#is_written_by_author> ?idauthor .
       ?idpaper <http://www.semanticweb.org/IA_Assessment2#Title> ?title .
    }}
    """
    results = g.query(query)
    Author_result = [str(result["title"]) for result in results]
    show_results()

def getPapersTopic(result):
    global Topic_result
    query = f"""
    SELECT DISTINCT ?Topic{result} ?title
    WHERE {{
          <http://www.semanticweb.org/IA_Assessment2#Results/{result}> <http://www.semanticweb.org/IA_Assessment2#belongs_to_paper> ?y .
          ?y <http://www.semanticweb.org/IA_Assessment2#Title> ?title
    }}
    """
    results = g.query(query)
    Topic_result = [str(result["title"]) for result in results]
    show_results()


def show_results():
    result_text.delete(1.0, tk.END)  # Limpiar el cuadro de texto
    result_text.insert(tk.END, "Publications by Host:\n")
    for paper in publication_hosts:
        result_text.insert(tk.END, f"{paper}\n")
    
    result_text.insert(tk.END, "\nPublications by Author:\n")
    for paper in Author_result:
        result_text.insert(tk.END, f"{paper}\n")

    result_text.insert(tk.END, "\nPapers by Topic:\n")
    for paper in Topic_result:
        result_text.insert(tk.END, f"{paper}\n")


# Crear un botón para realizar la consulta
query_button = tk.Button(window, text="Realizar consulta", command=lambda: (getPublicationHost(pubHost_entry.get()), getPapersByAuthor(author_forename_entry.get()), getPapersTopic(topic_entry.get())))
query_button.pack()

# Crear un cuadro de texto desplazable para mostrar los resultados
result_text = scrolledtext.ScrolledText(window, width=40, height=10)
result_text.pack(fill=tk.BOTH, expand=True)
result_text.pack_propagate(0)

# Ejecutar la ventana principal
window.mainloop()
