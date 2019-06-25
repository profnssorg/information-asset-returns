'''
NOME: Some Evidence on Political Information and Exchange Coupon in Brazil - main
AUTHOR: Bernardo Paulsen
DATE: 2019/06/24
VERSION: 1.1.0
LINK: https://github.com/profnssorg/information-asset-returns

DESCRIPTION: Outputs all graphs and tables from the paper

'''


######### IMPORT PACKAGES ########


import os                           # for scrapping - os run command

#import scrapy                      # scrapping - package
#import numpy as np                 # api - array used for series and dataframe
                                    #data structures / fundamental package for s
                                    #cientific computing
#import pandas as pd                # api - series and datagrame data structues /
                                    #various data structures and data analysis to
                                    #ols

#from arch import arch_model        # garch model
#import statsmodels.tsa.stattools as stat
                                    # adf, kpss, shapito white               
#import statsmodels.stats.diagnostic as dig
                                    #ljung box              
#from scipy import stats            # confidence interval

#from matplotlib import pyplot as plt
                                    # graphs                   
#import matplotlib.dates as mdates  # for dates on graphs


######## IMPORT MODULES ########


from modules import importbacen     # module for importing data from BACEN SGS
from modules import calculations    # module for calculations with time series
from modules import graphs          # muodule for output of graphs
from modules import tables          # module for output of tables
from modules import news            # module for dealing with news


######## IMPORT DATA ########


# EXECUTE SCRAPPING
#os.system('scrapy crawl g1 -o noticias.json')

# IMPORT TIME SERIES
BASE = ImportBacen.create(names = ['Ptax', 'Selic', 'Di'],
                          numbers = [1, 11, 12],
                          initial_date = '26/09/2016',
                          final_date = '16/05/2019')


######## PRECESS DATA ########


# APPENDS EXCHANGE COUPONS TO DATAFRAME
Calculations.exchange_coupon(BASE, 0, [1, 2], ['Oc1', 'Di1'])

# APPENDS GARCH'S CSD AND RESIDUALS OF EXCHANGE COUPONS TO DATAFRAME
Calculations.garch(BASE, [3,4])

# APPENDS LIMITS FROM BOTH PARAMETRIC AND NON PARAMETRIC ANALYSIS TO DATAFRAME
Calculations.limits(BASE, [5, 7])

# CREATES LIST WITH RELEVANT NEWS
noticias_relevantes = News.transformar(
    News.separar_noticias(
        News.juntar(
            News.corrigir(
                News.datas_do_ano(),
                BASE.Ptax),
            News.proximodia(
                News.arrumar(
                    News.noticias('noticias.json')),
                News.lista_datas(
                    News.corrigir(
                        News.datas_do_ano(),
                        BASE.Ptax)))),
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


######## OUTPUT DATA ########

#### GRAPHS ####

Graph.multiple((
    
    # GRAPH FOR PTAX
    ([BASE.Ptax], # Series
     [], # Series labels
     'PTAX', # Y axis' name
     'Dollar Exchange Rate', # Title
     'ptax'), # Graph label

    # GRAPH FOR SELIC
    ([BASE.Selic], # Series
     [], # Series labels
     'Selic', # Y axis' name
     'Referential Rate of the Special Settlement and Custody System', # Title
     'selic'), # Graph label

    # GRAPH FOR DI
     ([BASE.Di], # Series
      [], # Series labels
      'DI', # Y axis' name
      'Interbank Deposit Rate', # Title
      'di'), # Graph label

    # GRAPH FOR OC1
    ([BASE.Oc1], # Series
      [], # Series labels
      'OC1', # Y axis' name
      'OC1 Exchange Coupon', # Title
      'oc'), # Graph label

    # GRAPH FOR DI1
    ([BASE.Di1], # Series
      [], # Series labels
      'DI1', # Y axis' name
      'DI1 Exchange Coupon', # Title
      'di1'), # Graph label

    # GRAPH FOR OC1 RESIDUALS
    ([BASE.Oc1Res], # Series
      [], # Series labels
      'Residuals', # Y axis' name
      'Residuals of OC1\'s GARCH', # Title
      'ocres'), # Graph label

    # GRAPH FOR DI1 RESIDUALS
    ([BASE.Di1Res], # Series
      [], # Series labels
      'Residuals', # Y axis' name
      'Residuals of DI1\'s GARCH', # Title
      'dires'), # Graph label

    # GRAPH FOR OC1 CSD
    ([BASE.Oc1Csd], # Series
      [], # Series labels
      'CSD', # Y axis' name
      'OC1\'s Conditional Standard Deviation', # Title
      'occsd'), # Graph label

    # GRAPH FOR DI1 CSD
    ([BASE.Di1Csd], # Series
      [], # Series labels
      'CSD', # Y axis' name
      'DI1\'s Conditional Standard Deviation', # Title
      'dicsd'), # Graph label

    # GRAPH FOR OC1 PARAMETRIC LIMITS
    ([BASE.Oc1Csd, BASE.Oc1CsdParUp, BASE.Oc1CsdParLo], # Series
      ['CSD', 'Upper Limit', 'Lower Limit'], # Series labels
      'CSD', # Y axis' name
      'Parametric Limits for OC1\'s CSD', # Title
      'oclimpar'), # Graph label

    # GRAPH FOR DI1 PARAMETRIC LIMITS
    ([BASE.Di1Csd, BASE.Di1CsdParUp, BASE.Di1CsdParLo], # Series
      ['CSD', 'Upper Limit', 'Lower Limit'], # Series labels
      'CSD', # Y axis' name
      'Parametric Limits for DI1\'s CSD', # Title
      'dilimpar'), # Graph label

    # GRAPH FOR OC1 NON PARAMETRIC LIMITS
    ([BASE.Oc1Csd, BASE.Oc1CsdNonUp, BASE.Oc1CsdNonLo],
      ['CSD', 'Upper Limit', 'Lower Limit'], # Series labels
      'CSD', # Y axis' name
      'Non Parametric Limits for OC1\'s CSD', # Title
      'oclimnon'), # Graph label

    # GRAPH FOR DI1 NON PARAMETRIC LIMITS
    ([BASE.Di1Csd, BASE.Di1CsdNonUp, BASE.Di1CsdNonLo],
      ['CSD', 'Upper Limit', 'Lower Limit'], # Series labels
      'CSD', # Y axis' name
      'Non Parametric Limits for DI1\'s CSD', # Title
      'dilimnon'), # Graph label
    ))

#### TABLES ####

# DESCRIPTIVE STATISTICS FOR PTAX, SELIC AND DI
Tables.des('PTAX, Selic and DI',
    'desptaxselicdi',
    [BASE.Ptax, BASE.Selic, BASE.Di],
    ['PTAX', 'Selic', 'DI'])

# DESCRIPTIVE STATISTICS FOR OC1 AND DI1
Tables.des('OC1 and DI1 Exchange Coupons',
    'desocdi',
    [BASE.Oc1, BASE.Di1],
    ['OC1', 'DI1'])

# DESCRIPTIVE STATISTICS FOR OC1 AND DI1 CSD
Tables.des('OC1 and DI1\'s CSD',
    'descsd',
    [BASE.Oc1Csd, BASE.Di1Csd],
    ['OC1\'s CSD', 'DI1\'s CSD'])

# ADF TEST FOR OC1 AND DI1
Tables.adf('ocdiadf',
    [BASE.Oc1, BASE.Di1],
    ['OC1', 'DI1'])

# KPSS TEST FOR OC1 AND DI1
Tables.kpss('ocdikpss',
    [BASE.Oc1, BASE.Di1],
    ['OC1', 'DI1'])

#LJUNG-BOX TEST FOR BOTH CSD RESIDUALS
Tables.ljung('reswhite',
             [BASE.Oc1Res, BASE.Di1Res],
             ['Residuals of OC1\'s GARCH', 'Residuals of DI1\'s GARCH'])

# SHAPIRO WILK TEST FOR BOTH CSD
Tables.shapiro('csdshapiro',
        [BASE.Oc1Csd, BASE.Di1Csd],
        ['OC1\'s CSD', 'DI1\'s CSD'])

# PARAMETRIC LIMITS FOR OC1 AND DI1
Tables.limits('limpar',
          [BASE.Oc1CsdParUp, BASE.Di1CsdParUp],
          [BASE.Oc1CsdParLo, BASE.Di1CsdParLo],
          ['OC1\'s CSD', 'DI1\'s CSD'],
          par = True)

# NON PARAMETRIC LIMITS FOR OC1 AND DI1
Tables.limits('limnon',
          [BASE.Oc1CsdNonUp, BASE.Di1CsdNonUp],
          [BASE.Oc1CsdNonLo, BASE.Di1CsdNonLo],
          ['OC1\'s CSD', 'DI1\'s CSD'],
          par = False)

# DAYS OF ABNORMAL VOLATILITY FOR OC1 BY PARAMETRIC ANALYSIS
oc_par = Tables.outside('ocparout',
                     BASE,
                     'Oc1',
                     'Oc1Csd',
                     ['Oc1CsdParUp', 'Oc1CsdParLo'],
                     di = False,
                     non = False)

# DAYS OF ABNORMAL VOLATILITY FOR DI1 BY PARAMETRIC ANALYSIS
di_par = Tables.outside('diparout',
                     BASE,
                     'Di1',
                     'Di1Csd',
                     ['Di1CsdParUp', 'Di1CsdParLo'],
                     di = True,
                     non = False)

# DAYS OF ABNORMAL VOLATILITY FOR OC1 BY NON PARAMETRIC ANALYSIS
oc_non = Tables.outside('ocnonout',
                     BASE,
                     'Oc1',
                     'Oc1Csd',
                     ['Oc1CsdNonUp', 'Oc1CsdNonLo'],
                     di = False,
                     non = True)

# DAYS OF ABNORMAL VOLATILITY FOR DI1 BY NON PARAMETRIC ANALYSIS
di_non = Tables.outside('dinonout',
                     BASE,
                     'Di1',
                     'Di1Csd',
                     ['Di1CsdNonUp', 'Di1CsdNonLo'],
                     di = True,
                     non = True)

# NEWS COMMON TO OC1 AND DI1 BY PARAMETRIC ANALYSIS
parcom = Tables.noticia_para_cada_dia('parcom', News.comum(oc_par, di_par), noticias_relevantes,
                             'Political News Related to Both OC1 and DI1, for Parametric Analysis')

# NEWS SPECIFIC TO OC1 BY PARAMETRIC ANALYSIS
paroc = Tables.noticia_para_cada_dia('paroc', News.diferente(oc_par, di_par), noticias_relevantes,
                             'Political News Related to OC1 Only, for Parametric Analysis')

# NEWS SPECIFIC TO DI1 BY PARAMETRIC ANALYSIS
pardi = Tables.noticia_para_cada_dia('pardi', ews.diferente(di_par, oc_par), noticias_relevantes,
                             'Political News Related to DI1 Only, for Parametric Analysis')

# NEWS COMMON TO OC1 AND DI1 BY NON PARAMETRIC ANALYSIS
noncom = Tables.noticia_para_cada_dia('noncom', News.comum(oc_non, di_non), noticias_relevantes,
                             'Political News Related to Both OC1 and DI1, for Non Parametric Analysis')

# NEWS SPECIFIC TO OC1 BY NON PARAMETRIC ANALYSIS
nonoc = Tables.noticia_para_cada_dia('nonoc', News.diferente(oc_non, di_non), noticias_relevantes,
                             'Political News Related to OC1 Only, for Non Parametric Analysis')

# NEWS SPECIFIC TO DI1 BY NON PARAMETRIC ANALYSIS
nondi = Tables.noticia_para_cada_dia('nondi', News.diferente(di_non, oc_non), noticias_relevantes,
                             'Political News Related to DI1 Only, for Non Parametric Analysis')

