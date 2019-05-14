# Importação de bibliotecas

import input_
import process
import output

from arch import arch_model

# ENTRADA
# ENTRADA
# ENTRADA

# Datas de início e fim para as séries que serão coletadas
data_inicial = '01/01/2010'
data_final = '31/12/2018'

# PROCESSAMENTO
# PROCESSAMENTO
# PROCESSAMENTO

# Criação dos DataFrames das variáveis
PTAX = serie(1, data_inicial, data_final)
Selic = serie(11, data_inicial, data_final)
DI = serie(12, data_inicial, data_final)

# Cálculo do cupom cambial
CupomCambialOC = cupomCambial(Selic, PTAX)
CupomCambialDI = cupomCambial(DI, PTAX)

# Estimação do GARCH
ResultadoGarchOC = arch_model(CupomCambialOC.valor).fit()
ResultadoGarchDI = arch_model(CupomCambialDI.valor).fit()

# Definição dos limites
# Análise Paramétrica
OCP = limitP(ResultadoGarchOC.conditional_volatility)
DIP = limitP(ResultadoGarchDI.conditional_volatility)
# Análise Não Paramétrica
OCnP = limitNP(ResultadoGarchOC.conditional_volatility)
DInP = limitNP(ResultadoGarchDI.conditional_volatility)

# SAIDA
# SAIDA
# SAIDA

# Gráficos e estatísticas descritivas das séries base
graph(PTAX,
      'PTAX 800',
      'Dollar Exchange Rate',
      'PTAX',
      'fig:PTAX')
graph(Selic,
      'Selic',
      'Referential Rate of the Special Settlement and Custody System',
      'Selic',
      'fig:Selic')
graph(DI,
      'DI',
      'Interbank Deposit Rate',
      'DI',
      'fig:DI')
des('tab:desptaxselicdi',
    [PTAX, Selic, DI],
    ['PTAX', 'Selic', 'DI'])

# Gráficos e estatísticas descritivas (com testes) das séries de cupom cambial
graph(CupomCambialOC,
      'CupomCambialOC',
      'OC1 Exchange Coupon',
      'OC1',
      'fig:oc1')
graph(CupomCambialDI,
      'CupomCambialDI',
      'DI1 Exchange Coupon',
      'DI1',
      'fig:di1')
des('tab:desc_oc1_di1',
    [CupomCambialOC, CupomCambialDI],
    ['OC1 Exchange Coupon', 'DI1 Exchange Coupon'])
adf('tab:coupon_adf',
    [CupomCambialOC, CupomCambialDI],
    ['OC1 Exchange Coupon', 'DI1 Exchange Coupon'])
kpss('tab:coupon_kpss',
    [CupomCambialOC, CupomCambialDI],
    ['OC1 Exchange Coupon', 'DI1 Exchange Coupon'])

# Tabelas e gráficos do GARCH
ljungShapiro('tab:residuals_white',
             [ResultadoGarchOC.resid, ResultadoGarchDI.resid],
             ['Residuals of OC1 Exchange Coupon', 'Residuals of DI1 Exchange Coupon'])
graph(ResultadoGarchOC.conditional_volatility,
      'Conditional Standard Deviation',
      'Conditional Standard Deviation of OC1 Exchange Coupon',
      'CSDOC',
      'fig:csdoc')
graph(ResultadoGarchDI.conditional_volatility,
      'Conditional Standard Deviation',
      'Conditional Standard Deviation of OC1 Exchange Coupon',
      'CSDDI',
      'fig:csddi')
des('tab:des_csd',
    [ResultadoGarchOC.conditional_volatility, ResultadoGarchDI.conditional_volatility],
    ['CSD of OC1 Exchange Coupon', 'CSD of Exchange Coupon'],
    csd = True)

# Gráfico e tabela análise paramétrica
tabP('tab:par_lim',
     [OCP, DIP],
     ['CSD of OC1 Exchange Coupon', 'CSD of Exchange Coupon'])
graph(ResultadoGarchOC.conditional_volatility,
      'Conditional Standard Deviation',
      'Parametric Limits for Conditional Standard Deviation of OC1 Exchange Couponn',
      'par_oc',
      'fig:par_oc',
      limit = True)
graph(ResultadoGarchDI.conditional_volatility,
      'Conditional Standard Deviation',
      'Parametric Limits for Conditional Standard Deviation of DI1 Exchange Couponn',
      'par_di',
      'fig:par_di',
      limit = True)
outside('tab:limite_par_oc',
        CupomCambialOC,
        ResultadoGarchOC.conditional_volatility,
        DIP)
outside('tab:limite_par_di',
        CupomCambialDI,
        ResultadoGarchDI.conditional_volatility,
        DIP)

# Gráfico e tabela análise não paramétrica
tabNP('tab:non_lim',
     [OCnP, DInP],
     ['CSD of OC1 Exchange Coupon', 'CSD of Exchange Coupon'])
graph(ResultadoGarchOC.conditional_volatility,
      'Conditional Standard Deviation',
      'Non-Parametric Limits for Conditional Standard Deviation of OC1 Exchange Couponn',
      'non_oc',
      'fig:non_oc',
      limit = True,
      np = True)
graph(ResultadoGarchDI.conditional_volatility,
      'Conditional Standard Deviation',
      'Non-Parametric Limits for Conditional Standard Deviation of DI1 Exchange Couponn',
      'non_di',
      'fig:non_di',
      limit = True,
      np = True)
outside('tab:limite_non_oc',
        CupomCambialOC,
        ResultadoGarchOC.conditional_volatility,
        DInP)
outside('tab:limite_non_di',
        CupomCambialDI,
        ResultadoGarchDI.conditional_volatility,
        DInP)



