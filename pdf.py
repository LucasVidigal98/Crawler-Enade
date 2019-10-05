import requests
from pdf2jpg import pdf2jpg
import os
from thread_convert import ThreadConvert

def download_pdf(content_dict):

	try:
		os.mkdir('Pdfs/')
	except:
		pass
	
	for links_pdf in content_dict.keys():

		try:
		    with open('Pdfs/' + 'Prova ' + str(links_pdf) + '.pdf', "wb") as file:
		        response = requests.get(str(content_dict[links_pdf][0]))
		        file.write(response.content)
		except:
			continue

		try:
		    with open('Pdfs/' + 'Gabarito ' + str(links_pdf) + '.pdf', "wb") as file:
		        response = requests.get(str(content_dict[links_pdf][1]))
		        file.write(response.content)
		except:
			continue

		try:
		    with open('Pdfs/' + 'Padrão de resposta ' + str(links_pdf) + '.pdf', "wb") as file:
		       response = requests.get(str(content_dict[links_pdf][2]))
		       file.write(response.content)
		except:
			continue

def convert_pdf(content_dict):

	try:
		os.mkdir('Images')
	except:
		pass
	
	t_1 = ThreadConvert(0, content_dict)
	t_2 = ThreadConvert(1, content_dict)
	t_3 = ThreadConvert(2, content_dict)
	t_1.start()
	t_2.start()
	t_3.start()