# IMPORT PACKAGES
import numpy as np # api - array used for series and dataframe data structures
                   # fundamental package for scientific computing
import pandas as pd # api - series and datagrame data structues & various 
                    # data structures and data analysis tools

class ImportBacen():

    '''THIS CLASS HAS METHODS TO IMPORT DATA FROM BACEN SGS API'''

    def __init__(self):
        
        self.init = 'OK'
        
    def create(names = list(), # names to be assign to series
               numbers = list(),
               initial_date = str(),
               final_date = str()): # series' numbers on SGS
    
        '''CREATES DATAFRAME FROM BACEN-SGS SERIES'''

        for i in range(len(names)):
            name = str(names[i])
            url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=csv&&dataInicial={}&dataFinal={}'.format(numbers[i], initial_date, final_date)
            df = pd.read_csv(url, sep = ';', index_col = 0, parse_dates = [0], infer_datetime_format = True, decimal = ',')
            if i == 0:
                DF = pd.DataFrame({name: df.valor},
                                       index = df.index)
            else:
                DF[name] = df.valor
        
        return(DF)

    def append(self, # DataFrame to append Series
               names = list(), # names to be assign to Series
               numbers = list(),
               initial = str(),
               final = str()): # series' numbers on SGS
    
        '''APPENDS BACEN-SGS SERIES TO DATAFRAME'''

        for i in range(len(names)):
            name = str(names[i])
            url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=csv&&dataInicial={}&dataFinal={}'.format(numbers[i], initial_date, final_date)
            df = pd.read_csv(url, sep = ';', index_col = 0, parse_dates = [0], infer_datetime_format = True, decimal = ',')
            self[name] = df.valor