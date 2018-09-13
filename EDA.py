import pandas as pd

def clean_df(filename, report_month, original_program_begin_date):
    '''This intakes a file as a string and will output a clean dataframe
    INTAKE:
            filename: string
            report_month: string '2016-01-01'
            original_program_begin_date: string '2016-01-01'
    '''
    student_df = pd.read_csv(filename)
    del student_df['ETHNICITY']
    del student_df['PROG_GPA']
    student_df.dropna(inplace=True)
    jan_june_df = student_df[(student_df['REPORT_MONTH'] < report_month) &
                               (student_df['ORIGINAL_PROGRAM_BEGIN_DATE'] == original_program_begin_date)].sort_values(by=['ACCOUNT_ID', 'REPORT_MONTH'])
    jan04_grouped = jan_june_df.groupby('ACCOUNT_ID',as_index=False)['Y_VAR'].sum()
    jan04_grouped.rename(index=str, columns={"Y_VAR": "COUNT"}, inplace=True)
    new_student_df = jan_june_df.merge(jan04_grouped, how='inner', on='ACCOUNT_ID')
    return new_student_df

#Check for nulls
student_df[student_df['PACE'].isnull()]['ACCOUNT_ID'].nunique()

#Check for number of rows and columns
student_df.shape

#Check to see how many male/female
student_df['GENDER'].value_counts()

#Check dtype for each column
student_df.info()

def unique_values(df):
    """
    Input: dataframe
    Output: Print out which indicates the number of unique values in each columns
    """
    for col in df.columns:
        print("There are {} unique values in the {} column".format(df[col].nunique(), col))

#Correlation plot to determine which variables have high correlation
cormat = student_df.corr()
f, ax = plt.subplots(figsize=(30, 30))
sns.heatmap(cormat, vmax=.8, square=True,annot=True, fmt='.2f')
plt.show()
