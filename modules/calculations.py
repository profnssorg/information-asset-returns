
# IMPORT PACKAGES

#import numpy as np # api - array used for series and dataframe data structures
                   # fundamental package for scientific computing
#import pandas as pd # api - series and datagrame data structues & various 
                    # data structures and data analysis tools

from arch import arch_model
from scipy import stats

class Calculations():

    '''THIS CLASS HAS METHODS TO EXECUTE CALCULATIONS IN TIME SERIES'''
    
    def __init__(self):
        
        self.init = 'OK'

    def exchange_coupon(self, # DataFrame containing the Series for the exchange coupon
                      dol = int(), # column number of exchange rate Series
                      rs = list(), # columns numbers for interest rates Series (min 1 number, if > 1 then more than one measure of exchange coupon is generated)
                      names = list()): # names for exchange coupons

        '''APPENDS EXCHANGE COUPON TO DATAFRAME'''

        usd = self[self.columns[dol]]
        for e in range(len(rs)):
            r = self[self.columns[rs[e]]]
            name = names[e]
            arr = np.array(list())
            for i in range(len(usd)):
                if i == 0:
                    arr = np.append(arr, np.NaN)
                else:
                    arr = np.append(arr, ((1 + r[i]/100)/(usd[i]/usd[i-1])-1))
            self[name] = arr

    def garch(self, # DataFrame containing the Series 
              cols = list()): # columns numbers of Series

        '''APPENDS GARCH'S CSD AND RESIDUALS TO DATAFRAME'''

        for i in range(len(cols)):
            name = self.columns[cols[i]]
            fitted_model = arch_model(self[name][1:]).fit()
            self['{}Csd'.format(name)] = fitted_model.conditional_volatility
            self['{}Res'.format(name)] = fitted_model.resid

    def limits(self, # DataFrame containing the Series
               cols = list()): # columns numbers of Series

        '''APPENDS PARAMETRIC AND NON PARAMETRIC LIMITS TO DATAFRAME'''

        def create_par(up = True):

            '''RETURNS ARRAY OF PARAMETRIC LIMIT (UPPER OR LOWER)'''

            mean = series.mean()
            std = series.std()
            if up == True:
                value = mean + stats.norm.ppf(q = 0.975) * (std)
            else:
                value = mean - stats.norm.ppf(q = 0.975) * (std)
            arr = np.array(list())
            for i in range(len(series)):
                if i == 0:
                    arr = np.append(arr, np.NaN)
                else:
                    arr = np.append(arr, value)
            return(arr)

        def create_non(up = True):

            '''RETURNS ARRAY OF NON PARAMETRIC LIMIT (UPPER OR LOWER)'''

            mean = series.rolling(window = 63, min_periods = 0, center = True).mean()
            std = series.rolling(window = 63, min_periods = 0, center = True).std()
            arr = np.array(list())
            for i in range(len(mean)):
                if up == True:
                    value = mean[i] + stats.norm.ppf(q = 0.975) * (std[i])
                else:
                    value = mean[i] - stats.norm.ppf(q = 0.975) * (std[i])
                if i == 0:
                    arr = np.append(arr, np.NaN)
                else:
                    arr = np.append(arr, value)
            return(arr)

        for e in range(len(cols)):
            name = self.columns[cols[e]]
            series = self[name]
            # PARAMETRIC
            # ----UPPER
            self['{}ParUp'.format(name)] = create_par(up=True)
            # ----LOWER 
            self['{}ParLo'.format(name)] = create_par(up=False)
            # NON PARAMETRIC
            # ----UPPER
            self['{}NonUp'.format(name)] = create_non(up = True)
            # ----LOWER
            self['{}NonLo'.format(name)] = create_non(up = False)