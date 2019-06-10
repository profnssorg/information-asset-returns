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
from modules import import_process # module for importing and trasnforming data
from modules import process_output_graphs # muodule for output of graphs
from modules import process_output_tables # module for output of tables
#
# IMPORT DATA ------------------------------------------------------------------
#
# NUMBERS OF SERIES
sgs_numbers = [1, 11, 12]

# INITIAL DATE FOR SERIES
sgs_initial_date = '26/09/2016'

# FINAL DATE FOR SERIES
sgs_final_date = '16/05/2019'

#
# PRECESS DATA -----------------------------------------------------------------
#
# Scrapping
os.system('scrapy crawl g1 -o noticias.json')

# CREATES DATAFRAM WITH SERIES FROM BACEN-SGS
BASE = bacen_sgs_api(names = ['Ptax', 'Selic', 'Di'],
                     numbers = sgs_numbers,
                     initial_date = sgs_initial_date,
                     final_date = sgs_final_date)

# APPENDS EXCHANGE COUPONS TO DATAFRAME
exchange_coupon(BASE, 0, [1, 2], ['Oc1', 'Di1'])

# APPENDS GARCH'S CSD AND RESIDUALS OF EXCHANGE COUPONS TO DATAFRAME
garch(BASE, [3,4])

# APPENDS LIMITS FROM BOTH PARAMETRIC AND NON PARAMETRIC ANALYSIS FOR BOTH MEASU
#RES OF EXCHANGE COUPON TO DATAGRAME
limits(BASE, [5, 7])

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

# OUTPUT DATA ------------------------------------------------------------------

#       PTAX, SELIC AND DI -----------------------------------------------------

# GRAPH FOR PTAX
graph([BASE.Ptax],
      [],
      'PTAX',
      'Dollar Exchange Rate',
      'ptax')

# GRAPH FOR SELIC
graph(BASE.Selic,
      [],
      'Selic',
      'Referential Rate of the Special Settlement and Custody System',
      'selic')

# GRAPH FOR DI
graph(BASE.Di,
      [],
      'DI',
      'Interbank Deposit Rate',
      'di')

# DESCRIPTIVE STATISTICS TABLE FOR PTAX, SELIC AND DI
des('PTAX, Selic and DI',
    'desptaxselicdi',
    [BASE.Ptax, BASE.Selic, BASE.Di],
    ['PTAX', 'Selic', 'DI'])

#       EXCHANGE COUPONS -------------------------------------------------------

graph([BASE.Oc1],
      [],
      'OC1',
      'OC1 Exchange Coupon',
      'oc')
graph([BASE.Di1],
      [],
      'DI1',
      'DI1 Exchange Coupon',
      'di1')

des('OC1 and DI1 Exchange Coupons',
    'desocdi',
    [BASE.Oc1, BASE.Di1],
    ['OC1', 'DI1'])
adf('ocdiadf',
    [BASE.Oc1, BASE.Di1],
    ['OC1', 'DI1'])
kpss('ocdikpss',
    [BASE.Oc1, BASE.Di1],
    ['OC1', 'DI1'])


#		4_2_2 ESTIMATION -----------------------------------------------

ljungShapiro('reswhite',
             [BASE.Oc1Res, BASE.Di1Res],
             ['Residuals of OC1\'s GARCH', 'Residuals of DI1\'s GARCH'])
graph([BASE.Oc1Res],
      [],
      'Residuals',
      'Residuals of OC1\'s GARCH',
      'ocres')
graph([BASE.Di1Res],
      [],
      'Residuals',
      'Residuals of DI1\'s GARCH',
      'dires')

funcao(BASE.Oc1, 'OC1 Exchange Coupon', 'oc')
funcao(BASE.Di1, 'DI1 Exchange Coupon', 'di')
funcao(BASE.Oc1Res, 'Residuals of OC1', 'ocres', True)
funcao(BASE.Di1Res, 'Residuals of DI1', 'dires', True)


#		4_2_3 VOLATILITY ESTIMATE -------------------------------------

graph([BASE.Oc1Csd],
      [],
      'CSD',
      'OC1\'s CSD',
      'occsd')
graph([BASE.Di1Csd],
      [],
      'CSD',
      'DI1\'s CSD',
      'dicsd')
des('OC1 and DI1\'s CSD',
    'descsd',
    [BASE.Oc1Csd, BASE.Di1Csd],
    ['OC1\'s CSD', 'DI1\'s CSD'])
#
#		------------------------------------- 4_2_3 VOLATILITY ESTIMATE
#
#
#		4_2_4 PARAMETRIC ----------------------------------------------
#
# Gráfico e tabela análise paramétrica
shapiro('csdshapiro',
        [ResultadoGarchOC.conditional_volatility, ResultadoGarchDI.conditional_volatility],
        ['OC1\'s CSD', 'DI1\'s CSD'])
# TABELA COM LIMITES PARAMETRICOS PARA CSDs DE OC E DI
tabP('limpar',
     [OCP, DIP],
     ['OC1\'s CSD', 'DI1\'s CSD'])
# GRAFICO COM LIMITES PARAMETRICOS PARA CSD DE OC
graph([BASE.Oc1Csd, BASE.Oc1CsdParUp, BASE.Oc1CsdParLo],
      ['CSD', 'Upper Limit', 'Lower Limit'],
      'CSD',
      'Parametric Limits for OC1\'s CSD',
      'oclimpar')
graph([BASE.Di1Csd, BASE.Di1CsdParUp, BASE.Di1CsdParLo],
      ['CSD', 'Upper Limit', 'Lower Limit'],
      'CSD',
      'Parametric Limits for OC1\'s CSD',
      'oclimpar')
#oc_out_par = outside('ocparout',
#                     CupomCambialOC,
#                     ResultadoGarchOC.conditional_volatility,
#                     DIP)
#di_out_par = outside('diparout',
#        CupomCambialDI,
#        ResultadoGarchDI.conditional_volatility,
#        DIP, True)
#
#		---------------------------------------------- 4_2_4 PARAMETRIC
#
#
#   4_2_5 NON PARAMETRIC ------------------------------------------
#
tabNP('limnon',
     [OCnP, DInP],
     ['OC1\'s CSD', 'DI1\'s CSD'])
graph(ResultadoGarchOC.conditional_volatility,
      'CSD',
      'Non-Parametric Limits for OC1\'s CSD',
      'oclimnon',
      limit = True,
      non = True)
graph(ResultadoGarchDI.conditional_volatility,
      'CSD',
      'Non-Parametric Limits for DI1\'s CSD',
      'dilimnon',
      limit = True,
      non = True)
oc_out_non = outside('ocnonout',
                     CupomCambialOC,
                     ResultadoGarchOC.conditional_volatility,
                     OCnP,
                     np = True)
di_out_non = outside('dinonout',
                     CupomCambialDI,
                     ResultadoGarchDI.conditional_volatility,
                     DInP,
                     True,
                     True)
#
#   ------------------------------------------ 4_2_5 NON PARAMETRIC
#
#
#   5 RESULTS -----------------------------------------------------
#
noticias_relevantes = transformar(separar_noticias(juntar(corrigir(datas_do_ano(), PTAX), proximodia(arrumar(noticias('noticias.json')), lista_datas(corrigir(datas_do_ano(), PTAX)))), ['incerteza',
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

a = noticia_para_cada_dia('parnews', oc_out_par, noticias_relevantes)
b = noticia_para_cada_dia('nonnews', oc_out_non, noticias_relevantes, np = True)
#
#   ----------------------------------------------------- 5 RESULTS
#
os.system('cd latex')
os.system('xelatex main')
