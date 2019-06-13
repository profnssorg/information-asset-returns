'''

github : https://github.com/profnssorg/information-asset-returns

'''
#
# IMPORT PACKAGES --------------------------------------------------------------
#
# Impoprt (and transform) data
import os # scrapping - os run command
#import scrapy # scrapping - package
#import numpy as np # api - array used for series and dataframe data structures
                   # fundamental package for scientific computing
#import pandas as pd # api - series and datagrame data structues & various 
                    # data structures and data analysis tools
#
# Transform data
#from arch import arch_model # garch model
#import statsmodels.tsa.stattools as stat # adf, kpss, shapito white
#import statsmodels.stats.diagnostic as dig #ljung box
#from scipy import stats # confidence interval
#
# Output data
#	Graphs
#from matplotlib import pyplot as plt # graphs
#import matplotlib.dates as mdates
#
# IMPORT MODULES ---------------------------------------------------------------
#
from modules import importbacen # module for importing data from BACEN SGS
from modules import calculations # module for calculations with time series
from modules import graphs # muodule for output of graphs
from modules import tables # module for output of tables
from modules import news # module for dealing with news
#
# IMPORT DATA ------------------------------------------------------------------
#
# NUMBERS OF SERIES
#sgs_numbers = [1, 11, 12]

# INITIAL DATE FOR SERIES
#sgs_initial_date = '26/09/2016'

# FINAL DATE FOR SERIES
#sgs_final_date = '16/05/2019'

#
# PRECESS DATA -----------------------------------------------------------------
#
# Scrapping
#os.system('scrapy crawl g1 -o noticias.json')

# CREATES DATAFRAM WITH SERIES FROM BACEN-SGS
BASE = ImportBacen.create(names = ['Ptax', 'Selic', 'Di'],
                          numbers = [1, 11, 12],
                          initial_date = '26/09/2016',
                          final_date = '16/05/2019')

# APPENDS EXCHANGE COUPONS TO DATAFRAME
Calculations.exchange_coupon(BASE, 0, [1, 2], ['Oc1', 'Di1'])

# APPENDS GARCH'S CSD AND RESIDUALS OF EXCHANGE COUPONS TO DATAFRAME
Calculations.garch(BASE, [3,4])

# APPENDS LIMITS FROM BOTH PARAMETRIC AND NON PARAMETRIC ANALYSIS FOR BOTH MEASU
#RES OF EXCHANGE COUPON TO DATAGRAME
Calculations.limits(BASE, [5, 7])

# Creates list with relevant news
'''
noticias_relevantes = transformar(separar_noticias('noticias.json',
                                                   ['incerteza',
                                                    'mercado',
                                                    'economia',
                                                    'd\\u00f3lar',
                                                    'selic',
                                                    'cdi',
                                                    'c\\u00e2mara',
                                                    'senado'
                                                    'stf'
                                                    'superior tribunal federal'
                                                    'tcu',
                                            'tribunal de contas da uni\\u00e3o',
                                                    'presidente',
                                                    'presid\\u00eancia']))'''

# CREATES LIST WITH RELEVANT NEWS
noticias_relevantes = News.transformar(News.separar_noticias(News.juntar(News.corrigir(News.datas_do_ano(),
                                                                       BASE.Ptax),
                                                              News.proximodia(News.arrumar(News.noticias('noticias.json')),
                                                              News.lista_datas(News.corrigir(News.datas_do_ano(), BASE.Ptax)))),
                                                                    ['incerteza',
                                                                     'mercado',
                                                                     'economia',
                                                                     'd\\u00f3lar',
                                                                     'selic',
                                                                     'cdi',
                                                                     'c\\u00e2mara',
                                                                     'senado'
                                                                     'stf'
                                                                     'superior tribunal federal'
                                                                     'tcu',
                                                                     'tribunal de contas da uni\\u00e3o',
                                                                     'presidente',
                                                                     'presid\\u00eancia']))





# OUTPUT DATA ------------------------------------------------------------------

#       PTAX, SELIC AND DI -----------------------------------------------------

# GRAPH FOR PTAX
Graph.series([BASE.Ptax],
      [],
      'PTAX',
      'Dollar Exchange Rate',
      'ptax')

# GRAPH FOR SELIC
Graph.series([BASE.Selic],
      [],
      'Selic',
      'Referential Rate of the Special Settlement and Custody System',
      'selic')

# GRAPH FOR DI
Graph.series([BASE.Di],
      [],
      'DI',
      'Interbank Deposit Rate',
      'di')

# DESCRIPTIVE STATISTICS TABLE FOR PTAX, SELIC AND DI
Tables.des('PTAX, Selic and DI',
    'desptaxselicdi',
    [BASE.Ptax, BASE.Selic, BASE.Di],
    ['PTAX', 'Selic', 'DI'])

#       EXCHANGE COUPONS -------------------------------------------------------

Graph.series([BASE.Oc1],
      [],
      'OC1',
      'OC1 Exchange Coupon',
      'oc')

Graph.series([BASE.Di1],
      [],
      'DI1',
      'DI1 Exchange Coupon',
      'di1')

Tables.des('OC1 and DI1 Exchange Coupons',
    'desocdi',
    [BASE.Oc1, BASE.Di1],
    ['OC1', 'DI1'])

Tables.adf('ocdiadf',
    [BASE.Oc1, BASE.Di1],
    ['OC1', 'DI1'])

Tables.kpss('ocdikpss',
    [BASE.Oc1, BASE.Di1],
    ['OC1', 'DI1'])


#   4_2_2 ESTIMATION -----------------------------------------------

Tables.ljung_shapiro('reswhite',
             [BASE.Oc1Res, BASE.Di1Res],
             ['Residuals of OC1\'s GARCH', 'Residuals of DI1\'s GARCH'])

Graph.series([BASE.Oc1Res],
      [],
      'Residuals',
      'Residuals of OC1\'s GARCH',
      'ocres')

Graph.series([BASE.Di1Res],
      [],
      'Residuals',
      'Residuals of DI1\'s GARCH',
      'dires')

Graph.acf_pacf(BASE.Oc1, 'OC1 Exchange Coupon', 'oc', True)

Graph.acf_pacf(BASE.Di1, 'DI1 Exchange Coupon', 'di', True)

Graph.acf_pacf(BASE.Oc1Res, 'Residuals of OC1', 'ocres')

Graph.acf_pacf(BASE.Di1Res, 'Residuals of DI1', 'dires')


#   4_2_3 VOLATILITY ESTIMATE -------------------------------------

Graph.series([BASE.Oc1Csd],
      [],
      'CSD',
      'OC1\'s CSD',
      'occsd')

Graph.series([BASE.Di1Csd],
      [],
      'CSD',
      'DI1\'s CSD',
      'dicsd')

Tables.des('OC1 and DI1\'s CSD',
    'descsd',
    [BASE.Oc1Csd, BASE.Di1Csd],
    ['OC1\'s CSD', 'DI1\'s CSD'])

#   4_2_4 PARAMETRIC ----------------------------------------------

Tables.shapiro('csdshapiro',
        [BASE.Oc1Csd, BASE.Di1Csd],
        ['OC1\'s CSD', 'DI1\'s CSD'])

Tables.limits('limpar',
          [BASE.Oc1CsdParUp, BASE.Di1CsdParUp],
          [BASE.Oc1CsdParLo, BASE.Di1CsdParLo],
          ['OC1\'s CSD', 'DI1\'s CSD'],
          par = True)

Graph.series([BASE.Oc1Csd, BASE.Oc1CsdParUp, BASE.Oc1CsdParLo],
      ['CSD', 'Upper Limit', 'Lower Limit'],
      'CSD',
      'Parametric Limits for OC1\'s CSD',
      'oclimpar')

Graph.series([BASE.Di1Csd, BASE.Di1CsdParUp, BASE.Di1CsdParLo],
      ['CSD', 'Upper Limit', 'Lower Limit'],
      'CSD',
      'Parametric Limits for DI1\'s CSD',
      'dilimpar')

oc_out_par = Tables.outside('ocparout',
                     BASE,
                     'Oc1',
                     'Oc1Csd',
                     ['Oc1CsdParUp', 'Oc1CsdParLo'],
                     di = False,
                     non = False)
Tables.outside('diparout',
                     BASE,
                     'Di1',
                     'Di1Csd',
                     ['Di1CsdParUp', 'Di1CsdParLo'],
                     di = True,
                     non = False)

#   4_2_5 NON PARAMETRIC ------------------------------------------

Tables.limits('limnon',
          [BASE.Oc1CsdNonUp, BASE.Di1CsdNonUp],
          [BASE.Oc1CsdNonLo, BASE.Di1CsdNonLo],
          ['OC1\'s CSD', 'DI1\'s CSD'],
          par = False)

Graph.series([BASE.Oc1Csd, BASE.Oc1CsdNonUp, BASE.Oc1CsdNonLo],
      ['CSD', 'Upper Limit', 'Lower Limit'],
      'CSD',
      'Non Parametric Limits for OC1\'s CSD',
      'oclimnon')

Graph.series([BASE.Di1Csd, BASE.Di1CsdNonUp, BASE.Di1CsdNonLo],
      ['CSD', 'Upper Limit', 'Lower Limit'],
      'CSD',
      'Non Parametric Limits for DI1\'s CSD',
      'dilimnon')

oc_out_non = Tables.outside('ocnonout',
                     BASE,
                     'Oc1',
                     'Oc1Csd',
                     ['Oc1CsdParUp', 'Oc1CsdParLo'],
                     di = False,
                     non = True)
Tables.outside('dinonout',
                     BASE,
                     'Di1',
                     'Di1Csd',
                     ['Di1CsdNonUp', 'Di1CsdNonLo'],
                     di = True,
                     non = True)

# RESULTS

a = Tables.noticia_para_cada_dia('parnews', oc_out_par, noticias_relevantes)
b = Tables.noticia_para_cada_dia('nonnews', oc_out_non, noticias_relevantes)

#     ---------------------------------------------------

#os.system('cd latex')
#os.system('pdflatex cic-tc')
