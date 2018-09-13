import pandas as pd
from scipy import stats
import numpy as np
from numpy import linalg as LA


def get_grades(month1, month2, grade1, grade2, master_df):
    '''This function pulls all students with a specified grade in month1 (excludes duplicates)
    and then captures those same students in their following month2 to determine what their
    new grade is.The returned values are the total number of students as well as the
    probability of change or probability of no change if the student received the same grade.
    '''
    if grade1 != 'W':
        df1 = master_df[(master_df['MONTHS_IN_ATTENDANCE']==month1) & (master_df['LAST_GRADE']==grade1) |
          (master_df['MONTHS_IN_ATTENDANCE']==month1) & (master_df['LAST_GRADE']==grade2)].drop_duplicates(subset='ACCOUNT_ID')
        df2 = master_df[(master_df["ACCOUNT_ID"].isin(df1['ACCOUNT_ID'])) & (master_df['MONTHS_IN_ATTENDANCE']==month2)].drop_duplicates(subset='ACCOUNT_ID')
        df3 = df1[df1['ACCOUNT_ID'].isin(df2['ACCOUNT_ID'])]
        total = df3['LAST_GRADE'].value_counts().sum()
        grades = df2['LAST_GRADE'].value_counts()
        print("Total Students: {}".format(total), "\n", round(grades/total, 3))
    else:
        df1 = student_df[(student_df['MONTHS_IN_ATTENDANCE']==month1) & (student_df['LAST_GRADE']==grade1) |
          (student_df['MONTHS_IN_ATTENDANCE']==month1) & (student_df['LAST_GRADE']==grade2) |
          (student_df['MONTHS_IN_ATTENDANCE']==month1) & (student_df['LAST_GRADE']=='IX') |
          (student_df['MONTHS_IN_ATTENDANCE']==month1) & (student_df['LAST_GRADE']=='I') |
          (student_df['MONTHS_IN_ATTENDANCE']==month1) & (student_df['LAST_GRADE']=='P') |
          (student_df['MONTHS_IN_ATTENDANCE']==month1) & (student_df['LAST_GRADE']=='IP')].drop_duplicates(subset='ACCOUNT_ID')
        df2 = master_df[(master_df["ACCOUNT_ID"].isin(df1['ACCOUNT_ID'])) & (master_df['MONTHS_IN_ATTENDANCE']==month2)].drop_duplicates(subset='ACCOUNT_ID')
        df3 = df1[df1['ACCOUNT_ID'].isin(df2['ACCOUNT_ID'])]
        total = df3['LAST_GRADE'].value_counts().sum()
        grades = df2['LAST_GRADE'].value_counts()
        print("Total Students: {}".format(total), "\n", round(grades/total, 3))

# The below Markov Chain is based off probability percentages of receiving a grade and either
#continuing to maintain that grade or getting another grade.
markov_chain = np.array([.856, .081, .063, .192, .634, .174, .068, .063, .869]).reshape(3, 3)

#This function takes the probability matrix and takes a power to show impact of
#grades over a length of time
def markov_power(markov):
    for num in range(1, 40):
        print("Transition matrix for month {}".format(num), "\n",
              LA.matrix_power(markov, num), "\n")
