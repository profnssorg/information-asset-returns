'''
NOME: Some Evidence on Political Information and Exchange Coupon in Brazil -
      BACEN SGS API Module
AUTHOR: Bernardo Paulsen
DATE: 2019/06/24
VERSION: 1.0.0
LINK: https://github.com/profnssorg/information-asset-returns

DESCRIPTION: Class for the import of data from BACEN SGS API

'''

######## IMPORT PACKAGES ########


import numpy as np # api - array used for series and dataframe data structures
                   # fundamental package for scientific computing
import pandas as pd # api - series and datagrame data structues & various 
                    # data structures and data analysis tools


######### CLASS DEFINITION ########


class ImportBacen():

    '''
    CLASS WITH METHODS TO IMPORT DATA FROM BACEN SGS API

    Creates pandas.DataFrame, and append to this pandas.DataFrame, 
    pandas.Series with data from Central Bank of Brazil Time Series Management
    System via it's Application Programing Interface (BACEN-SGS API).

    Parameters
    ----------

    Methods
    -------
    create: creates pandas.DataFrame
        From series' names, numbers and intial and final date, collects series
        and creates pandas.DataFrame.

    append: appends pandas.Series to pandas.DataFrame
        From series' names, numbers and intial and final date, collects series
        and appends to pandas.DataFrame.

    '''

    def __init__(self):
        
        self.init = 'OK'
        
    def create(names = list(str()), # names to be assign to series
               numbers = list(int()), # series' numbers on SGS
               initial_date = str(), # initial date
               final_date = str()): # final date
    
        '''
        CREATES DATAFRAME WITH BACEN-SGS SERIES

        Outputs pandas.DataFrame  with series from Central Bank of Brazil Time 
        Series. Management Systema (BACEN-SGS) through its Apllication
        Programming Interface

        Parameters
        ----------
        names : list of strings
            Names to be assigned to pandas.Series inside pandas.DataFrame.

        numbers : list of integer
            Numbers of series in BACEN-SGS.

        initial_date : string
            Initial date for series

        final_date : string
            Final date for series

        Returns
        -------
        pandas.DataFrame: contains series

        '''

        for i in range(len(names)):
            name = str(names[i])
            url = 'http://api.bcb.gov.br/dados'
            url += '/serie/bcdata.sgs.{}'.format(numbers[i])
            url += '/dados?formato=csv&'
            url +=  '&dataInicial={}&dataFinal={}'.format(initial_date,
                final_date)
            df = pd.read_csv(url,
                sep = ';', index_col = 0, parse_dates = [0],
                infer_datetime_format = True, decimal = ',')
            if i == 0:
                DF = pd.DataFrame({name: df.valor},
                                       index = df.index)
            else:
                DF[name] = df.valor
        
        return(DF)

    def append(self, # DataFrame to append Series
               names = list(), # names to be assign to Series
               numbers = list(), # series' numbers on SGS
               initial = str(), # initial date
               final = str()): # final date
    
        '''
        APPENDS BACEN-SGS SERIES TO DATAFRAME

        Appends to pandas.DataFrame series from Central  Bank of  Brazil  Time
        Series   Management  Systema   (BACEN-SGS)  through   its  Apllication
        Programming Interface

        Parameters
        ----------
        self : pandas.DataFrame
            Object to append pandas.Series.

        names : list of strings
            Names to be assigned to pandas.Series.

        numbers : list of integer
            Numbers of series in BACEN-SGS.

        initial_date : string
            Initial date for series

        final_date : string
            Final date for series

        Returns
        -------
        Appends pandas.Series to self
        '''

        for i in range(len(names)):
            name = str(names[i])
            url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=csv&&dataInicial={}&dataFinal={}'.format(numbers[i], initial_date, final_date)
            df = pd.read_csv(url, sep = ';', index_col = 0, parse_dates = [0], infer_datetime_format = True, decimal = ',')
            self[name] = df.valor




