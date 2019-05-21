# Importação de bibliotecas
#import numpy as np
#import pandas as pd
#from scipy import stats
from matplotlib import pyplot as plt
#import statsmodels.stats.diagnostic as dig

# Função para criar gráfico da variável
def graph(df, seriesName, graphName, pngName, refName, limit = False, np = False):
    if limit == True:
        if np == False:
            limitP(df).plot(figsize = (18,9))
        else:
            limitNP(df).plot(figsize = (18,9))
    df.plot(figsize = (18,9))
    plt.xlabel('Date')
    plt.ylabel(seriesName)
    plt.grid(which = 'both', axis = 'x')
    plt.savefig(pngName)
    
    a = open(pngName, 'w')
    a.write('''\\begin{{figure}}[H]
\\caption{{{}}}
\\label{{{}}}
\\centering
\\includegraphics[width=\textwidth]{{images/{}.png}}
\\end{{figure}}'''.format(graphName, refName, pngName))
    a.close()