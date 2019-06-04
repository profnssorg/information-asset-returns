#
#
#
#
# SCRAPPING --------------------------------------------------------------------
#
# fazer lista com noticias do arquivo json
def noticias(arq):
    arquivo = open(arq)
    lista = []
    i = 0
    for linha in arquivo.readlines():
        lista.append(linha[1:-3])
    lis = lista[1:-1]
    return(lis[::-1])
    arquivo.close()
# arrumar lista das noticias, deixando bonitinho
def arrumar(notic):
    lista = []
    for noticia in notic:
        lista.append('data: {}; hora: {}; titulo: {}; link: {}'.format(noticia[10:20],
                                                             noticia[21:26],
                                                             noticia[noticia.find('titulo')+10:noticia.find('link')-4],
                                                             noticia[noticia.find('link')+8:]))
    return(lista)
# Criar lista com datas do ano
def datas_do_ano():
    ser = pd.DataFrame(index = pd.date_range('2016-09-26', periods=964))
    return(ser)
#
#
# faz lista de todas as datas do ano, usado para colocar noticia no dia seguinte
def lista_datas(poxa):
    datas = []
    for coisa in poxa:
        data = str('{}/{}/{}'.format(coisa[8:10], coisa[5:7], coisa[:4]))
        if data not in datas:
            datas.append(data)
    return(datas)
#
#
#
#
# lista de noticias com dia para o qual a noticia vale
def proximodia(noticis, datas):
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
#
#
# Retorna lista com dia do ano e dia de cupom cambial correspondente
def corrigir(datas, serie):
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
# pega as noticias e coloca antes delas a data de cupom com a qual ela é relacionada
def juntar(eita, noti):
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
# separa as noticias que interessam
def separar_noticias(arq, palavras):
    lista = []
    for linha in arq:
        achou = False
        for palavra in palavras:
            if achou == False:
                if (palavra.lower() in linha.lower()[:linha.find('link')]) == True:
                    lista.append(linha)
                    achou == True
    return(lista)
# transforma o formato do texto para o normal
def transformar(lista):
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
#
#----------------------------------------------------------------------SCRAPPING
#
#
# TIME SERIES ------------------------------------------------------------------
#
# CREATE DATAFRAME FROM API LINK
def serie(numero, DataInicial, DataFinal):
    url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=csv&&dataInicial={}&dataFinal={}'.format(numero, data_inicial, data_final)
    return(pd.read_csv(url, sep = ';', index_col = 0, decimal = ','))
# EXCHANGE COUPON
def cupomCambial(juros, usd):
    CupomCambialValor = []
    CupomCambialData = []
    for i in range(len(usd.valor)):
        if i >= 1:
            valor = (1+ juros.valor[i]/100)/(usd.valor[i]/usd.valor[i-1])-1
            CupomCambialValor.append(valor)
            CupomCambialData.append(usd.index[i])
    v = {'valor': CupomCambialValor}        
    CupomCambial = pd.DataFrame(v, index = CupomCambialData)
    return(CupomCambial)
# LIMITS - PARAMETRIC
def limitP(v):
    mais = []
    menos = []
    data = []
    maior = v.mean() + (stats.norm.ppf(q = 0.975) * (v.std()))
    menor = v.mean() - (stats.norm.ppf(q = 0.975) * (v.std()))
    for i in range(len(v.values)):
        mais.append(maior)
        menos.append(menor)
        data.append(v.index[i])
    va = {'UpperLimit': mais, 'LowerLimit': menos}        
    T = pd.DataFrame(va, index = data)
    return(T)
# LIMITS - NON PARAMETRIC
def limitNP(v):
    mais = []
    menos = []
    valor = []
    data = []
    mean = v.rolling(window = 63, min_periods = 0, center = True).mean()
    std = v.rolling(window = 63, min_periods = 0, center = True).std()
    for i in range(len(v.values)):
        valor.append(v[i])
        array = pd.Series(valor)
        data.append(v.index[i])
        mais.append(mean[i] + (stats.norm.ppf(q = 0.975) * (std[i])))
        menos.append(mean[i] - (stats.norm.ppf(q = 0.975) * (std[i])))
    va = {'UpperLimit': mais, 'LowerLimit': menos}        
    T = pd.DataFrame(va, index = data)
    return(T)
#
#--------------------------------------------------------------------TIME SERIES
#