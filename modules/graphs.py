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

