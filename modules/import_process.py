#
#
#
#
# SCRAPPING --------------------------------------------------------------------
#
# JSON FILE TO LIST
def noticias(arq):
    arquivo = open(arq)
    lista = []
    i = 0
    for linha in arquivo.readlines():
        lista.append(linha[1:-3])
    lis = lista[1:-1]
    return(lis[::-1])
    arquivo.close()
# CREATE LIST WITH DATES FROM INTERVAL
def datas_do_ano():
    ser = pd.DataFrame(index = pd.date_range('2016-09-26', periods=1000))
    a = []
    for i in range(len(ser)):
        a.append('{}/{}/{}'.format(str(ser.index[i])[8:10], str(ser.index[i])[5:7], str(ser.index[i])[:4]))
    return(a)
# MATCH DATES LIST WITH TIME SERIES LIST
def corrigir(datas, serie):
    e = []
    for i in range(len(datas)):
        t = True
        n = i
        o = 0
        while t == True:
            if (datas[n] in serie.index) == True:
                e.append('{} --- {}'.format(datas[i], datas[n]))
                t = False
            else:
                n += 1
                if n > (len(datas)-1):
                    t = False
    return(e)
# INSERTS TIME SERIES DATE TO NEWS
def juntar(eita, noti):
    opa = []
    for noticia in noti:
        ja = False
        data = noticia[10:20]
        for dia in eita:
            if ja == False:
                date = dia[:10]
                if data == date:
                    ja = True
                    opa.append('{} //// {}'.format(dia[15:], noticia))
    return(opa)
# FILTER THE NEWS FROM KEYWORDS
def separar_noticias(arq, palavras):
    lista = []
    for linha in arq:
        achou = False
        for palavra in palavras:
            if achou == False:
                if (palavra.lower() in linha.lower()[:linha.find('link')]) == True:
                    lista.append(linha[:-3])
                    achou == True
    return(lista)
# CONVERTS THE TEXT TO UTF8
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
                ja = True
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