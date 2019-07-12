'''
NOME: Some Evidence on Political Information and Exchange Coupon in Brazil -
      Tables Module
AUTHOR: Bernardo Paulsen
DATE: 2019/06/24
VERSION: 1.0.0
LINK: https://github.com/profnssorg/information-asset-returns

DESCRIPTION: Class for the output of latex tables

'''


######## IMPORT PACKAGES ########


#import numpy as np # api - array used for series and dataframe data structures
                   # fundamental package for scientific computing
#import pandas as pd # api - series and datagrame data structues & various 
                    # data structures and data analysis tools
import statsmodels.tsa.stattools as stat # adf, kpss, shapito white
import statsmodels.stats.diagnostic as dig #ljung box


######## CLASS DEFINITION ########


class Tables():

    '''THIS CLASS HAS METHODS TO EXPORT TABLES'''
    
    def __init__(self):
        
        self.init = 'OK'

    def des(title = str(), # series names for input in table's title
            label = str(),
            series = list(),
            names = list()):

        '''TABLE WITH DESCRIPTIVE STATISTICS'''

        b = open('latex/tables/{}.txt'.format(label), 'w')
        a = '''\\begin{{table}}[H]
\\caption{{Descriptive Statistics for {}}}
\\label{{tab:{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | c | c | }}
\\hline
Series & Mean & Standard Deviation & Minimum Value & Maximum Value \\\\
\\hline \\hline'''.format(title, label)
        for i in range(len(series)):
            var = series[i]
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

    def adf(label = str(),
            series = list(),
            names = list()):

        '''TABLE FOR AUGMENTED DICKEY-FULLER TEST'''

        b = open('latex/tables/{}.txt'.format(label), 'w')
        a = '''\\begin{{table}}[H]
\\caption{{Augmented Dickey-Fuller Test}}
\\label{{tab:{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | }}
\\hline
Series & Test Statistic & Critical Value at 5\% Level \\\\
\\hline \\hline'''.format(label)
        for i in range(len(series)):
            adf = stat.adfuller(series[i][1:])
            a += '\n{0} & {1:.3e} & {2:.3e} \\\\'.format(names[i],
                                                         adf[0],
                                                         adf[4]['5%'])
            a += '\n\\hline'
        a += '''\n\\end{tabular}
\\end{table}'''
        b.write(a)
        b.close()

    def kpss(label = str(),
             variables = list(),
             names = list()):

        '''TABLE FOR KWIATKOWSKI-PHILLIPS-SCHMIDT-SHIN TEST'''

        b = open('latex/tables/{}.txt'.format(label), 'w')
        a = '''\\begin{{table}}[H]
\\caption{{Kwiatkowski–Phillips–Schmidt–Shin Test}}
\\label{{tab:{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | }}
\\hline
Series & Test Statistic & Critical Value at 5\% Level \\\\
\\hline \\hline'''.format(label)
        for i in range(len(variables)):
            kpss = stat.kpss(variables[i][1:])
            a += '\n{0} & {1:.3e} & {2:.3e} \\\\'.format(names[i],
                                                         kpss[0],
                                                         kpss[3]['5%'])
            a += '\n\\hline'
        a += '''\n\\end{tabular}
    \\end{table}'''
        b.write(a)
        b.close()

    def ljung(label = str(),
                     variables = list(),
                     names = list()):

        '''TABLE FOR LJUNG-BOX AND SHAPIRO-WILK TESTS'''

        b = open('latex/tables/{}.txt'.format(label), 'w')
        a = '''\\begin{{table}}[H]
\\caption{{Ljung-Box Test}
\\label{{tab:{}}}
\\centering
\\begin{{tabular}}{{ | c | c | }}
\\hline
Series & P-value \\\\
\\hline \\hline'''.format(label)
        for i in range(len(variables)):
            var = variables[i][1:]
            a += '\n{0} & {1:.3e} \\\\'.format(names[i],
                                                         dig.acorr_ljungbox(var)[1][39])
            a += '\n\\hline'
        a += '''\n\\end{tabular}
\\end{table}'''
        b.write(a)
        b.close()

    def shapiro(label = str(),
                variables = list(),
                names = list()):

        '''TABLE FOR SHAPIRO-WILK TEST'''

        b = open('latex/tables/{}.txt'.format(label), 'w')
        a = '''\\begin{{table}}[H]
\\caption{{Shapiro-Wilk Test}}
\\label{{tab:{}}}
\\centering
\\begin{{tabular}}{{ | c | c | }}
\\hline
Series & P-value \\\\
\\hline \\hline'''.format(label)
        for i in range(len(variables)):
            var = variables[i][1:]
            a += '\n{0} & {1:.3e} \\\\'.format(names[i],
                                               stats.shapiro(var)[1])
            a += '\n\\hline'
        a += '''\n\\end{tabular}
\\end{table}'''
        b.write(a)
        b.close()

    def limits(label = str(),
                  upper_limits = list(),
                  lower_limits = list(),
                  names = list(),
                  par = True):

        '''TABLE WITH LIMITS'''

        if par == True:
            title = 'Parametric'
            up = 'Upper Limit'
            lo = 'Lower Limit'
        else:
            title = 'Non Parametric'
            up = 'Mean of Upper Limits'
            lo = 'Mean of Lower Limits'

        b = open('latex/tables/{}.txt'.format(label), 'w')
        a = '''\\begin{{table}}[H]
\\caption{{Limits from {} Analysis}}
\\label{{tab:{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | c | c | }}
\\hline
Series & {} & {} \\\\
\\hline \\hline'''.format(title, label, up, lo)
        for i in range(len(upper_limits)):
            upper = upper_limits[i]
            lower = lower_limits[i]
            a += '\n{0} & {1:.3f} & {2:.3f} \\\\'.format(names[i],
                                                         upper.mean(),
                                                         lower.mean())
            a += '\n\\hline'
        a += '''\n\\end{tabular}
\\end{table}'''
        b.write(a)
        b.close()

    def outside(label = str(),
                df = pd.DataFrame(),
                ec = str(),
                csd = str(),
                limits = list(),
                di = False ,
                non = False):

        '''TABLE WITH DAYS WITH ABNORMAL VOLATILITY'''

        exc_cou = df[ec]
        con_std = df[csd]
        upp_lim = df[limits[0]]
        low_lim = df[limits[1]]

        dias = []
        if di == False:
            cupom = 'OC1'
        else:
            cupom = 'DI1'

        if non == False:
            anal = 'Parametric'
        else:
            anal = 'Non Parametric'

        b = open('latex/tables/{}.txt'.format(label), 'w')
        a = '''\\begin{{table}}[H]
\\caption{{Days with Abnormal Returns for {} Exchange Coupon by {} Analysis}}
\\label{{tab:{}}}
\\centering
\\begin{{tabular}}{{ | c | c | c | c | c | c |}}
\\hline
& Date & Exchange Coupon & CSD & Lower Limit & Upper Limit \\\\
\\hline \\hline'''.format(cupom, anal, label)
        n = 0
        for i in range(len(con_std.index)):
            if con_std[i] > upp_lim[i] or con_std[i] < low_lim[i]:
                poxa = con_std.index[i]
                date = '{}/{}/{}'.format(str(poxa)[:4], str(poxa)[5:7], str(poxa)[8:10])
                n += 1
                dias.append(upp_lim.index[i])
                a += '\n{0} & {1} & {2:.3f} & {3:.3f} & {4:.3f} & {5:.3f}\\\\'.format(n,
                                                                                      date,
                                                                                      exc_cou[i],
                                                                                      con_std[i],
                                                                                      low_lim[i],
                                                                                      upp_lim[i])
                a += '\n\\hline'
        a += '''\n\\end{tabular}
\\end{table}'''
        b.write(a)
        b.close()
        return(dias)
    
    def noticia_para_cada_dia(refName, dias, noticias, np = False):
        diass = list()
        for poxa in dias:
            diass.append('{}/{}/{}'.format(str(poxa)[8:10], str(poxa)[5:7], str(poxa)[:4]))

        lista = list()
        if np == False:
            anal = 'Parametric'
        else:
            anal = 'Non Parametric'

        b = open('latex/tables/{}.txt'.format(refName), 'w')
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
                    data_hora_noticia = '{}/{} {}:{}'.format(noticia[30:32], noticia[27:29], noticia[45:47], noticia[57:59])
                    n += 1
                    a += '\n{} & {} & {} & {}[...] \\\\'.format(n, data_cupom, data_hora_noticia, noticia[noticia.find('titulo')+8:noticia.find('titulo')+49])
                    a += '\n\\hline'
                    lista.append(noticia)
        a += '''\n\\end{longtable}'''
        b.write(a)
        b.close()
        return(lista)