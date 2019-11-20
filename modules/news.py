'''
NOME: Some Evidence on Political Information and Exchange Coupon in Brazil -
      News Module
AUTHOR: Bernardo Paulsen
DATE: 2019/06/24
VERSION: 2.0.0
LINK: https://github.com/profnssorg/information-asset-returns

DESCRIPTION: Class for processing the news data

'''

# IMPORT PACKAGES ########


import pandas as pd


# CLASS DEFINITION ########


class News():

    def __init__(self):

        self.init = 'OK'

    # fazer lista com noticias do arquivo json
    def news(arq):
        arquivo = open(arq)
        lista = []
        i = 0
        for linha in arquivo.readlines():
            lista.append(linha[1:-3])
        lis = lista[1:-1]
        return (lis[::-1])
        arquivo.close()

    # arrumar lista das noticias, deixando bonitinho
    def arrange(notic):
        lista = []
        for noticia in notic:
            lista.append('data: {}; hora: {}; titulo: {}; link: {}'.format(noticia[10:20],
                noticia[21:26],
                noticia[noticia.find('titulo') + 10:noticia.find('link') - 4],
                noticia[noticia.find('link') + 8:]))
        return (lista)

    # Criar lista com datas do ano
    def days_of_year():
        ser = pd.DataFrame(index=pd.date_range('2016-09-26', periods=964))
        return (ser)

    #
    #
    # faz lista de todas as datas do ano, usado para colocar noticia no dia seguinte
    def list_days(poxa):
        datas = []
        for coisa in poxa:
            data = str('{}/{}/{}'.format(coisa[8:10], coisa[5:7], coisa[:4]))
            if data not in datas:
                datas.append(data)
        return (datas)

    #
    #
    #
    #
    # lista de noticias com dia para o qual a noticia vale
    def nextday(noticis, datas):
        completa = list()
        for noticia in noticis:
            data_noticia = noticia[6:16]
            hora_noticia = noticia[24:26]
            minuto_noticia = noticia[27:29]
            titulo_noticia = noticia[noticia.find('titulo') + 8:noticia.find('link') - 2]
            link_noticia = noticia[noticia.find('link') + 6:]
            ja_achou = False
            for i in range(len(datas) - 1):
                data = datas[i]
                if ja_achou == False:
                    if str(data_noticia) == str(data):
                        o = i
                        if int(hora_noticia) >= 18:
                            o += 1
                        completa.append('data: {}; hora: {}; minuto: {}; dia: {}; titulo: {}; link: {}'.format(data_noticia,
                            hora_noticia,
                            minuto_noticia,
                            datas[o],
                            titulo_noticia,
                            link_noticia))
                        ja_achou = True
        return (completa)

    #
    #
    # Retorna lista com dia do ano e dia de cupom cambial correspondente
    def correct(datas, serie):
        e = []
        for i in range(len(datas)):
            t = True
            n = i
            o = 0
            while t == True:
                if (datas.index[n] in serie.index) == True:
                    e.append('{} --- {}'.format(datas.index[i], datas.index[n]))
                    t = False
                else:
                    n += 1
                    if n > (len(datas) - 1):
                        t = False
        return (e)

    # pega as noticias e coloca antes delas a data de cupom com a qual ela é relacionada
    def join(eita, noti):
        opa = []
        for noticia in noti:
            ja = False
            data = noticia[45:55]
            for dia in eita:
                if ja == False:
                    date = '{}/{}/{}'.format(dia[8:10], dia[5:7], dia[:4])
                    cup = '{}/{}/{}'.format(dia[32:34], dia[29:31], dia[24:28])
                    if data == date:
                        ja = True
                        opa.append('cupom: {} // {}'.format(cup, noticia))
        return (opa)

    # separa as noticias que interessam
    def separate_news(arq, palavras):
        lista = []
        for linha in arq:
            achou = False
            for palavra in palavras:
                if achou == False:
                    if (palavra.lower() in linha.lower()[:linha.find('link')]) == True:
                        lista.append(linha)
                        achou == True
        return (lista)

    # transforma o formato do texto para o normal
    def transform(lista):
        final = []
        asci = ['$', ';', '%', '\\u00f4', '\\u00f5', '\\u00e1', '\\u00e0',
        '\\u00e3', '\\u00e2', '\\u00e9', '\\u00ea','\\u00ed', '\\u00f3',
        '\\u00fa', '\\u00e7']
        utf = ['\\$', ',', ' por cento', 'ô', 'õ', 'á', 'à', 'ã', 'â', 'é',
        'ê', 'í', 'ó', 'ú', 'ç']
        for noticia in lista:
            a = noticia
            ja = False
            for i in range(len(asci)):
                if ja == False:
                    a = noticia.replace(asci[i], utf[i])
                    ja = True
                else:
                    a = a.replace(asci[i], utf[i])
            final.append(a)
        return (final)