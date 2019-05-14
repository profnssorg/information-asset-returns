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
    for i in range(len(v.values)):
        valor.append(v[i])
        array = np.array(valor)
        data.append(v.index[i])
        mais.append(array.mean() + (stats.norm.ppf(q = 0.975) * (array.std())))
        menos.append(array.mean() - (stats.norm.ppf(q = 0.975) * (array.std())))
    va = {'UpperLimit': mais, 'LowerLimit': menos}        
    T = pd.DataFrame(va, index = data)
    return(T)