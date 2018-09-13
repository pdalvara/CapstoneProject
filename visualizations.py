import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
from scipy import stats
import matplotlib.dates as mdates
plt.style.use('ggplot')



Course_by_report_month = student_df.groupby(['REPORT_MONTH','Y_VAR'])['ACCOUNT_ID'].count().unstack()

#Shows month over month on and off course customers
ax = Course_by_report_month.plot(x=Course_by_report_month.index, figsize=(12, 8), kind='bar', colormap='Set1',
                           title='On/Off Course by Report Month')
x_labels=Course_by_report_month.index.strftime('%b %y')
ax.set_xticklabels(x_labels)


#Shows when customers go off course
ax = Course_by_num_months[:24].plot(figsize=(12, 8), colormap='Set1', kind='line',
                           title='On/Off Course by Month', fontsize=14)
ax.legend(['Off Course', 'On Course'])
plt.tight_layout()
# plt.savefig('on_off_course.png')
# fig = months_plot.get_figure()
# fig.savefig("months_plot.png")

#This shows pace month over month
pace = student_df.groupby(['REPORT_MONTH', 'Y_VAR']).agg({'PACE':np.mean}).unstack()
ax2 = pace.plot(figsize=(12,8), kind='line', colormap='Set1')
ax2.legend(['Off Course', 'On Course'])

#This shows drops month over month
WF = student_df.groupby(['MONTHS_IN_ATTENDANCE', 'Y_VAR'])['WF'].mean().unstack()
WF[:24].plot(figsize=(12, 8), colormap='Set1')
plt.legend(['Off Course', 'On Course'])
