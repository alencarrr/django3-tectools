# -*- coding: utf-8 -*-
import tempfile
from datetime import datetime, time

import pdfkit
from core import models
from django.conf import settings
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template

# para colocar senha no pdfo qyyeo que de
# enc=pdfencrypt.StandardEncryption("dragao00",canPrint=0)

def minutesToHourStr(valor : int):
    hora = int(valor / 60)
    minutos = (valor - (hora * 60))
    str_hora = str(hora)
    str_minuto = str(minutos)
    if hora < 10:
      str_hora = '0' + str_hora

    if minutos < 10:
      str_minuto = '0' + str_minuto

    return '{}:{}'.format(str_hora,str_minuto)

def timeToMinutes(timeobject : time):
    return int(timeobject.hour*60+timeobject.minute+timeobject.second/60)

def imprime(request,pk):    
    # Retorna apenas dados da PK enviada
    apontamento = models.Apontamento.objects.get(pk=pk)

    apontamentos = models.Apontamento.objects.filter(periodo=apontamento.periodo,recurso=apontamento.recurso)

    total_minutos = 0;
    subtotal = {}
    for apontamento in apontamentos:
        inicio = apontamento.hora_inicial.replace(microsecond=0)
        final = apontamento.hora_final.replace(microsecond=0)
        tempo = (timeToMinutes(final)-timeToMinutes(inicio))
        apontamento.subtotal = minutesToHourStr(tempo)
        total_minutos += tempo

    # Configuro timestamp do relatorio.
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Define o contexto dos dados a serem lidos no template html
    contexto = {'apontamentos':apontamentos, 'date':date, 'total':minutesToHourStr(total_minutos)}

    # cria objeto template com base no template html
    template = get_template('report/apontamento.html')

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
        css_file = settings.CSS_REPORT_ROOT+'/apontamento.css'
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
        pdfkit.from_string(html_string,settings.PDF_ROOT+"/apontamento.pdf", options=opcoes, css=css_file)
        #buffer.seek(io.SEEK_SET)
        #resposta = HttpResponse(buffer.getvalue(),content_type='application/pdf')
        # print(buffer.getvalue())
        #resposta['Content-Disposition'] = 'inline; filename=mapacarga.pdf'
        #resposta['Content-Transfer-Enconding']='binary'
        #buffer.seek(io.SEEK_SET)
          # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return FileResponse(open(settings.PDF_ROOT+"/apontamento.pdf","rb"), as_attachment=False, filename="apontamento.pdf")
        # return resposta
    except Exception as e:
        print('Error: {}'.format(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
