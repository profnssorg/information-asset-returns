# Importação de bibliotecas
#import numpy as np
#import pandas as pd
from scipy import stats

# Calcula cupom cambial
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

# Limite Paramétrico
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

# Limite Não Paramétrico
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