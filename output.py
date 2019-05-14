# Importação de bibliotecas
#import numpy as np
#import pandas as pd
#from scipy import stats
import statsmodels.stats.diagnostic as dig
from matplotlib import pyplot as plt

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

# Função para criar tabela de estatisticas decritivas
def des(refName, variables = [], names = [], csd = False):
    b = open(refName, 'w')
    a = '''\\begin{{table}}[H]
\\caption{{Descriptive Statistics}}
\\label{{{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | c | c | }}
\\hline
Series & Mean & Standard Deviation & Minimum Value & Maximum Value \\\\
\\hline \\hline'''.format(refName)
    if csd == False:
        for i in range(len(variables)):
            var = variables[i]
            a += '\n{0} & {1:.3f} & {2:.3f} & {3:.3f} & {4:.3f} \\\\'.format(names[i],
                                                                             var.mean()[0],
                                                                             var.std()[0],
                                                                             var.min()[0],
                                                                             var.max()[0])
            a += '\n\\hline'
    else:
        for i in range(len(variables)):
            var = variables[i]
            a += '\n{0} & {1:.3f} & {2:.3f} & {3:.3f} & {4:.3f} \\\\'.format(names[i],
                                                                             var.mean(),
                                                                             var.std(),
                                                                             var.min(),
                                                                             var.max())
            a += '\n\\hline'
    a += '''\n\\end{tabular}
\\end{table}'''
    b.write(a)
    b.close()

# Teste de Augmented Dickey-Fuller
def adf(refName, variables = [], names = []):
    b = open(refName, 'w')
    a = '''\\begin{{table}}[H]
\\caption{{Augmented Dickey-Fuller Test}}
\\label{{{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | }}
\\hline
Series & Test Statistic & Critical Value at 5\% Level \\\\
\\hline \\hline'''.format(refName)
    for i in range(len(variables)):
        adf = stat.adfuller(variables[i].valor)
        a += '\n{0} & {1:.3e} & {2:.3e} \\\\'.format(names[i],
                                                     adf[0],
                                                     adf[4]['5%'])
        a += '\n\\hline'
    a += '''\n\\end{tabular}
\\end{table}'''
    b.write(a)
    b.close()

# Teste de KPSS
def kpss(refName, variables = [], names = []):
    b = open(refName, 'w')
    a = '''\\begin{{table}}[H]
\\caption{{Augmented Dickey-Fuller Test}}
\\label{{{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | }}
\\hline
Series & Test Statistic & Critical Value at 5\% Level \\\\
\\hline \\hline'''.format(refName)
    for i in range(len(variables)):
        kpss = stat.kpss(variables[i].valor)
        a += '\n{0} & {1:.3e} & {2:.3e} \\\\'.format(names[i],
                                                     kpss[0],
                                                     kpss[3]['5%'])
        a += '\n\\hline'
    a += '''\n\\end{tabular}
\\end{table}'''
    b.write(a)
    b.close()

# Testes de Ljung-Box e Shapiro-Wilk
def ljungShapiro(refName, variables = [], names = []):
    b = open(refName, 'w')
    a = '''\\begin{{table}}[H]
\\caption{{Ljung-Box Test and Shapiro-Wilk Test}}
\\label{{{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | }}
\\hline
Series & P-value for Ljung-Box Test & P-value for Shapiro-Wilk Test \\\\
\\hline \\hline'''.format(refName)
    for i in range(len(variables)):
        var = variables[i]
        a += '\n{0} & {1:.3e} & {2:.3e} \\\\'.format(names[i],
                                                     dig.acorr_ljungbox(var, lags=1)[1][0],
                                                     stats.shapiro(var)[1])
        a += '\n\\hline'
    a += '''\n\\end{tabular}
\\end{table}'''
    b.write(a)
    b.close()

# Tabela com limites da análise paramétrica
def tabP(refName, variables = [], names = []):
    b = open(refName, 'w')
    a = '''\\begin{{table}}[H]
\\caption{{Limits from Parametric Analysis}}
\\label{{{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | c | c | }}
\\hline
Series & Lower Limit & Upper Limit \\\\
\\hline \\hline'''.format(refName)
    for i in range(len(variables)):
        var = variables[i]
        a += '\n{0} & {1:.3f} & {2:.3f} \\\\'.format(names[i],
                                                     var.LowerLimit[0],
                                                     var.UpperLimit[0])
        a += '\n\\hline'
    a += '''\n\\end{tabular}
\\end{table}'''
    b.write(a)
    b.close()

# Tabela com média dos limites da análise nãp paramétrica
def tabNP(refName, variables = [], names = []):
    b = open(refName, 'w')
    a = '''\\begin{{table}}[H]
\\caption{{Limits from Parametric Analysis}}
\\label{{{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | c | c | }}
\\hline
Series & Mean of Lower Limits & Mean of Upper Limits \\\\
\\hline \\hline'''.format(refName)
    for i in range(len(variables)):
        var = variables[i]
        a += '\n{0} & {1:.3f} & {2:.3f} \\\\'.format(names[i],
                                                     var.LowerLimit.mean(),
                                                     var.UpperLimit.mean())
        a += '\n\\hline'
    a += '''\n\\end{tabular}
\\end{table}'''
    b.write(a)
    b.close()
    print(a)

def outside(refName, ec, csd, lim):
    b = open('{}.txt'.format(refName), 'w')
    a = '''\\begin{{table}}[H]
\\caption{{Days with Abnormal Returns}}
\\label{{{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | c | c | c |}}
\\hline
& Exchange Coupon & Conditional Standard Deviation & Lower Limit & Upper Limit & Date \\\\
\\hline \\hline'''.format(refName)
    n = 0
    for i in range(len(csd.index)):
        if csd[i] > lim.UpperLimit[i]:
            n += 1
            a += '\n{0} & {1:.3f} & {2:.3f} & {3:.3f} & {4:.3f} & {5}\\\\'.format(n,
                                                                                  ec.valor[i],
                                                                                  csd[i],
                                                                                  lim.LowerLimit[i],
                                                                                  lim.UpperLimit[i],
                                                                                  csd.index[i])
            a += '\n\\hline'
        elif csd[i] < lim.LowerLimit[i]:
            n += 1
            a += '\n{0} & {1:.3f} & {2:.3f} & {3:.3f} & {4:.3f} & {5}\\\\'.format(n,
                                                                                  ec.valor[i],
                                                                                  csd[i],
                                                                                  lim.LowerLimit[i],
                                                                                  lim.UpperLimit[i],
                                                                                  csd.index[i])
            a += '\n\\hline'
    a += '''\n\\end{tabular}
\\end{table}'''
    b.write(a)
    b.close()












