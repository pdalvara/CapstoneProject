import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from scipy import stats


def month_data(df, months, course=1):
    '''
    This function is used in conjunction with the code below to create 18 months worth of
    bar graphs'''
    return df[(df['MONTHS_IN_ATTENDANCE']==months) &
           (df['Y_VAR'] == on_course)]['LAST_GRADE'].value_counts()

fig, axes = plt.subplots(6,3, figsize=(10,10))
month = 0
for ax1, ax2, ax3 in axes:
    month += 1
    ax1.bar(month_data(student_df, month).index, month_data(student_df, month).values)
    ax1.set_title(month)
    month += 1
    ax2.bar(month_data(student_df, month).index, month_data(student_df, month).values)
    ax2.set_title(month)
    month += 1
    ax3.bar(month_data(student_df, month).index, month_data(student_df, month).values)
    ax3.set_title(month)
