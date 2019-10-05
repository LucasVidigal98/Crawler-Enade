import threading
from pdf2jpg import pdf2jpg

class ThreadConvert(threading.Thread):

	def __init__(self, id_thread, content_dict):
		super(ThreadConvert, self).__init__()
		self.id_thread = id_thread
		self.content_dict = content_dict

	def run(self):

		if self.id_thread == 0:

			for key in self.content_dict.keys():	
				pdf_name = 'Pdfs/Prova ' + key + '.pdf'
				pdf2jpg.convert_pdf2jpg(pdf_name, 'Images/', pages='ALL')
			
					

		if self.id_thread == 1:

			for key in self.content_dict.keys():
				pdf_name = 'Pdfs/Gabarito ' + key + '.pdf'
				pdf2jpg.convert_pdf2jpg(pdf_name, 'Images/', pages='ALL')
				
					

		if self.id_thread == 2:

			for key in self.content_dict.keys():
				pdf_name = 'Pdfs/Padrão de resposta ' + key + '.pdf'
				pdf2jpg.convert_pdf2jpg(pdf_name, 'Images/', pages='ALL')
				
