"""
NOME: Some Evidence on Political Information and Exchange Coupon in Brazil -
      Calculations Module
AUTHOR: Bernardo Paulsen
DATE: 2019/07/09
VERSION: 2.0.0
LINK: https://github.com/profnssorg/information-asset-returns

DESCRIPTION: Class for the output of graphs' image and latex text

"""


######## IMPORT PACKAGES ########


from arch import arch_model
import numpy as np
from scipy import stats


######## CLASS DEFINITION ########

class Calculations():

    def __init__(self):

        self.init = 'OK'

    def exchange_coupon(self,  # DataFrame containing the Series for the exchange coupon
                        dol=str(),  # column number of exchange rate Series
                        rs=list(),
                        # columns numbers for interest rates Series (min 1 number, if > 1 then more than one measure of exchange coupon is generated)
                        names=list()):  # names for exchange coupons

        '''APPENDS EXCHANGE COUPON TO DATAFRAME'''

        for i in range(len(rs)):
            self[names[i]] = ( (1 + self[rs[i]].shift(1) / 100) / (self[dol] / self[dol].shift(1)) - 1)

    def garch(self,  # DataFrame containing the Series
              cols=list()):  # columns numbers of Series

        '''APPENDS GARCH'S CSD AND RESIDUALS TO DATAFRAME'''

        for i in range(len(cols)):
            fitted_model = arch_model(self[cols[i]][1:]).fit()
            self['{}Csd'.format(cols[i])] = fitted_model.conditional_volatility
            self['{}Res'.format(cols[i])] = fitted_model.resid

    def limits(self,  # DataFrame containing the Series
               cols=list()):  # columns numbers of Series

        '''APPENDS PARAMETRIC AND NON PARAMETRIC LIMITS TO DATAFRAME'''

        def create(par = True,
            up=True):

            '''RETURNS ARRAY OF PARAMETRIC LIMIT (UPPER OR LOWER)'''

            if par:
                mean = series.mean()
                std = series.std()
            if not par:
                mean = series.rolling(window=63, min_periods=0, center=True).mean()
                std = series.rolling(window=63, min_periods=0, center=True).std()
            
            if up:
                value = mean + stats.norm.ppf(q=0.975) * (std)
            if not up:
                value = mean - stats.norm.ppf(q=0.975) * (std)

            return (value)

        for e in range(len(cols)):
            name = self.columns[cols[e]]
            series = self[name]
            # PARAMETRIC
            # ----UPPER
            self['{}ParUp'.format(name)] = create(par = True, up=True)
            # ----LOWER
            self['{}ParLo'.format(name)] = create(par = True, up=False)
            # NON PARAMETRIC
            # ----UPPER
            self['{}NonUp'.format(name)] = create(par = False, up=True)
            # ----LOWER
            self['{}NonLo'.format(name)] = create(par = False, up=False)