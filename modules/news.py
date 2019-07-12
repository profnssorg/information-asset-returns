'''
NOME: Some Evidence on Political Information and Exchange Coupon in Brazil -
      News Module
AUTHOR: Bernardo Paulsen
DATE: 2019/06/24
VERSION: 1.0.0
LINK: https://github.com/profnssorg/information-asset-returns

DESCRIPTION: Class for processing the news data

'''


######## CLASS DEFINITION ########


class News():

    '''THIS CLASS HAS METHODS TO MANIPULATE NEWS'''
    
    def __init__(self):
        
        self.init = 'OK'
    
    def noticias(arq):

        ''' CREATES LIST FROM NEWS JSON FILE '''

        arquivo = open(arq)
        lista = []
        i = 0
        for linha in arquivo.readlines():
            lista.append(linha[1:-3])
        lis = lista[1:-1]
        return(lis[::-1])
        arquivo.close()

    def arrumar(notic):


        ''' ORGANIZES INFOS OF NEWS '''

        lista = []
        for noticia in notic:
            lista.append('data: {}; hora: {}; titulo: {}; link: {}'.format(noticia[10:20],
                noticia[21:26],
                noticia[noticia.find('titulo')+10:noticia.find('link')-4],
                noticia[noticia.find('link')+8:]))
        return(lista)
    
    def datas_do_ano():

        ''' CREATES LIST WITH DATES (DATAFORMAT) '''

        ser = pd.DataFrame(index = pd.date_range('2016-09-26', periods=964))
        return(ser)
    
    def lista_datas(poxa):

        ''' CREATES LIST WITH DATES (STRING) '''

        datas = []
        for coisa in poxa:
            data = str('{}/{}/{}'.format(coisa[8:10], coisa[5:7], coisa[:4]))
            if data not in datas:
                datas.append(data)
        return(datas)

    def proximodia(noticis, datas):

        ''' APPENDS NEXT DAY TO NEWS AFTER 18H '''

        completa = list()
        for noticia in noticis:
            data_noticia = noticia[6:16]
            hora_noticia = noticia[24:26]
            minuto_noticia = noticia[27:29]
            titulo_noticia = noticia[noticia.find('titulo')+8:noticia.find('link')-2]
            link_noticia = noticia[noticia.find('link')+6:]
            ja_achou = False
            for i in range(len(datas)-1):
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
        return(completa)

    def corrigir(datas, serie):

        ''' LIST WITH MATCHING BUSINESS DAY FOR ALL DATES '''
        
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
                    if n > (len(datas)-1):
                        t = False
        return(e)

    def juntar(eita, noti):

        ''' APPENDS CORRESPONDING BUSINESS DAY TO NEWS STRING '''

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
        return(opa)

    def separar_noticias(arq, palavras):

        ''' SEPARATES NEWS WITH KEYWORDS ''''
        
        lista = []
        for linha in arq:
            achou = False
            for palavra in palavras:
                if achou == False:
                    if (palavra.lower() in linha.lower()[:linha.find('link')]) == True:
                        lista.append(linha)
                        achou == True
        return(lista)
    
    def transformar(lista):

        '''' CHANGES NEWS ENCODING '''
        
        final = []
        asci = ['$', ';', '%', '\\u00f4', '\\u00f5', '\\u00e1', '\\u00e0', '\\u00e3', '\\u00e2', '\\u00e9', '\\u00ea', '\\u00ed', '\\u00f3', '\\u00fa', '\\u00e7']
        utf = ['\\$', ',', ' por cento', 'ô', 'õ', 'á', 'à', 'ã', 'â', 'é', 'ê', 'í', 'ó', 'ú', 'ç']
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
        return(final)
