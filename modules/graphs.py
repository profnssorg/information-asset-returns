'''
NOME: Some Evidence on Political  Information and Exchange Coupon in Brazil  -
      Graph Module
AUTHOR: Bernardo Paulsen
DATE: 2019/06/24
VERSION: 1.1.0
LINK: https://github.com/profnssorg/information-asset-returns

DESCRIPTION: Class for the output of graphs' image and latex text

'''


######## IMPORTING PACKAGES ########


from matplotlib import pyplot as plt # graphs
from matplotlib import dates as mdates # dates on graphs
#import numpy as np # arrays
#import pandas as pd # Series


######## DEFINING CLASS ########


class Graph():

    '''
    CLASS FOR THE OUTPUT OF GRAPHS

    Output graphs of pandas.Series (.png and .txt for use in LaTeX).

    Methods
    -------
    series : outputs graph with one or multiple series
        Outputs graph's .png and .txt files.

    multiple : calls Graph.series method for multiple graphs
        Outputs graphs' .png and .txt files.
    '''

    def series(series = list(),
               legends = list(),
               y_axis = str(),
               title = str(),
               label = str()):

        '''
        GRAPH FOR ONE OR MULTIPLE SERIES

        Outputs graphs' .png image (saved at .latex/graphs/) and .txt LaTeX
        text (saved at ./latex/graphstext/).

        Parameters
        ----------
        series : list of pandas.Series objects
            Maxim lenght of 4. A ll objects will be  plotted in the same color
            and axis, but in different line styles.

        legends : list of strings, optional
            Legends to  be  displayed in the  graph. This list  myst be of the
            same lenght as the  series list, as each  Series will be assing to 
            the correpondent legend. If null, no legend is be displayed.

        y_axis : string, optional
            Name of y axis.

        title : string, optional
            LaTeX title of graph.

        label : string, optional
            LaTeX label for graph.

        Returns
        -------
        image : .png
            Image with graph

        text: .txt
            LaTeX text for the graph

        '''
        
        lines = ['solid', 'dashed', 'dashdot', 'dotted']
        
        for i in range(len(series)):
            ax = series[i].plot(figsize = (8,5), color = 'black',
                linestyle = lines[i])
        if legends:
            ax.legend(legends)
        ax.grid(axis = 'x')
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
        plt.gcf().autofmt_xdate()
        plt.xlabel('Date')
        if yaxis:
            plt.ylabel(y_axis)
        if label:
            plt.savefig('latex/graphs/{}'.format(label), dpi = 200)
        plt.show()
        if label:
            a = open('latex/graphstext/{}.txt'.format(label), 'w')
            a.write('''\\begin{{figure}}[H]
\\caption{{{0}}}
\\label{{fig:{1}}}
\\centering
\\includegraphics[width=\\textwidth]{{graphs/{1}.png}}
\\end{{figure}}'''.format(title, label))
            a.close()
        
    def multiple(tup = tuple()):


        '''
        FOR VARIOUS GRAPHS

        Calls Graph.series method multiple times.

        Parameters
        ----------
        tup : tuple
            Each    element    shall    have    the    same    structure    of 
            Graph.series' parameters.

        Returns
        -------
        image : .png
            Images for each graph

        text: .txt
            LaTeX text for each graph

        '''

        for i in range(len(tup)):
            Graph.series(tup[i][0],
                        tup[i][1],
                        tup[i][2],
                        tup[i][3],
                        tup[i][4],)

