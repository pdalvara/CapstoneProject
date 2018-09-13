import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from scipy import stats

def null_student_cleaning(df):
    del df['ETHNICITY']
    del df['PROG_GPA']
    del df['STATE']
    del df['ZIP_CODE']
    null_df = df[df['PACE'].isnull()]
    del null_df['PACE']
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
    null_df['LAST_GRADE'] = null_df['LAST_GRADE'].map(grades_dict).astype("category", categories=set(grades_dict.values()))
    counts =null_df['GENDER'].value_counts()
    dist = stats.rv_discrete(values=(np.arange(counts.shape[0]),
                                 counts/counts.sum()))
    fill_idxs = dist.rvs(size=null_df.shape[0] - null_df['GENDER'].count())
    null_df.loc[null_df['GENDER'].isnull(), "GENDER"] = counts.iloc[fill_idxs].index.values
    null_df = null_df.reset_index()
    del null_df['index']
    return null_df

month_one_nulls = null_master[(null_master['MONTHS_IN_ATTENDANCE'] == 1)]
month_one_nulls = month_one_nulls[['ACCOUNT_ID', 'NAME', 'DEPARTMENT',
                    'PROGRAM_TYPE', 'AWARD_TYPE', 'PROG_TYPE',
                   'REENROLL', 'LAST_GRADE', 'MODALITY', 'GENDER',
                   'AGE_BUCKET', 'CAMPUS']]

month_one_nulls[month_one_nulls['LAST_GRADE'] == 'A']['EXTERNAL_PROGRAM_TYPE'].value_counts()

month_one_nulls['LAST_GRADE'].value_counts()
#Bar Graph that shows distribution of grades for month 1
plt.bar(month_one_nulls['LAST_GRADE'].value_counts().index, month_one_nulls['LAST_GRADE'].value_counts().values)
#Bar Graph that shows distribution for individuals who continued
plt.bar(students_who_continued['LAST_GRADE'].value_counts().index, students_who_continued['LAST_GRADE'].value_counts().values)

#Pivot table that orders by degree level - this is to determine counts in each program
counts = pd.pivot_table(month_one_nulls,index=['ACCOUNT_ID','PROGRAM_TYPE','EDUC_PROG_TYPE', 'AWARD_TYPE', 'NAME'])
counts.index.get_level_values('PROGRAM_TYPE').value_counts()
counts.index.get_level_values('EDUC_PROG_TYPE').value_counts()
counts.index.get_level_values('AWARD_TYPE').value_counts()
counts.index.get_level_values('COLLEGE_NAME').value_counts()

#counts by college and program for null students
month_one_nulls.pivot_table(index='COLLEGE_NAME', columns='LAST_GRADE', aggfunc=len, fill_value=0)

#Grades by PROGRAM
month_one_nulls.pivot_table(index='EXTERNAL_PROGRAM_TYPE', columns='LAST_GRADE', aggfunc=len, fill_value=0)
