'''
NOME: Some Evidence on Political Information and Exchange Coupon in Brazil -
      BACEN SGS API Module
AUTHOR: Bernardo Paulsen
DATE: 2019/06/24
VERSION: 2.0.0
LINK: https://github.com/profnssorg/information-asset-returns

DESCRIPTION: Class for the import of data from BACEN SGS API

'''

# IMPORT PACKAGES ########


import pandas as pd


# DEFINING CLASS ########


class ImportBacen():

    ''' CLASS WITH METHODS TO IMPORT DATA FROM BACEN SGS API '''

    def __init__(self):

        self.init = 'OK'

    def create(names=list(),  # names to be assign to series
        numbers=list(),  # series' numbers on SGS
        initial_date=str(),  # initial date
        final_date=str()):  # final date

        ''' CREATES DATAFRAME WITH BACEN-SGS SERIES '''

        for i in range(len(names)):

            name = str(names[i])

            url = 'http://api.bcb.gov.br/dados'
            url += '/serie/bcdata.sgs.{}'.format(numbers[i])
            url += '/dados?formato=csv&'
            url += '&dataInicial={}&dataFinal={}'.format(initial_date,
                final_date)
            df = pd.read_csv(url,
                sep=';', index_col=0, parse_dates=[0],
                infer_datetime_format=True, decimal=',')

            if not i:
                DF = pd.DataFrame({name: df.valor},
                    index=df.index)
            else:
                DF[name] = df.valor

        return (DF)


    def append(self,  # DataFrame to append Series
        names=list(),  # names to be assign to Series
        numbers=list(),  # series' numbers on SGS
        initial_date=str(),  # initial date
        final_date=str()):  # final date

        ''' APPENDS BACEN-SGS SERIES TO DATAFRAME '''

        for i in range(len(names)):

            name = str(names[i])

            url = 'http://api.bcb.gov.br/dados'
            url += '/serie/bcdata.sgs.{}'.format(numbers[i])
            url += '/dados?formato=csv&'
            url += '&dataInicial={}&dataFinal={}'.format(initial_date,
                final_date)

            df = pd.read_csv(url, sep=';', index_col=0, parse_dates=[0],
                infer_datetime_format=True, decimal=',')
            self[name] = df.valor

