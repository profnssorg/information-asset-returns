# IMPORT PACKAGES
import numpy as np # api - array used for series and dataframe data structures
                   # fundamental package for scientific computing
import pandas as pd # api - series and datagrame data structues & various 
                    # data structures and data analysis tools
from arch import arch_model # garch model
from scipy import stats # confidence interval
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
def bacen_sgs_api(names = list(), # names to be assign to series
                  numbers = list(), # series' numbers on SGS
                  initial_date = str(),
                  final_date = str()):
    
    '''CREATES DATAFRAME FROM BACEN-SGS SERIES'''

    for i in range(len(names)):
        name = str(names[i])
        url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=csv&&dataInicial={}&dataFinal={}'.format(numbers[i], initial_date, final_date)
        df = pd.read_csv(url, sep = ';', index_col = 0, parse_dates = [0], infer_datetime_format = True, decimal = ',')
        if i == 0:
            DF = pd.DataFrame({name: df.valor},
                              index = df.index)
        else:
            DF[name] = df.valor
    return(DF)
def exchange_coupon(df = pd.DataFrame(), # DataFrame containing the Series for the exchange coupon
                  dol = int(), # column number of exchange rate Series
                  rs = list(), # columns numbers for interest rates Series (min 1 number, if > 1 then more than one measure of exchange coupon is generated)
                  names = list()): # names for exchange coupons
    
    '''APPENDS EXCHANGE COUPON TO DATAFRAME'''
    
    usd = df[df.columns[dol]]
    for e in range(len(rs)):
        r = df[df.columns[rs[e]]]
        name = names[e]
        arr = np.array(list())
        for i in range(len(usd)):
            if i == 0:
                arr = np.append(arr, np.NaN)
            else:
                arr = np.append(arr, (1+ r[i]/100)/(usd[i]/usd[i-1]))
        df[name] = arr
def garch(df = pd.DataFrame(), # DataFrame containing the Series 
          cols = list()): # columns numbers of Series
    
    '''APPENDS GARCH'S CSD AND RESIDUALS TO DATAFRAME'''
    
    for i in range(len(cols)):
        name = df.columns[cols[i]]
        fitted_model = arch_model(df[name][1:]).fit()
        df['{}Csd'.format(name)] = fitted_model.conditional_volatility
        df['{}Res'.format(name)] = fitted_model.resid

def limits(df = pd.DataFrame(), # DataFrame containing the Series
           cols = list()): # columns numbers of Series
    
    '''APPENDS PARAMETRIC AND NON PARAMETRIC LIMITS TO DATAFRAME'''
    
    def create_par(up = True):
        
        '''RETURNS ARRAY OF PARAMETRIC LIMIT (UPPER OR LOWER)'''
        
        mean = series.mean()
        std = series.std()
        if up == True:
            value = mean + stats.norm.ppf(q = 0.975) * (std)
        else:
            value = mean - stats.norm.ppf(q = 0.975) * (std)
        arr = np.array(list())
        for i in range(len(series)):
            if i == 0:
                arr = np.append(arr, np.NaN)
            else:
                arr = np.append(arr, value)
        return(arr)

    def create_non(up = True):

        '''RETURNS ARRAY OF NON PARAMETRIC LIMIT (UPPER OR LOWER)'''
        
        mean = series.rolling(window = 63, min_periods = 0, center = True).mean()
        std = series.rolling(window = 63, min_periods = 0, center = True).std()
        arr = np.array(list())
        for i in range(len(mean)):
            if up == True:
                value = mean[i] + stats.norm.ppf(q = 0.975) * (std[i])
            else:
                value = mean[i] - stats.norm.ppf(q = 0.975) * (std[i])
            if i == 0:
                arr = np.append(arr, np.NaN)
            else:
                arr = np.append(arr, value)
        return(arr)
    
    for e in range(len(cols)):
        name = df.columns[cols[e]]
        series = df[name]
        # PARAMETRIC
        # ----UPPER
        df['{}ParUp'.format(name)] = create_par(up=True)
        # ----LOWER 
        df['{}ParLo'.format(name)] = create_par(up=False)
        # NON PARAMETRIC
        # ----UPPER
        df['{}NonUp'.format(name)] = create_non(up = True)
        # ----LOWER
        df['{}NonLo'.format(name)] = create_non(up = False)
#
#--------------------------------------------------------------------TIME SERIES
#