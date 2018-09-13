import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline
from pandas.tools.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA
from scipy import signal
from scipy import stats
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA
plt.style.use('ggplot')

#This was not used in the capstone presentation but is the beginning stages of an Arima Model
#for time series forecasting

df['REPORT_MONTH'] = pd.to_datetime(df['REPORT_MONTH'])
course_by_month = df.groupby(['REPORT_MONTH', 'Y_VAR'])['ACCOUNT_ID'].count().unstack()

off_course = course_by_month[0]
on_course = course_by_month[1]

off_course.plot(figsize=(20,8), xticks=off_course.index, color='r', legend=True)
on_course.plot(figsize=(20,8), xticks=on_course.index, color='b', legend=True)

plt.figure(figsize=(20, 8))
autocorrelation_plot(off_course)

plt.figure(figsize=(20, 8))
autocorrelation_plot(on_course)

def plot_trend_data(ax, series):
    ax.plot(series.index.date, series)
    ax.set_title("On course")

def make_design_matrix(arr):
    """Construct a design matrix from a numpy array, converting to a 2-d array
    and including an intercept term."""
    return sm.add_constant(arr.reshape(-1, 1), prepend=False)

def  fit_linear_trend(series):
    """Fit a linear trend to a time series.  Return the fit trend as a numpy array."""
    X = make_design_matrix(np.arange(len(series)) + 1)
    linear_trend_ols = sm.OLS(series.values, X).fit()
    linear_trend = linear_trend_ols.predict(X)
    return linear_trend

def plot_linear_trend(ax, series):
    linear_trend = fit_linear_trend(series)
    plot_trend_data(ax, series)
    ax.plot(series.index.date, linear_trend)

fig,  ax  =  plt.subplots(1, figsize=(14, 2))
plot_linear_trend(ax, on_course)
plt.tight_layout()

on_course_series = on_course
on_course_linear_trend = fit_linear_trend(on_course_series)
on_course_series_detrended = on_course_series - on_course_linear_trend

fig, ax = plt.subplots(1, figsize=(14, 2))
ax.plot(on_course_series_detrended.index, on_course_series_detrended)
ax.set_title("On course, Detrended")
plt.tight_layout()
