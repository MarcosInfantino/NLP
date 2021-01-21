import requests
from bs4 import BeautifulSoup
import docs
from config import CONFIG
import mainFunctions

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

def obtener_resultados(termino_busqueda, numero_resultados, codigo_lenguaje):
	url_google = 'https://www.google.com/search?q={}&num={}&hl={}'.format(termino_busqueda, numero_resultados, codigo_lenguaje)
	respuesta = requests.get(url_google, headers=USER_AGENT)
	respuesta.raise_for_status()
	return termino_busqueda, respuesta.text

def procesar_resultados(html, palabra):
	soup = BeautifulSoup(html, 'html.parser')
	resultados_encontrados = []
	bloque = soup.find_all("div", class_="g")
	for resultado in bloque:
		titulo = resultado.find('h3')
		link = resultado.find('a')['href']
		resultados_encontrados.append((titulo, link))
	return resultados_encontrados
	
def scrap(termino_busqueda, numero_resultados, codigo_lenguaje):
	palabra, html = obtener_resultados(termino_busqueda, numero_resultados, codigo_lenguaje)
	resultados = procesar_resultados(html, palabra)
	return resultados

'''if __name__ == '__main__':
	palabra = "\"En este apartado se consideran las entregas tipo presentación de diapositivas o páginasWeb. En ellas abundan los párrafos cortos\""
	resultados = scrap(palabra, 10, "es")
	print(resultados)'''

