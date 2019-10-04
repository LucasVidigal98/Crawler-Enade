from bs4 import BeautifulSoup as BS
import requests

def crawler_init():

	req = requests.get('http://portal.inep.gov.br/educacao-superior/enade/provas-e-gabaritos') # Rquisição para a página do enade
	soup = BS(req.text, 'html.parser')
	years = soup.find_all(class_='list-download__row') #Captura as informações de todos os anos.
	content = dict()									# Relaciona os links dos pdf de acordo com as áreas.
	position = list()									# Salva a informação de onde começa e termina um link			
	count = 0
	position_caracter = 0								#Salva a posição do caracteres ', <, >
	count_areas = 0
			
	for info in years:

		links_list = list()								#Lista de links				
		study_area = info.find_all('h6')				#Area capturada pelo crawler
		links = info.find_all('a')						#Links capturados pelo crawler

		str_study_area = str(study_area)

		for caracter in str_study_area:				#Revove as tags <h6> da area de estudo capturada pelo crawler.

			if count == 2:
				position_caracter = 0
				count = 0
				break

			if caracter == '>':
				position.append(position_caracter)
				count += 1

			if caracter == '<' and count > 0:
				position.append(position_caracter)
				count += 1

			position_caracter += 1

		str_study_area = str_study_area[position[0]+1:position[1]]  # str_study_area recebe a string sem as tags <h6>
		position = list()

		for link in links:
			
			str_link = str(link)
		
			for caracter in str_link:       #Encontra o inicio eo final da string do link

				if caracter == '"':
					position.append(position_caracter)
					count += 1

				if count == 2:
					position_caracter = 0
					count = 0
					break

				position_caracter += 1

			links_list.append(str_link[position[0]+1:position[1]])   #Salva o link na lista
			position = list()

		if str_study_area in content.keys():		#Salva a area com seus respctivos links no docionario // Vefifica se a área já está no dicit
			content.update({str(str_study_area + '_' + str(count_areas)):links_list})
			count_areas += 1
		else:
			content.update({str_study_area:links_list})                  

	return content