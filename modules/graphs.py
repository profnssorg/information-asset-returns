# IMPORT PACKAGES

#import numpy as np # api - array used for series and dataframe data structures
                   # fundamental package for scientific computing
#import pandas as pd # api - series and datagrame data structues & various 
                    # data structures and data analysis tools

from matplotlib import pyplot as plt
import matplotlib.dates as mdates

import statsmodels.tsa.stattools as stat

class Graph():

    '''THIS CLASS HAS METHODS TO EXPORT GRAPHS'''
    
    def __init__(self):
        
        self.init = 'OK'

    def series(series = list(), # list with Series to be plotted
               legends = list(), # legends for Series. if empty, legends are not included
               y_axis = str(), # name of y axis
               title = str(), # title of graphic in LaTeX
               label = str()): # label to use in LaTeX

        '''GRAPH FOR ONE OR MULTIPLE SERIES'''

        for serie in series:
            ax = serie.plot(figsize = (8,5))
        if len(legends) > 0:
            ax.legend(legends)
        ax.grid(axis = 'x')
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
        plt.gcf().autofmt_xdate()
        plt.xlabel('Date')
        plt.ylabel(y_axis)
        plt.savefig('latex/graphs/{}'.format(label), dpi = 200)
        plt.show()

        a = open('latex/graphstext/{}.txt'.format(label), 'w')
        a.write('''\\begin{{figure}}[H]
\\caption{{{0}}}
\\label{{fig:{1}}}
\\centering
\\includegraphics[width=\\textwidth]{{graphs/{1}.png}}
\\end{{figure}}'''.format(title, label))
        a.close()

    def acf_pacf(serie, # Series
                 title,
                 label, 
                 pacf = False): # IF FALSE, RETURNS ONLY ACF GRAPH

        '''GRAPH FOR ACF ND PACF'''

        cima = []
        baixo = []
        for i in stat.acf(serie[1:], alpha = .05)[1]:
            cima.append(i[0])
            baixo.append(i[1])
        va = {'cima': cima, 'baixo': baixo}
        a = pd.DataFrame(va)

        serieum = pd.Series(stat.acf(serie[1:], alpha = .05)[0])
        serieum.plot(figsize = (8,5), kind = 'bar')
        plt.plot(a)
        plt.xlabel('Lag')
        plt.ylabel('ACF')
        plt.legend(('97.5%', '2.5%'))
        plt.savefig('latex/graphs/{}acf'.format(label))
        plt.show()

        if pacf == True:
            cima = []
            baixo = []
            for i in stat.pacf(serie[1:], alpha = .05)[1]:
                cima.append(i[0])
                baixo.append(i[1])
            va = {'cima': cima, 'baixo': baixo}
            a = pd.DataFrame(va)

            serieum = pd.Series(stat.pacf(serie[1:], alpha = .05)[0])
            serieum.plot(figsize = (8,5), kind = 'bar')
            plt.plot(a)
            plt.xlabel('Lag')
            plt.ylabel('PACF')
            plt.legend(('97.5%', '2.5%'))
            plt.savefig('latex/graphs/{}pacf'.format(label))
            plt.show()

        a = open('latex/graphstext/{}acf.txt'.format(label), 'w')
        a.write('''\\begin{{figure}}[H]
\\caption{{Auto-Correlation Funcion for {0}}}
\\label{{fig:{1}acf}}
\\centering
\\includegraphics[width=\\textwidth]{{graphs/{1}acf.png}}
\\end{{figure}}'''.format(title, label))
        a.close() 

        if pacf == True:
            a = open('latex/graphstext/{}pacf.txt'.format(label), 'w')
            a.write('''\\begin{{figure}}[H]
\\caption{{Partial Auto-Correlation Funcion for {0}}}
\\label{{fig:{1}pacf}}
\\centering
\\includegraphics[width=\\textwidth]{{graphs/{1}pacf.png}}
\\end{{figure}}'''.format(title, label))
            a.close() 