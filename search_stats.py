import requests
import json

from bs4 import BeautifulSoup
import json
import os
troops = {}

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------


def lista_tropas(name, troop, url):
    list_temp = []
    dict = {}

    # Realizar solicitud HTTP GET a la página
    response = requests.get(url)

    # Crear objeto BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(response.text, "html.parser")

    tabla_tropas = soup.find(string=troop).parent.parent.parent
    nombre_tropas = tabla_tropas.find_all("a")

    for i in nombre_tropas:
        tropa = {}
        if (i.text != ""):
            tropa["name"] = i.text
            tropa["url"] = i["href"]
            tropa["stats"] = buscar_estadisticas(i["href"])
            # dict[i.text] = tropa
            json_data = json.dumps(tropa)
            new_name = modificar_nombre_tropa_para_json(i.text)

            # with open(new_name + '.json', 'w') as archivo:
            #   archivo.write(json_data)


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
def modificar_nombre_tropa_para_json(nombre_tropa):
    new_name = nombre_tropa.replace(" ", "").lower()
    if "." in new_name:
        new_name = new_name.replace(".", "_")
    if "-" in new_name:
        new_name = new_name.replace("-", "_")
    
    return new_name


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------


def modificar_json(json_data, valor_a_modificar, valor_modificado):
    temp_dict = json.loads(json_data)
    for key, value in temp_dict.items():
        if valor_a_modificar in value:
            index = value.index(valor_a_modificar)
            value[index] = valor_modificado

    return json.dumps(temp_dict)
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------


def modificar_dict(dict_data, valor_a_modificar, valor_modificado):
    for key, value in dict_data.items():
        for i in value:
            if i == valor_a_modificar:
                index = value.index(valor_a_modificar)
                value[index] = {valor_a_modificar: valor_modificado}
                print(dict_data)

                return


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------


def buscar_estadisticas(url_data):
    # URL de la página del Rey Bárbaro en Fandom
    url = "https://clashofclans.fandom.com/" + url_data

    # Realizar solicitud HTTP GET a la página
    response = requests.get(url)

    # Crear objeto BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(response.text, "html.parser")

    etiqueta = soup.find(string="Level")
    etiqueta2 = soup.find(string="Level ")
    etiqueta3 = soup.find(string=" Level")
    etiqueta4 = soup.find(string=" Level ")
    etiqueta5 = soup.find(string="Level* ")
    if etiqueta != None:
        etiqueta_padre = etiqueta.parent
        return buscar(etiqueta_padre, url)

    elif etiqueta2 != None:
        etiqueta_padre = etiqueta2.parent
        return buscar(etiqueta_padre, url)

    elif etiqueta3 != None:
        etiqueta_padre = etiqueta3.parent
        return buscar(etiqueta_padre, url)

    elif etiqueta4 != None:
        etiqueta_padre = etiqueta4.parent
        return buscar(etiqueta_padre, url)

    elif etiqueta5 != None:
        etiqueta_padre = etiqueta5.parent
        return buscar(etiqueta_padre, url)

    else:
        return

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------


def buscar(etiqueta_padre, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tabla = etiqueta_padre.parent
    clase = ""
    clase_tabla = tabla.parent.parent.get('class')

    for i in clase_tabla:
        clase += " " + i

    table = soup.find("table", class_=clase.strip())

    # print(len(table))

    # Crear un diccionario para almacenar las estadísticas
    stats = {}

    i = 0
    y = 0
    stats_update = {}

    for valor in table.find_all("td"):
        title = table.find_all("th")

        if valor != "" and title != "":
            # print(title[i].text)
            # print(valor.text)

            stat_name = title[i].text.strip()
            stat_value = valor.text.strip()

            stats[stat_name] = stat_value

            i += 1

            if i == len(title):

                stats_update[y] = stats
                y += 1
                stats = {}
                i = 0

    return stats_update

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def modificar_nombres_img():
    

# Directorio donde se encuentran las imágenes
    input_directory = "/Users/Juan Felipe/pruebas_json/app/src/main/res/drawable/"

# Obtener la lista de archivos en el directorio
    file_list = os.listdir(input_directory)

# Iterar a través de los archivos
    for filename in file_list:
    # Verificar si el archivo es una imagen (puedes agregar más extensiones si es necesario)
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif",".webp")):
        # Construir el nuevo nombre en minúsculas
            new_filename = modificar_nombre_tropa_para_json(filename)
            if("_webp" in new_filename):
                new_filename = new_filename.replace("_webp",".webp" )
                new_filename = new_filename.replace("_","" )
                new_filename = new_filename.replace("info","" )
        
        # Rutas de archivo originales y nuevas
            old_path = os.path.join(input_directory, filename)
            new_path = os.path.join(input_directory, new_filename)
        
        # Renombrar el archivo
            os.rename(old_path, new_path)
        
            print(f"Archivo {filename} renombrado a {new_filename}")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
"""
lista_tropas("Elixir Troops", "Barbarian",
             "https://clashofclans.fandom.com/wiki/Category:Troops")


lista_tropas("Temporary Troops", "Ice Wizard",
             "https://clashofclans.fandom.com/wiki/Category:Troops")

lista_tropas("Dark Elixir Troops", "Minion",
             "https://clashofclans.fandom.com/wiki/Category:Troops")


lista_tropas("Super Troops", "Super Barbarian",
             "https://clashofclans.fandom.com/wiki/Category:Troops")
lista_tropas("Builder Base", "Raged Barbarian",
             "https://clashofclans.fandom.com/wiki/Category:Troops")
"""
modificar_nombres_img()