
# TIME SERIES GRAPH
def graph(df, yName, graphName, refName, limit = False, non = False):
    if limit == True:
        if non == False:
            limitP(df).plot(figsize = (8,5))
        else:
            limitNP(df).plot(figsize = (8,5))
    ax = df.plot(figsize = (8,5))
    ax.grid(axis = 'x')
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
    plt.gcf().autofmt_xdate()
    plt.xlabel('Date')
    plt.ylabel(yName)
    plt.savefig('graphs/{}'.format(refName), dpi = 200)
    plt.show()

    a = open('graphstext/{}.txt'.format(refName), 'w')
    a.write('''\\begin{{figure}}[H]
\\caption{{{0}}}
\\label{{fig:{1}}}
\\centering
\\includegraphics[width=\\textwidth]{{graphs/{1}.png}}
\\end{{figure}}'''.format(graphName, refName))
    a.close()  

# ACF AND PACF GRAPHS
def funcao(serie, graphName, refName, pacf = False):
    cima = []
    baixo = []
    for i in stat.acf(serie, alpha = .05)[1]:
        cima.append(i[0])
        baixo.append(i[1])
    va = {'cima': cima, 'baixo': baixo}
    a = pd.DataFrame(va)

    serieum = pd.Series(stat.acf(serie, alpha = .05)[0])
    serieum.plot(figsize = (8,5), kind = 'bar')
    plt.plot(a)
    plt.xlabel('Lag')
    plt.ylabel('ACF')
    plt.legend(('97.5%', '2.5%'))
    plt.savefig('graphs/{}acf'.format(refName))
    plt.show()

    if pacf == True:
        cima = []
        baixo = []
        for i in stat.pacf(serie, alpha = .05)[1]:
            cima.append(i[0])
            baixo.append(i[1])
        va = {'cima': cima, 'baixo': baixo}
        a = pd.DataFrame(va)

        serieum = pd.Series(stat.pacf(serie, alpha = .05)[0])
        serieum.plot(figsize = (8,5), kind = 'bar')
        plt.plot(a)
        plt.xlabel('Lag')
        plt.ylabel('PACF')
        plt.legend(('97.5%', '2.5%'))
        plt.savefig('graphs/{}pacf'.format(refName))
        plt.show()
    
    a = open('graphstext/{}acf.txt'.format(refName), 'w')
    a.write('''\\begin{{figure}}[H]
\\caption{{Auto-Correlation Funcion for {0}}}
\\label{{fig:{1}acf}}
\\centering
\\includegraphics[width=\\textwidth]{{graphs/{1}acf.png}}
\\end{{figure}}'''.format(graphName, refName))
    a.close() 

    if pacf == True:
        a = open('graphstext/{}pacf.txt'.format(refName), 'w')
        a.write('''\\begin{{figure}}[H]
\\caption{{Partial Auto-Correlation Funcion for {0}}}
\\label{{fig:{1}pacf}}
\\centering
\\includegraphics[width=\\textwidth]{{graphs/{1}pacf.png}}
\\end{{figure}}'''.format(graphName, refName))
        a.close() 
