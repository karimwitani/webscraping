import os
from datetime import date
from datetime import datetime as dt
import shutil
import pandas as pd
from datetime import datetime

import sqlite3
import pandas as pd
conn = sqlite3.connect('./clickup_sales.db')
cursor = conn.cursor()

from sqlalchemy import create_engine
engine = create_engine('sqlite:///clickup_sales.db', echo=True)




dates = pd.read_sql("SELECT DISTINCT AUDIT_DATE FROM LEADS_STATUS order by AUDIT_DATE desc",conn)
most_recent_audit = dates.iloc[0,0]
previous_audit = dates.iloc[1,0]


current_audit = pd.read_sql(f"SELECT  * FROM LEADS_STATUS WHERE AUDIT_DATE = '{most_recent_audit}'",conn)

# 1- 


analysis_sql = {}
analysis_sql_1_1= f"""
    SELECT * FROM LEADS_STATUS
    WHERE ASSIGNEE = '[Ese]'
        AND AUDIT_DATE = '{most_recent_audit}'
"""

analysis_sql_1_2= f"""
    SELECT * FROM LEADS_STATUS
    WHERE ASSIGNEE = '[Ese]'
        AND AUDIT_DATE = '{previous_audit}'
"""

analysis_1_1 = pd.read_sql(analysis_sql_1_1 ,conn)
analysis_1_2 = pd.read_sql(analysis_sql_1_2,conn)

analysis_1_3 = analysis_1_1.merge(analysis_1_2,how='left',left_on='TASK_ID',right_on='TASK_ID',suffixes=['_current','_previous'])
analysis_1_3 = analysis_1_3[analysis_1_3['STATUS_current']!=analysis_1_3['STATUS_previous']]
analysis_1_3['STATUS_previous'][analysis_1_3['STATUS_previous'].isnull()] = 'New'


# 2- 
analysis_2_1 = analysis_1_3[['STATUS_current','STATUS_previous']]
analysis_2_1 = analysis_2_1['STATUS_current'].value_counts()
analysis_2_1 = pd.DataFrame(analysis_2_1)
analysis_2_1['Percentage'] = analysis_2_1['STATUS_current'] / analysis_2_1['STATUS_current'].sum() *100
analysis_2_1['Percentage']  = pd.Series(["{0:.2f}%".format(val ) for val in analysis_2_1['Percentage']], index = analysis_2_1.index)

result_closed_lost = analysis_2_1.loc['closed [lost]']['STATUS_current']
result_intro = analysis_2_1.loc['intro call']['STATUS_current']
result_dev = analysis_2_1.loc['in-development']['STATUS_current']
result_agmnt = analysis_2_1.loc['agreement sent']['STATUS_current']

# 3- 

analysis_3_1 =  pd.pivot_table(analysis_1_3,index='STATUS_current',columns='STATUS_previous',values='TASK_ID',aggfunc='count')
analysis_3_1

# 4- 
analysis_4_1 = analysis_1_1.merge(analysis_1_2,how='left',left_on='TASK_ID',right_on='TASK_ID',suffixes=['_current','_previous'])
analysis_4_1 = analysis_4_1[analysis_4_1['STATUS_current']==analysis_4_1['STATUS_previous']]
analysis_4_1 = analysis_4_1[['TASK_ID', 'TASK_NAME_current', 'STATUS_current','DATE_CREATED_current', 'AUDIT_DATE_current', 'ASSIGNEE_current']]
analysis_4_1['AUDIT_DATE_current'] =  pd.to_datetime(analysis_4_1['AUDIT_DATE_current'])
analysis_4_1['DATE_CREATED_current'] =  pd.to_datetime(analysis_4_1['DATE_CREATED_current'])
analysis_4_1['DIFF'] = analysis_4_1['AUDIT_DATE_current']-analysis_4_1['DATE_CREATED_current']
analysis_4_1= analysis_4_1[analysis_4_1['STATUS_current']!='closed [lost]']
analysis_4_1