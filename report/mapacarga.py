# -*- coding: utf-8 -*-
import tempfile
from datetime import datetime

from core import models
from django.conf import settings
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
import pdfkit


# para colocar senha no pdfo qyyeo que de 
# enc=pdfencrypt.StandardEncryption("dragao00",canPrint=0)

def imprimeMapa(request,pk):    
    print('chagou methodo imprimeMapa em {}'.format(settings.PDF_ROOT+settings.OS_SEPARATOR+"mapacarga.pdf"))
    mapa = models.Mapa.objects.get(pk=pk)
    campos = models.Mapa.objects.all().filter(id=pk)

    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Define o contexto dos dados a serem lidos no template html
    contexto = {'mapa':mapa,'campos':campos, 'date':date}

    # cria objeto template com base no template html
    template = get_template('report/mapacarga.html')

    # rederiza o template com os dados referenciados no contexto
    html_string = template.render(contexto)
   
    #a = open(settings.PDF_ROOT+"/mapacarga.html",'w')
    #a.write(html_string)
    #a.close()

    # Converte o HTML já renderizado com as informações para o PDF
    #buffer = io.BytesIO()
    #file_html = open(settings.PDF_ROOT+"/mapacarga.pdf",'wb')
    #pdf = pisa.pisaDocument(io.BytesIO(html_string.encode('UTF-8')),file_html)
    #pdf = pisa.pisaDocument(io.BytesIO(html_string.encode('UTF-8')),buffer)
    #file_html.close()

    # prepara a resposta HTTP
    try:
        css_file = settings.CSS_REPORT_ROOT+settings.OS_SEPARATOR+'mapacarga.css'
        # folha: A4 dpi: 72 width: 595 height: 842
        # folha: A4 dpi: 300 width: 2480 height: 3508
        opcoes = {
          'encoding':'UTF-8',
          'page-size': 'A4',
          'page-width':'210mm', 
          'page-height': '297mm',   
          'margin-bottom': '15',        
          'orientation': 'Portrait',
          'user-style-sheet': css_file,
          'footer-line':'',
          'footer-center':'[page] de [topage]',
        
        }
        pdfkit.from_string(html_string,settings.PDF_ROOT+settings.OS_SEPARATOR+"mapacarga.pdf", options=opcoes, css=css_file)

        return FileResponse(open(settings.PDF_ROOT+settings.OS_SEPARATOR+"mapacarga.pdf","rb"), as_attachment=False, filename="mapacarga.pdf")
        # return resposta
    except Exception as e:
        print('Error: {}'.format(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
