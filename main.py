from crawler import*
from pdf import*

content = crawler_init()
#print('Fazendo Download...')
#download_pdf(content)
print('Convertendo PDF\'s')
convert_pdf(content)