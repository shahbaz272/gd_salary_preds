import selenium_scraper as sc
import pandas as pd
driver_path = "C:/Users/shahb/gd_salary_preds/chromedriver.exe"
#df = sc.get_jobs('Data Science',1000,True,driver_path)
#df.to_csv("scraped_jobs_raw.csv",index=False)

raw_df = pd.read_csv('scraped_jobs_raw.csv')

raw_df.head()

pwprint('done')
