# Importação de bibliotecas
#import numpy as np
#import pandas as pd
#from scipy import stats
#from matplotlib import pyplot as plt
import statsmodels.stats.diagnostic as dig

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