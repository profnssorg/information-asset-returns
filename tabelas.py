# Importação de bibliotecas
#import numpy as np
#import pandas as pd
#from scipy import stats
#import statsmodels.stats.diagnostic as dig
#from matplotlib import pyplot as plt

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

# pega os dias e as noticias selecionadas e exporta uma tabela com as noticias para cada dia de volatilidade anormal
def noticia_para_cada_dia(refName, dias, noticias, np = False):
    lista = []
    if np == False:
        anal = 'Parametric'
    else:
        anal = 'Non Parametric'

    b = open('{}.txt'.format(refName), 'w')
    a = '''\\begin{{longtable}}{{ | c | c | c | }}
\\caption{{Political News in Days of Abnormal Volatility by {} Analysis}}
\\label{{{}}}
\\hline \\multicolumn{{1}}{{|c|}}{{\\textbf{{}}}} & \\multicolumn{{1}}{{c|}}{{\\textbf{{Date}}}} & \\multicolumn{{1}}{{c|}}{{\\textbf{{News Headline}}}} \\\\ \\hline \\hline
\\endfirsthead
\\multicolumn{{3}}{{c}}%
{{{{\\bfseries \\tablename\\ \\thetable{{}} -- continued from previous page}}}} \\\\
\\hline \\multicolumn{{1}}{{|c|}}{{\\textbf{{}}}} & \\multicolumn{{1}}{{c|}}{{\\textbf{{Date}}}} & \\multicolumn{{1}}{{c|}}{{\\textbf{{News Headline}}}} \\\\ \\hline \\hline
\\endhead
\\hline \\hline \\multicolumn{{3}}{{| r |}}{{{{Continued on next page}}}} \\\\ \\hline
\\endfoot
\\hline \\hline \\multicolumn{{3}}{{| r |}}{{End of table}} \\\\ \\hline
\\endlastfoot'''.format(anal, refName)
    n = 0
    for dia in dias:
        for noticia in noticias:
            if (dia in noticia[noticia.find('data')+9:noticia.find('data')+19]):
                n += 1
                a += '\n{} & {} & {}[...] \\\\'.format(n, dia, noticia[noticia.find('titulo')+10:noticia.find('titulo')+70])
                a += '\n\\hline'
                lista.append(noticia)
    a += '''\n\\end{{longtable}}'''
    b.write(a)
    b.close()
    return(lista)