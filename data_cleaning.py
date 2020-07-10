import pandas as pd
pd.set_option('display.max_rows', 500)
raw_df = pd.read_csv("C:/Users/shahb/gd_salary_preds/scraped_jobs_raw.csv")

#fix salary estimate - min,max
salary = raw_df['Salary Estimate'].apply(lambda x: x.split("(")[0])
salary = salary.apply(lambda x: x.replace("$","").replace("K",""))

salary = salary.apply(lambda x: x.split("-"))

min_salary = salary.apply(lambda x:x[0])
max_salary = salary.apply(lambda x:x[1])

raw_df['min_salary'] = min_salary
raw_df['max_salary'] = max_salary

raw_df.min_salary = raw_df.min_salary.astype(int)
raw_df.max_salary = raw_df.max_salary.astype(int)

raw_df['avg_salary'] = raw_df[['min_salary','max_salary']].mean(axis=1)

#fix company name

raw_df['Company Name'] = raw_df['Company Name'].apply(lambda x: x.split("\n")[0])

#fix size - min,max

size = raw_df.Size.apply(lambda x: x.replace(' employees',"").replace('Unknown',"-1").replace("+",' to'))

raw_df['min_size'] = size.apply(lambda x: x if '-1' in x else (x.replace(" ","").split('to'))[0])

raw_df['max_size'] = size.apply(lambda x: x if '-1' in x else (x.replace(" ","").split('to'))[1])

raw_df.loc[raw_df.max_size=="",'max_size']=10000

raw_df.min_size = raw_df.min_size.astype(int)
raw_df.max_size = raw_df.max_size.astype(int)

raw_df['avg_size'] = raw_df[['min_size','max_size']].mean(axis=1)

#Fix Location to extract states
raw_df.loc[raw_df.Location=='Remote','Location']='Remote, Remote'
raw_df.loc[raw_df.Location=='Virginia','Location']='Virginia, VA'
raw_df.loc[raw_df.Location=='Minnesota','Location']='Minnesota, MN'
raw_df.loc[raw_df.Location=='Connecticut','Location'] ='Connecticut, CT'
raw_df.loc[raw_df.Location=='New Jersey','Location'] ='New Jersey, NJ'
raw_df.loc[raw_df.Location=='California','Location'] ='California, CA'
raw_df.loc[raw_df.Location=='Greenwood Village, Arapahoe, CO','Location'] = 'Greenwood Village - Araphoe, CO'
raw_df.loc[raw_df.Location=='United States','Location'] =raw_df.loc[raw_df.Location=='United States','Headquarters']

raw_df = raw_df[raw_df.Location != '-1']


cities = raw_df.Location.apply(lambda x: x.split(', ')[0])
states = raw_df.Location.apply(lambda x: x.split(', ')[1])

raw_df['city'] = cities
raw_df['state'] = states

#derive ago of company

raw_df['age'] = raw_df.Founded.apply(lambda x: x if x==-1 else 2020-x)

# major skills

raw_df['python_yn'] = raw_df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
raw_df['R_yn'] = raw_df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() else 0)
raw_df['spark_yn'] = raw_df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
raw_df['aws_yn'] = raw_df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
raw_df['hadoop_yn'] = raw_df['Job Description'].apply(lambda x: 1 if 'hadoop' in x.lower() else 0)

#drop irrelevant columns
raw_df.drop(['Salary Estimate','Job Description','Location','Headquarters','Size','Founded',"Revenue",'Competitors','min_salary','min_size','max_size'],axis=1,inplace=True)

# save csv to disk
raw_df.to_csv("cleaned_data.csv",index=False)