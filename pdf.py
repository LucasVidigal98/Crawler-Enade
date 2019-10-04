import requests

def download_pdf(content_dict):
	
	for links_pdf in content_dict.keys():

	    with open('Pdfs\\' + 'Prova ' + str(links_pdf) + '.pdf', "wb") as file:
	        response = requests.get(str(content_dict[links_pdf][0]))
	        file.write(response.content)

	    with open('Pdfs\\' + 'Gabarito ' + str(links_pdf) + '.pdf', "wb") as file:
	        response = requests.get(str(content_dict[links_pdf][1]))
	        file.write(response.content)

	    with open('Pdfs\\' + 'Padrão de resposta ' + str(links_pdf) + '.pdf', "wb") as file:
	       response = requests.get(str(content_dict[links_pdf][2]))
	       file.write(response.content)