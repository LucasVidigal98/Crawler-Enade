import requests

def download_pdf(content_dict):
	
	for links_pdf in content_dict.keys():

	    with open(str(content_dict[links_pdf][0]), "wb") as file:
	        response = requests.get(str(content_dict[links_pdf][0]))
	        file.write(response.content)

	    with open(str(content_dict[links_pdf][1]), "wb") as file:
	        response = requests.get(str(content_dict[links_pdf][1]))
	        file.write(response.content)

	    with open(str(content_dict[links_pdf][2]), "wb") as file:
	       response = requests.get(str(content_dict[links_pdf][2]))
	       file.write(response.content)