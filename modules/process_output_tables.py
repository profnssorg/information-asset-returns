# Função para criar tabela de estatisticas decritivas
def des(series, refName, variables = [], names = [], csd = False):
    b = open('latex/tables/{}.txt'.format(refName), 'w')
    a = '''\\begin{{table}}[H]
\\caption{{Descriptive Statistics for {}}}
\\label{{tab:{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | c | c | }}
\\hline
Series & Mean & Standard Deviation & Minimum Value & Maximum Value \\\\
\\hline \\hline'''.format(series, refName)
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
    b = open('latex/tables/{}.txt'.format(refName), 'w')
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
    b = open('latex/tables/{}.txt'.format(refName), 'w')
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
    b = open('latex/tables/{}.txt'.format(refName), 'w')
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

# Testes de Ljung-Box e Shapiro-Wilk
def shapiro(refName, variables = [], names = []):
    b = open('latex/tables/{}.txt'.format(refName), 'w')
    a = '''\\begin{{table}}[H]
\\caption{{Shapiro-Wilk Test}}
\\label{{{}}}
\\centering
\\begin{{tabular}}{{ | c | c | }}
\\hline
Series & P-value \\\\
\\hline \\hline'''.format(refName)
    for i in range(len(variables)):
        var = variables[i]
        a += '\n{0} & {1:.3e} \\\\'.format(names[i],
                                           dig.acorr_ljungbox(var, lags=1)[1][0])
        a += '\n\\hline'
    a += '''\n\\end{tabular}
\\end{table}'''
    b.write(a)
    b.close()

# Tabela com limites da análise paramétrica
def tabP(refName, variables = [], names = []):
    b = open('latex/tables/{}.txt'.format(refName), 'w')
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
    b = open('latex/tables/{}.txt'.format(refName), 'w')
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

def outside(refName, ec, csd, lim, di = False , np = False):
    dias = []
    
    if di == False:
        cupom = 'OC1'
    else:
        cupom = 'DI1'

    if np == False:
        anal = 'Parametric'
    else:
        anal = 'Non Parametric'

    b = open('tables/{}.txt'.format(refName), 'w')
    a = '''\\begin{{table}}[H]
\\caption{{Days with Abnormal Returns for {} Exchange Coupon by {} Analysis}}
\\label{{tab:{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | c | c | c |}}
\\hline
& Date & Exchange Coupon & CSD & Lower Limit & Upper Limit \\\\
\\hline \\hline'''.format(cupom, anal, refName)
    n = 0
    for i in range(len(csd.index)):
        poxa = csd.index[i]
        date = '{}/{}/{}'.format(str(poxa)[:4], str(poxa)[5:7], str(poxa)[8:10])
        if csd[i] > lim.UpperLimit[i]:
            n += 1
            dias.append(lim.index[i])
            a += '\n{0} & {1} & {2:.3f} & {3:.3f} & {4:.3f} & {5:.3f}\\\\'.format(n,
                                                                                  date,
                                                                                  ec.valor[i],
                                                                                  csd[i],
                                                                                  lim.LowerLimit[i],
                                                                                  lim.UpperLimit[i])
            a += '\n\\hline'
        elif csd[i] < lim.LowerLimit[i]:
            n += 1
            dias.append(lim.index[i])
            a += '\n{0} & {1} & {2:.3f} & {3:.3f} & {4:.3f} & {5:.3f}\\\\'.format(n,
                                                                                  csd.index[i],
                                                                                  ec.valor[i],
                                                                                  csd[i],
                                                                                  lim.LowerLimit[i],
                                                                                  lim.UpperLimit[i])
            a += '\n\\hline'
    a += '''\n\\end{tabular}
\\end{table}'''
    b.write(a)
    b.close()
    return(dias)

# pega os dias e as noticias selecionadas e exporta uma tabela com as noticias para cada dia de volatilidade anormal
def noticia_para_cada_dia(refName, dias, noticias, np = False):
    diass = list()
    for poxa in dias:
        diass.append('{}/{}/{}'.format(str(poxa)[8:10], str(poxa)[5:7], str(poxa)[:4]))

    lista = list()
    if np == False:
        anal = 'Parametric'
    else:
        anal = 'Non Parametric'

    b = open('tables/{}.txt'.format(refName), 'w')
    a = '''\\begin{{longtable}}{{ | c | c | c | c | }}
\\caption{{Political News in Days of Abnormal Volatility by {} Analysis}}
\\label{{tab:{}}}
\\hline \\multicolumn{{1}}{{|c|}}{{\\textbf{{}}}} & \\multicolumn{{1}}{{c|}}{{\\textbf{{Ab. Vol.}}}} & \\multicolumn{{1}}{{c|}}{{\\textbf{{News Time}}}} & \\multicolumn{{1}}{{c|}}{{\\textbf{{Headline}}}} \\\\ \\hline \\hline
\\endfirsthead
\\multicolumn{{4}}{{c}}%
{{{{\\bfseries \\tablename\\ \\thetable{{}} -- continued from previous page}}}} \\\\
\\hline \\multicolumn{{1}}{{|c|}}{{\\textbf{{}}}} & \\multicolumn{{1}}{{c|}}{{\\textbf{{Ab. Vol.}}}} & \\multicolumn{{1}}{{c|}}{{\\textbf{{News Time}}}} & \\multicolumn{{1}}{{c|}}{{\\textbf{{Headline}}}} \\\\ \\hline \\hline
\\endhead
\\hline \\hline \\multicolumn{{4}}{{| r |}}{{{{Continued on next page}}}} \\\\ \\hline
\\endfoot
\\hline \\hline \\multicolumn{{4}}{{| r |}}{{End of table}} \\\\ \\hline
\\endlastfoot'''.format(anal, refName)
    n = 0
    for dia in diass:
        for noticia in noticias:
            if (dia in noticia[7:17]):
                data_cupom = '{}/{}/{}'.format(noticia[13:17], noticia[10:12], noticia[7:9])
                data_hora_noticia = '{}/{}/{} {}:{}'.format(noticia[33:37], noticia[30:32], noticia[27:29], noticia[45:47], noticia[57:59])
                n += 1
                a += '\n{} & {} & {} & {}[...] \\\\'.format(n, data_cupom, data_hora_noticia, noticia[noticia.find('titulo')+8:noticia.find('titulo')+49])
                a += '\n\\hline'
                lista.append(noticia)
    a += '''\n\\end{longtable}'''
    b.write(a)
    b.close()
    return(lista)


