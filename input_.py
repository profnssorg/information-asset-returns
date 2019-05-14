# Importação de bibliotecas
import numpy as np
import pandas as pd
# Funçnao para criar DataFrame por API
def serie(numero, DataInicial, DataFinal):
    url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=csv&&dataInicial={}&dataFinal={}'.format(numero, data_inicial, data_final)
    return(pd.read_csv(url, sep = ';', index_col = 0, decimal = ','))