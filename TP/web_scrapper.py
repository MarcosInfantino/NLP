import requests
from bs4 import BeautifulSoup
from config import CONFIG


USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

class Bing:
	def obtener_resultados(self, termino_busqueda):
		url_bing = "https://www.bing.com/search?q={}".format(termino_busqueda)
		respuesta = requests.get(url_bing, headers = USER_AGENT)
		respuesta.raise_for_status()
		return respuesta.text

	def procesar_resultados(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		resultados_encontrados = []
		bloque = soup.find_all("div", class_="b_title")
		for resultado in bloque:
			titulo = resultado.find("h2")
			link = resultado.find('a')['href']
			resultados_encontrados.append((titulo, link))
		return resultados_encontrados

class Google:
	def obtener_resultados(self, termino_busqueda):
		numero_resultados = 10
		codigo_lenguaje = "es"
		url_google = 'https://www.google.com/search?q={}&num={}&hl={}'.format(termino_busqueda, numero_resultados, codigo_lenguaje)
		respuesta = requests.get(url_google, headers=USER_AGENT)
		respuesta.raise_for_status()
		return respuesta.text

	def procesar_resultados(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		resultados_encontrados = []
		bloque = soup.find_all("div", class_="g")
		for resultado in bloque:
			titulo = resultado.find('h3')
			link = resultado.find('a')['href']
			resultados_encontrados.append((titulo, link))
		return resultados_encontrados


bing = Bing()
google = Google()
buscador = ""

if CONFIG["BUSCADOR_WEB_SCRAPPING"] == "GOOGLE":
	buscador = google
else:
	buscador = bing

def scrap(termino_busqueda):

	html = buscador.obtener_resultados(termino_busqueda)
	resultados = buscador.procesar_resultados(html)

	return resultados


##palabra = "hola"
##resultados = scrap(palabra)
##print(resultados)

