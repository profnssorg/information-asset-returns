"""
NOME: Some Evidence on Political  Information and Exchange Coupon in Brazil  -
      Graph Module
AUTHOR: Bernardo Paulsen
DATE: 2019/06/24
VERSION: 2.0.0
LINK: https://github.com/profnssorg/information-asset-returns

DESCRIPTION: Class for the output of graphs' image and latex text

"""


# IMPORTING PACKAGES ########


from matplotlib import pyplot as plt # graphs
from matplotlib import dates as mdates # dates on graphs


# DEFINING CLASS ########


class Graph():

    ''' CLASS FOR THE OUTPUT OF GRAPHS '''

    def __init__(self):

        self.init = 'OK'

    def series(series=list(),  # list with Series to be plotted
        legends=list(),  # legends for Series. if empty, legends are not included
        y_axis=str(),  # name of y axis
        title=str(),  # title of graphic in LaTeX
        label=str()):  # label to use in LaTeX

        lines = ['solid', 'dashed', 'dashdot', 'dotted']

        for i in range(len(series)):
            ax = series[i].plot(figsize=(8, 5), color='black', linestyle=lines[i])
        if len(legends) > 0:
            ax.legend(legends)
        ax.grid(axis='x')
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
        plt.gcf().autofmt_xdate()
        plt.xlabel('Date')
        plt.ylabel(y_axis)
        plt.savefig('latex/graphs/{}'.format(label), dpi=200)
        plt.show()

        a = open('latex/graphstext/{}.txt'.format(label), 'w')
        a.write('''\\begin{{figure}}[H]
\\caption{{{0}}}
\\label{{fig:{1}}}
\\centering
\\includegraphics[width=\\textwidth]{{graphs/{1}.png}}
\\end{{figure}}'''.format(title, label))
        a.close()

    def multiple(tup=tuple()):

        '''FOR VARIOUS GRAPHS '''

        for i in range(len(tup)):
            Graph.series(tup[i][0],
                tup[i][1],
                tup[i][2],
                tup[i][3],
                tup[i][4], )