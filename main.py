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
#sgs_numbers = [1, 11, 12]

# INITIAL DATE FOR SERIES
#sgs_initial_date = '26/09/2016'

# FINAL DATE FOR SERIES
#sgs_final_date = '16/05/2019'

#
# PRECESS DATA -----------------------------------------------------------------
#
# Scrapping
os.system('scrapy crawl g1 -o noticias.json')

# CREATES DATAFRAM WITH SERIES FROM BACEN-SGS
BASE = bacen_sgs_api(names = ['Ptax', 'Selic', 'Di'],
                     numbers = [1, 11, 12],
                     initial_date = '26/09/2016',
                     final_date = '16/05/2019')

# APPENDS EXCHANGE COUPONS TO DATAFRAME
exchange_coupon(BASE, 0, [1, 2], ['Oc1', 'Di1'])

# APPENDS GARCH'S CSD AND RESIDUALS OF EXCHANGE COUPONS TO DATAFRAME
garch(BASE, [3,4])

# APPENDS LIMITS FROM BOTH PARAMETRIC AND NON PARAMETRIC ANALYSIS FOR BOTH MEASU
#RES OF EXCHANGE COUPON TO DATAGRAME
limits(BASE, [5, 7])

# OUTPUT DATA ------------------------------------------------------------------

#       PTAX, SELIC AND DI -----------------------------------------------------

# GRAPH FOR PTAX
graph([BASE.Ptax],
      [],
      'PTAX',
      'Dollar Exchange Rate',
      'ptax')

# GRAPH FOR SELIC
graph([BASE.Selic],
      [],
      'Selic',
      'Referential Rate of the Special Settlement and Custody System',
      'selic')

# GRAPH FOR DI
graph([BASE.Di],
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

ljung_shapiro('reswhite',
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

acf_pacf(BASE.Oc1, 'OC1 Exchange Coupon', 'oc')

acf_pacf(BASE.Di1, 'DI1 Exchange Coupon', 'di')

acf_pacf(BASE.Oc1Res, 'Residuals of OC1', 'ocres', True)

acf_pacf(BASE.Di1Res, 'Residuals of DI1', 'dires', True)


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

#		4_2_4 PARAMETRIC ----------------------------------------------

shapiro('csdshapiro',
        [BASE.Oc1Csd, BASE.Di1Csd],
        ['OC1\'s CSD', 'DI1\'s CSD'])

limitstab('limpar',
          [BASE.Oc1CsdParUp, BASE.Di1CsdParUp],
          [BASE.Oc1CsdParLo, BASE.Di1CsdParLo],
          ['OC1\'s CSD', 'DI1\'s CSD'],
          par = True)

graph([BASE.Oc1Csd, BASE.Oc1CsdParUp, BASE.Oc1CsdParLo],
      ['CSD', 'Upper Limit', 'Lower Limit'],
      'CSD',
      'Parametric Limits for OC1\'s CSD',
      'oclimpar')

graph([BASE.Di1Csd, BASE.Di1CsdParUp, BASE.Di1CsdParLo],
      ['CSD', 'Upper Limit', 'Lower Limit'],
      'CSD',
      'Parametric Limits for DI1\'s CSD',
      'dilimpar')
oc_out_par = outside('ocparout',
                     BASE,
                     'Oc1',
                     'Oc1Csd',
                     ['Oc1CsdParUp', 'Oc1CsdParLo'],
                     di = False,
                     non = False)
di_out_par = outside('diparout',
                     BASE,
                     'Di1',
                     'Di1Csd',
                     ['Di1CsdParUp', 'Di1CsdParLo'],
                     di = True,
                     non = False)

#   4_2_5 NON PARAMETRIC ------------------------------------------

limitstab('limnon',
          [BASE.Oc1CsdNonUp, BASE.Di1CsdNonUp],
          [BASE.Oc1CsdNonLo, BASE.Di1CsdNonLo],
          ['OC1\'s CSD', 'DI1\'s CSD'],
          par = False)

graph([BASE.Oc1Csd, BASE.Oc1CsdNonUp, BASE.Oc1CsdNonLo],
      ['CSD', 'Upper Limit', 'Lower Limit'],
      'CSD',
      'Non Parametric Limits for OC1\'s CSD',
      'oclimnon')

graph([BASE.Di1Csd, BASE.Di1CsdNonUp, BASE.Di1CsdNonLo],
      ['CSD', 'Upper Limit', 'Lower Limit'],
      'CSD',
      'Non Parametric Limits for DI1\'s CSD',
      'dilimnon')

oc_out_non = outside('ocnonout',
                     BASE,
                     'Oc1',
                     'Oc1Csd',
                     ['Oc1CsdNonUp', 'Oc1CsdNonLo'],
                     di = False,
                     non = True)

di_out_non = outside('dinonout',
                     BASE,
                     'Di1',
                     'Di1Csd',
                     ['Di1CsdNonUp', 'Di1CsdNonLo'],
                     di = True,
                     non = True)

#     ---------------------------------------------------

out_and_news()
