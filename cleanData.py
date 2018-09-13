import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import LabelEncoder
%matplotlib inline

def clean_data(df):
    """
    Input: Dataframe
    Output: Filtered Dataframe
    This function will convert grades to a consistent format, fills in null gender
    proportionally to current distribution of M/F, and uses Label Encoding to convert
    grades so that dataframe can be used in machine learning model"""
    grades = {'A': ['A+', 'A-','A'],
          'B': ['B+','B-','B'],
          'C':['C+','C-','C'],
          'D':['D+','D-','D'],
          'F':['F'],
          'W': ['W'],
          'IX': ['IX'],
          'I':['I'],
          'P':['P'],
          'IP':['IP']}
    grades_dict = {v: k for k,vv in grades.items() for v in vv}
    df['LAST_GRADE'] = df['LAST_GRADE'].map(grades_dict).astype("category", categories=set(grades_dict.values()))
    counts = df['GENDER'].value_counts()
    dist = stats.rv_discrete(values=(np.arange(counts.shape[0]),
                                 counts/counts.sum()))
    fill_idxs = dist.rvs(size=df.shape[0] - df['GENDER'].count())
    df.loc[df['GENDER'].isnull(), "GENDER"] = counts.iloc[fill_idxs].index.values
    student_df = df[['Y_VAR', 'ACCOUNT_ID', 'REPORT_MONTH', 'MONTHS_IN_ATTENDANCE',
                          'PACE', 'GPA',
                          'CREDITS', 'SCHOOL_CREDITS',
                          'WF', 'AGE_BUCKET', 'CRED_ATT',
                         'COURS_COMP', 'TOTAL_CREDITS',
                         'TOTAL_PROGRAM_CREDITS', 'TOTAL_COURS_COMP', 'PROGRAM_TYPE',
                         'REENROLL', 'LAST_GRADE', 'MODALITY', 'GENDER']]
    student_df2 = pd.get_dummies(student_df, columns=['PROGRAM_TYPE',
                                     'AGE_BUCKET', 'REENROLL',
                                     'MODALITY', 'GENDER'], drop_first=True)
    labeler = LabelEncoder()
    labeler.fit(student_df2['LAST_GRADE'])
    student_df2['LAST_GRADE'] = labeler.transform(student_df2['LAST_GRADE'])
    return student_df2

def tier(df, report_month):
    """
    Input: Dataframe, Report Month String (i.e. '2018-01-01')
    Output:  X, y variables
    Use this function to create X and y variables to use in training machine
    learning model"""
    df = df[df['REPORT_MONTH']==report_month]
    top = df[(df['PROJECTED_ZERO_CREDITS'] >= 1.5)]
    bottom = df[(df['PROJECTED_THREE_CREDITS'] < 1.5)]
    first_pass = df[(~df['ACCOUNT_ID'].isin(top['ACCOUNT_ID']))]
    middle = first_pass[~first_pass['ACCOUNT_ID'].isin(bottom['ACCOUNT_ID'])]
    del middle['PROJECTED_ZERO_CREDITS']
    del middle['PROJECTED_THREE_CREDITS']
    del middle['ACCOUNT_ID']
    del middle['REPORT_MONTH']
    del middle['PROG_GPA']
    middle.dropna(inplace=True)
    middle.reset_index(inplace=True)
    del middle['index']
    y = middle.pop('Y_VAR').values
    X = middle
    return X, y
