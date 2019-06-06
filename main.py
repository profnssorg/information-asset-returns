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
from arch import arch_model # garch model
#import statsmodels.tsa.stattools as stat # adf, kpss, shapito white
#import statsmodels.stats.diagnostic as dig #ljung box
#from scipy import stats # confidence interval
#
# Output data
#	Graphs
#from matplotlib import pyplot as plt # graphs
#
#----------------------------------------------------------------IMPORT PACKAGES
#
#
# IMPORT MODULES ---------------------------------------------------------------
#
from modules import import_process # module for importing and trasnforming data
from modules import process_output_graphs # muodule for output of graphs
from modules import process_output_tables # module for output of tables
#
#-----------------------------------------------------------------IMPORT MODULES
#
#
# OBJECTS ----------------------------------------------------------------------
#
data_inicial = str() # initial date for use in the time series collection via API
data_final - str() # data final para a  serie temporal que sera coletada

PTAX = pd.DataFrame() # data frame que contera a serie temporal de cambio (PTAX)
Selic = pd.DataFrame() # data frame que contera a serie temporal de juros Selic
DI = pd.DataFrame() # data frame que contera a serie temporal de juros DI

CupomCambialOC = pd.DataFrame() # data frame que contera a serie temporal do cu_
                                # pom cambial de oc1
CupomCambialDI = pd.DataFrame() # data frame que contera a serie temporal do cu_
                                # pom cambial de di1

#ResultadoGarchOC = # resultado da estimacao do garch para o cupom cambial de oc1
#ResultadoGarchDI = # resultado da estimacao do garch para o cupom cambial de oc1

OCP = pd.DataFrame() # data frame que contera as series temporais dos limites p_
                     # arametricos para o cupom cambial de oc1
DIP = pd.DataFrame() # data frame que contera as series temporais dos limites p_
                     # arametricos para o cupom cambial de di1
OCnP = pd.DataFrame() # data frame que contera as series temporais dos limites 
                      # nao parametricos para o cupom cambial de oc1
DInP = pd.DataFrame() # data frame que contera as series temporais dos limites
                      # nao parametricos para o cupom cambial de di1


#
#------------------------------------------------------------------------OBJECTS
#
#
# IMPUT DATA -------------------------------------------------------------------
#
# Initial and final date for the api data
data_inicial = '26/09/2016'
data_final = '16/05/2019'
#
#---------------------------------------------------------------------INPUT DATA
#
#
# PROCESS DATA -----------------------------------------------------------------
#
# Scrapping
os.system('scrapy crawl g1 -o noticias.json')
# Creates time series objects
PTAX = serie(1, data_inicial, data_final)
Selic = serie(11, data_inicial, data_final)
DI = serie(12, data_inicial, data_final)
#
# Crates exchange coupon data frame objects
CupomCambialOC = cupomCambial(Selic, PTAX)
CupomCambialDI = cupomCambial(DI, PTAX)
#
# Creates estimted garch objects
ResultadoGarchOC = arch_model(CupomCambialOC.valor).fit()
ResultadoGarchDI = arch_model(CupomCambialDI.valor).fit()
# Creates parametric limits data frame objects
OCP = limitP(ResultadoGarchOC.conditional_volatility)
DIP = limitP(ResultadoGarchDI.conditional_volatility)
# Creates pon arametric limits data frame objects
OCnP = limitNP(ResultadoGarchOC.conditional_volatility)
DInP = limitNP(ResultadoGarchDI.conditional_volatility)
# Creates list with relevant news
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
                                                    'presid\\u00eancia']))

os.system('cd latex')
os.system('xelatex main')

#
#-------------------------------------------------------------------PROCESS DATA
#
#
# EXPORT DATA ------------------------------------------------------------------
#
#
#		4_1_2 EXCHANGE COUPON ------------------------------------------
#
#
#				ptax selic di ----------------------------------
#
graph(PTAX,
      'PTAX',
      'Dollar Exchange Rate',
      'ptax')
graph(Selic,
      'Selic',
      'Referential Rate of the Special Settlement and Custody System',
      'selic')
graph(DI,
      'DI',
      'Interbank Deposit Rate',
      'di')
des('PTAX, Selic and DI',
    'desptaxselicdi',
    [PTAX, Selic, DI],
    ['PTAX', 'Selic', 'DI'])
#
#				---------------------------------- ptax selic di
#
#
#				oc di ------------------------------------------
#
graph(CupomCambialOC,
      'OC1',
      'OC1 Exchange Coupon',
      'oc')
graph(CupomCambialDI,
      'DI1',
      'DI1 Exchange Coupon',
      'di1')
des('OC1 and DI1 Exchange Coupons',
    'desocdi',
    [CupomCambialOC, CupomCambialDI],
    ['OC1', 'DI1'])
adf('ocdiadf',
    [CupomCambialOC, CupomCambialDI],
    ['OC1', 'DI1'])
kpss('ocdikpss',
    [CupomCambialOC, CupomCambialDI],
    ['OC1', 'DI1'])
#
#				------------------------------------------ oc di
#
#
#		------------------------------------------ 4_1_2 EXCHANGE COUPON
#
#
#		4_2_2 ESTIMATION -----------------------------------------------
#
ljungShapiro('reswhite',
             [ResultadoGarchOC.resid, ResultadoGarchDI.resid],
             ['Residuals of OC1\'s GARCH', 'Residuals of DI1\'s GARCH'])
graph(ResultadoGarchOC.resid,
      'Residuals',
      'Residuals of OC1\'s GARCH',
      'ocres')
graph(ResultadoGarchDI.resid,
      'Residuals',
      'Residuals of DI1\'s GARCH',
      'dires')
funcao(CupomCambialOC, 'OC1 Exchange Coupon', 'oc', True)
funcao(CupomCambialDI, 'DI1 Exchange Coupon', 'di', True)
funcao(ResultadoGarchOC.resid, 'Residuals of OC1', 'ocres')
funcao(ResultadoGarchDI.resid, 'Residuals of DI1', 'dires')

#
#		---------------------------------------------- 4_2_2 ESTIMATION
#
#
#		4_2_3 VOLATILITY ESTIMATE -------------------------------------
#
graph(ResultadoGarchOC.conditional_volatility,
      'CSD',
      'OC1\'s CSD',
      'occsd')
graph(ResultadoGarchDI.conditional_volatility,
      'CSD',
      'DI1\'s CSD',
      'dicsd')
des('OC1 and DI1\'s CSD',
    'descsd',
    [ResultadoGarchOC.conditional_volatility, ResultadoGarchDI.conditional_volatility],
    ['OC1\'s CSD', 'DI1\'s CSD'],
    csd = True)
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
graph(ResultadoGarchOC.conditional_volatility,
      'CSD',
      'Parametric Limits for OC1\'s CSD',
      'oclimpar',
      limit = True)
graph(ResultadoGarchDI.conditional_volatility,
      'CSD',
      'Parametric Limits for DI1\'s CSD',
      'dilimpar',
      limit = True)
oc_out_par = outside('ocparout',
                     CupomCambialOC,
                     ResultadoGarchOC.conditional_volatility,
                     DIP)
di_out_par = outside('diparout',
        CupomCambialDI,
        ResultadoGarchDI.conditional_volatility,
        DIP, True)
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
