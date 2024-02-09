#libs
import pandas as pd
import numpy as np
from scipy import stats

import statsmodels.graphics.tsaplots as smt
import statsmodels.graphics.gofplots as sm
import statsmodels.sandbox.stats.runs as wald
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt


#A function to diagnostics in time series

def ts_feature(serie, lags=None, title="", filename="", ylab=""):
    """
    Funcao para diagnotico em series temporais, analise grafica - autocorrelacao, autocorrelacao parcial, qq plot,
    histograma e teste de Dickey Fuller aumentado-ADF
    """
      
    if isinstance(serie, pd.Series):
        serie = pd.Series(serie)
    
    #layouts
    fig = plt.figure(figsize=(14, 14))
    layout = (3, 2)
    ts_ax = plt.subplot2grid(layout, (0, 0), colspan=2)
    acf_ax = plt.subplot2grid(layout, (1, 0))
    pacf_ax = plt.subplot2grid(layout, (1, 1))
    hist_ax = plt.subplot2grid(layout, (2, 0))
    qq_ax = plt.subplot2grid(layout, (2, 1))
   
    
    #time serie graphic
    ax = serie.plot(ax = ts_ax, lw=2, colormap='jet', marker='.', markersize=7, label='Original', fontsize=12)
    serie.rolling(window=12, center=False).mean().plot(ax=ts_ax, color='darkred', label='Move averege', fontsize=12)
    serie.rolling(window=12, center=False).std().plot(ax=ts_ax, color='darkgray', label='Move standard deviation', fontsize=12)
    ax.legend(loc='best')
    ax.set_xlabel("Time")
    ax.set_ylabel(ylab)
    ts_ax.set_title(title, fontsize = 14)
    
    #autocorrelation and partial autocorrelation graphic
    smt.plot_acf(serie, lags = lags, ax = acf_ax, alpha = 0.5)
    acf_ax.set_title('Autocorrelation', fontsize=14)
    smt.plot_pacf(serie, lags = lags, ax = pacf_ax, alpha = 0.5)
    pacf_ax.set_title('Parcial Autocorrelation', fontsize=14)
    
    
    #histogram graphic
    ax = serie.plot(ax=hist_ax, kind='hist')
    ax.set_ylabel('Frequency')
    hist_ax.set_title('Histogram', fontsize=14)
    
    #qq plot graphic
    sm.qqplot(serie, line='s', ax=qq_ax)
    plt.xlabel('Teoretical quantis')
    plt.ylabel('Sample quantis')
    qq_ax.set_title("Q-Q Plot", fontsize=14)  
    plt.tight_layout()
    plt.show()
        
    
    print('\n\nResults of Augmented Dickey-Fuller test:\n')
    print('If p-value < 0.05: Reject null hipoteses, the time serie is stationarity by 5% of significance.')
    dftest = adfuller(serie, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['test statistic', 'p-value', '# of lags', '# of observations'])
    
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
    
    return


def ts_trendseason(serie, title="", ylab1=""):
    # To use this function the dataset need datetime index rows 
    
    #pivot
    serie_sz = serie
    
    #trend
    serie = pd.Series(serie[serie.columns[0]])
    
    #layouts
    fig = plt.figure(figsize=(14, 24))
    layout = (4, 2)
    tw1_ax = plt.subplot2grid(layout, (0, 0))
    tw2_ax = plt.subplot2grid(layout, (0, 1))
    tw3_ax = plt.subplot2grid(layout, (1, 0))
    tw4_ax = plt.subplot2grid(layout, (1, 1))
    szy_ax = plt.subplot2grid(layout, (2, 0), colspan=2)
    szm_ax = plt.subplot2grid(layout, (3, 0), colspan=2)
    
    
    ##time serie graphic
    #4 month
    ax = serie.plot(ax = tw1_ax, lw=2, colormap='jet', marker='.', markersize=7, label='Original', fontsize=12)
    serie.rolling(window=4, center=False).mean().plot(ax=tw1_ax, color='darkred', label='4 m - Move average', fontsize=12)
    serie.rolling(window=4, center=False).std().plot(ax=tw1_ax, color='darkgray', label='4 m - Move standard deviation', fontsize=12)
    ax.legend(loc='best')
    ax.set_xlabel("Time")
    ax.set_ylabel(ylab1)
    plt.title(title, fontsize = 14)
    #6 month
    ax = serie.plot(ax = tw2_ax, lw=2, colormap='jet', marker='.', markersize=7, label='Original', fontsize=12)
    serie.rolling(window=6, center=False).mean().plot(ax=tw2_ax, color='darkred', label='6 m - Move average', fontsize=12)
    serie.rolling(window=6, center=False).std().plot(ax=tw2_ax, color='darkgray', label='6 mo - Move standard deviation', fontsize=12)
    ax.legend(loc='best')
    ax.set_xlabel("Time")
    ax.set_ylabel(ylab1)
    #8 month
    ax = serie.plot(ax = tw3_ax, lw=2, colormap='jet', marker='.', markersize=7, label='Original', fontsize=12)
    serie.rolling(window=8, center=False).mean().plot(ax=tw3_ax, color='darkred', label='8 m - Move average', fontsize=12)
    serie.rolling(window=8, center=False).std().plot(ax=tw3_ax, color='darkgray', label='8 m - Move standard deviation', fontsize=12)
    ax.legend(loc='best')
    ax.set_xlabel("Time")
    ax.set_ylabel(ylab1)
    #12 month
    ax = serie.plot(ax = tw4_ax, lw=2, colormap='jet', marker='.', markersize=7, label='Original', fontsize=12)
    serie.rolling(window=12, center=False).mean().plot(ax=tw4_ax, color='darkred', label='12 m - Move average', fontsize=12)
    serie.rolling(window=12, center=False).std().plot(ax=tw4_ax, color='darkgray', label='12 m - Move standard deviation', fontsize=12)
    ax.legend(loc='best')
    ax.set_xlabel("Time")
    ax.set_ylabel(ylab1)
  
    #seasonality 
    serie_sz['Month'] = serie_sz.index.strftime("%b")
    serie_sz['Year'] = serie_sz.index.year
    month_names = pd.date_range(start=serie_sz.index[0], periods=12, freq='MS').strftime('%b')

    #scater plot
    df_piv = serie_sz.pivot(index='Month', columns='Year', values=serie_sz.columns[0])
    df_piv = df_piv.reindex(index=month_names)
    
    df_piv.plot(ax=szy_ax,colormap='jet', fontsize=12)
    szy_ax.set_title('Seasonal effect by month', fontsize=14)
    szy_ax.set_ylabel(ylab1, fontsize=12)
    szy_ax.set_xlabel('Time', fontsize=12)
    szy_ax.legend(loc='best', bbox_to_anchor=(1.0, 0.7))
    
    #box plot
    #new pivot table
    df_piv_box = serie_sz.pivot(index='Year', columns='Month', values=serie_sz.columns[0])
    #reindex columns
    df_piv_box = df_piv_box.reindex(columns=month_names)
    #box plot
    df_piv_box.plot(ax=szm_ax, kind='box', fontsize=12)
    szm_ax.set_title('Seasonal effect by month', fontsize=14)
    szm_ax.set_xlabel('Time', fontsize=12)
    szm_ax.set_ylabel(ylab1, fontsize=12)   
    
    return
    