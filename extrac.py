import os
from PIL import Image 	# Importando o módulo Pillow para abrir a imagem no script
import pytesseract 		# Módulo para a utilização da tecnologia OCR
import pdftotext


# Verifica se é questão discursiva
def contemDiscursiva(IMAGEM):
	# print IMAGEM
	texto = pytesseract.image_to_string(Image.open(IMAGEM))
	texto = texto.upper()
	# print texto
	PalavrasPesquisa = ['DISCURSIVA', 'QUESTIONARIO','RASCUNHO']
	for palavra in PalavrasPesquisa:
		matches = texto.find(palavra)
		if matches != -1:
			return 1

	return 0


def getNumeroQuestoes(IMAGEM):

	texto = pytesseract.image_to_string(Image.open(IMAGEM))
	texto = texto.upper()
	numQuestoes = 0
	matchQuestao = 0
	list = []
	try:
		while matchQuestao != -1:

			matchQuestao = texto.find('QUESTAO')

			if matchQuestao != -1:
				numQuestoes+=1
				aux = texto[matchQuestao:matchQuestao+10]
				aux = aux.split(' ')
				aux = aux[1]
				# print "Colocando ", str(aux),"na lista"
				# if str(aux) == 'S':
				# 	print texto[matchQuestao:matchQuestao+10]
				if aux.isnumeric() == 1:
					list.append(str(aux))
				else:
					return [], 0

				# print "Questao ", aux[1], "encontrada"
				texto = texto.replace('QUESTAO', 'OK', 1)
	except:
		return [], 0
		print ("GetNumeroQuestoes:", list)
	matchQuestao = texto.find('AREA LIVRE')
	if matchQuestao != -1:
		return list, 'AL'
	# print list
	return list, 0

def paginaSimplesOuDupla(IMAGEM):
    
    im = Image.open(r""+IMAGEM)
    
    width, height = im.size
    # print(width, height)
    
    #Left, top, rigth, bottom
    imR = im.crop((0, 200, width/2, height))
    # imagem esquerda
    imR.save('imgEsquerda.jpg')
    
    imR = im.crop((width/2, 200, width, height))
    # imagem direita
    imR.save('imgDireita.jpg')
    
    
    imgEsquerdaNumQuestoes, lixo = getNumeroQuestoes('imgEsquerda.jpg')
    imgDireitaNumQuestoes, lixo = getNumeroQuestoes('imgDireita.jpg')
    
    if len(imgEsquerdaNumQuestoes) == 0 and len(imgDireitaNumQuestoes) == 0:
        return 'none', -1, -1
    
    elif len(imgEsquerdaNumQuestoes) > 0 and len(imgDireitaNumQuestoes) > 0:
        return 'dupla', imgEsquerdaNumQuestoes, imgDireitaNumQuestoes
    
    elif len(imgEsquerdaNumQuestoes) > 0 and len(imgDireitaNumQuestoes) == 0:
        return 'simples', imgEsquerdaNumQuestoes, imgDireitaNumQuestoes
    
    elif len(imgEsquerdaNumQuestoes) == 0 and len(imgDireitaNumQuestoes) > 0:
        return 'none', -1, -1
    return 'none', -1, -1

def extractQuestions(dicEnade, ano):

    ID = 0

    # print('>> Ano: ', ano)

    for area in dicEnade[ano]:

        print('   >> Area: ', area)
        os.mkdir('EnadeProvas/'+ano+'/'+area+'/Questoes')
        pdf = PdfFileReader(open('EnadeProvas/'+ano+'/'+area+'/Prova.pdf','rb'))
        numPages = pdf.getNumPages()
        for i in range(1, numPages):
            ID, OK = workInPage('EnadeProvas/'+ano+'/'+area+'/Prova.pdf_dir/'+str(i)+'_Prova.pdf.jpg', ID, 'EnadeProvas/'+ano+'/'+area+'/Questoes')

            if OK == -1:
                print('Pagina Ignorada: ', i)
            elif True: print('Pagina processada com Sucesso!: ', i)


def workInPage(IMAGEM, diretorio):
	listQuestoes = []
	print ('Processando pagina: ', IMAGEM)

	if contemDiscursiva(IMAGEM) == 1:
		print ("Descartando pagina, contém discursiva")
		return -1

	# print "Imagem não descartada ainda"

	im = Image.open(r""+IMAGEM)

	width, height = im.size
	# print "Tamanho da pagina:",width,'x',height,'px'
	
	tipoPagina, imgEsquerdaNumQuestoes, imgDireitaNumQuestoes = paginaSimplesOuDupla(IMAGEM)
	
	if tipoPagina == 'none': 
		print('Descartando pagina: nenhuma questão encontrada em', IMAGEM)
		return -1

	print('Pagina: ', tipoPagina, imgEsquerdaNumQuestoes, imgDireitaNumQuestoes)
	#Left, top, rigth, bottom
	coordenadasIMG = []

	if tipoPagina == 'simples':
		coordenadasIMG.append((0, 200, width, height-250))

	elif tipoPagina == 'dupla':
		coordenadasIMG.append((0, 200, width/2, height-250))
		coordenadasIMG.append((width/2, 200, width, height-250))

	elif True:
		input("ERRO AO IDENTIFICAR QUESTOES")
		return -1

	getQ = 0
	listQuestoes = imgEsquerdaNumQuestoes + imgDireitaNumQuestoes
	
	for i in range(len(coordenadasIMG)):
		# print "lado",i
		# print "lista = ", listQuestoes,159
		left, top, right, bottom = coordenadasIMG[i][0], coordenadasIMG[i][1], coordenadasIMG[i][2], coordenadasIMG[i][3]
		# print(left, top, right, bottom)

		saveTOP = saveBT = cont = 0
		if tipoPagina == 'simples' and len(listQuestoes) == 1: 
			lx, AL = getNumeroQuestoes(IMAGEM)
			if AL != 'AL':
				saveBT = bottom+50

		# X é a variável de baixo  
		# print "lista = ", listQuestoes,159
		# print "lista = ", listQuestoes,159
		x = 300
		while x < height-200:

			# print "lista = ", listQuestoes, "172 x=",x,"contador=",contador
			imR = im.crop((left, top, right, x))
			imR.save('processando.jpg')

			# ENCONTROU QUESTÃO, SALVA POSIÇÃO SUPERIOR
			if saveTOP == 0:
				# print "170"
				# print listQuestoes
				# print getQ,"eh o indice atual"
				lx, AL = getNumeroQuestoes('processando.jpg')
				if len(lx) != 0:
					# print "Encontrei questao savetop = x = ", savetop,"x passou para",x+100
					saveTOP = x
					x = x + 100
					top = top + 100

			# SE NÃO TIVER AREA LIVRE
			elif saveBT == 0:
				# print "178"
				# print listQuestoes
				# print getQ,"eh o indice atual"
				lx, AL = getNumeroQuestoes('processando.jpg')
				if AL == 'AL': saveBT = x
				if len(lx) != 0: saveBT = x

			# SE ENCONTROU INICIO E FIM, CORTA IMAGEM
			if saveTOP != 0 and saveBT != 0:
				# print listQuestoes
				# print getQ,"eh o indice atual"
				imR = im.crop((left, saveTOP+10, right, saveBT-50))
				
				print ('SALVANDO: '+diretorio+str(listQuestoes[getQ])+'.jpg')
				imR.save(diretorio+str(listQuestoes[getQ])+'.jpg')
				saveTOP = saveBT = 0
				# print("1) Get Question "+str(getQ+1)+" Success")
				getQ+=1
				if tipoPagina == 'simples': break
			    
			x+=15
			top+=15
		
		# SE NÃO ENCONTROU FINAL, CORTA ASSIM MESMO
		if saveTOP != 0 and saveBT == 0:
			imR = im.crop((left, saveTOP-5, right, bottom))
			if(getQ >= len(listQuestoes)):
				# print listQuestoes, getQ,'\n'
				qetQ= len(listQuestoes) - 1
			imR.save(diretorio+'/'+str(listQuestoes[getQ])+'.jpg')
			saveTOP = saveBT = 0
			# print("2) Get Question "+str(getQ)+" Success")
			getQ+=1

	# print('Numero de questoes capturadas: ', getQ)
	# print 'Total de questoes: ', imgEsquerdaNumQuestoes+imgDireitaNumQuestoes
	return  0


def	trabalhaNaProva(dirImagens, STORE_FOLDER):
	# print dirImagens
	# print STORE_FOLDER

	imagens =  os.listdir(dirImagens)

	ID = 0
	numPages = len(imagens)
	print (numPages, " paginas")
	for i in range(0,numPages):
		OK = workInPage(dirImagens+imagens[i], STORE_FOLDER)
		
def init_extract_questions(content):
		
		for key in content.keys():
			images = 'Images/Prova ' + key + '.pdf_dir'
			if '2009' in images or '2008' in images or '2007' in images or '2006' in images or '2005' in images or '2004' in images:
				#Se a prova for anterior de 2010 não pega as questões
				continue
			
			try:
				os.mkdir('Questoes/' + key)
			except:
				pass

			dire = 'Questoes/' + key

			trabalhaNaProva(images, dire)

def init_extract_answers():


	#Fazer for para pegar todos os arquivos

	try:
		with open('Gabarito Arquivologia.pdf', 'rb') as file:
			pdf = pdftotext.PDF(file)
	except:
		print('Deu ruim')
		#Continue

	found = False
	for str_page in pdf:
		for i in range(0, len(str_page)):
			
			found_number = False
			if str_page[i].isdigit() and str_page[i+1].isdigit():
				print(str(str_page[i]) + '' + str(str_page[i+1]))

				carater = i
				#Pega a resposta da questao da questao
				while not str_page[carater].isalpha():
					carater+=1

				answer = str_page[carater]
				print(answer)
				
				#Verfica a resposta da questão tem mais algum caracter além da própria resposta, se tiver, possivelment a questão foi anulada ou é uma questão discursiva
				if(str_page[carater+1].isalpha()):
					#Fazer o módulo para deletar a questao
					print('SIM')

				found_number = True
			elif found == False and str_page[i].isdigit() and not(str_page[i+1].isdigit()):
				print(str_page[i])

				carater = i
				#Pega a resposta da questao da questao
				while not str_page[carater].isalpha():
					carater+=1

				answer = str_page[carater]
				print(answer)

				#Verfica a resposta da questão tem mais algum caracter além da própria resposta, se tiver, possivelment a questão foi anulada ou é uma questão discursiva
				if(str_page[carater+1].isalpha()):
					#Fazer o módulo para deletar a questao
					print('SIM')

			#Verifica se foi encontrado um numero de dois digitos
			if found_number == True:
				found = True
			else:
				found = False