import os
from time import sleep
import pandas as pd
import csv
from datetime import datetime
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from sqlalchemy import create_engine



engine = create_engine('sqlite:///mailchimp_test.db', echo=True)


Download_Dir = {
    'MailChimp': '/Users/karim/Downloads/Mailchimp_downloads/'
}


col_renames = {
  'Unsubscribed':{
        'Email Address':'EMAIL',
        'First Name':'FIRST_NAME', 
        'Last Name':'LAST_NAME',
        'Address':'ADDRESS', 
        'Phone Number':'PHONE',
        'Company':'COMPANY',
        'Full Name':'FUll_NAME',
        'Company Size':'COMPANY_SIZE',
        'Member Rating':'MEMBER_RATING',
        'reason':'REASON',
        'description':'DESCRIPTION'},

    'Didnt_open':{
        'Email Address':'EMAIL',
        'First Name':'FIRST_NAME', 
        'Last Name':'LAST_NAME',
        'Address':'ADDRESS', 
        'Phone Number':'PHONE',
        'Company':'COMPANY',
        'Full Name':'FUll_NAME',
        'Company Size':'COMPANY_SIZE',
        'Member Rating':'MEMBER_RATING'},

    'Bounced':{
        'Email Address':'EMAIL',
        'First Name':'FIRST_NAME', 
        'Last Name':'LAST_NAME',
        'Address':'ADDRESS', 
        'Phone Number':'PHONE',
        'Company':'COMPANY',
        'Full Name':'FUll_NAME',
        'Company Size':'COMPANY_SIZE',
        'Member Rating':'MEMBER_RATING',
        'Bounce Type':'BOUNCE_TYPE'},
    
    'Clicked':{
        'Email Address':'EMAIL',
        'First Name':'FIRST_NAME', 
        'Last Name':'LAST_NAME',
        'Address':'ADDRESS', 
        'Phone Number':'PHONE',
        'Company':'COMPANY',
        'Full Name':'FUll_NAME',
        'Company Size':'COMPANY_SIZE',
        'Member Rating':'MEMBER_RATING',
        'URL':'URL',
        'Clicks':'CLICKS'},
    
    'Opened':{
        'Email Address':'EMAIL',
        'First Name':'FIRST_NAME', 
        'Last Name':'LAST_NAME',
        'Address':'ADDRESS', 
        'Phone Number':'PHONE',
        'Company':'COMPANY',
        'Full Name':'FUll_NAME',
        'Company Size':'COMPANY_SIZE',
        'Member Rating':'MEMBER_RATING',
        'Opens':'OPENS'},
    
    'Sent_to':{
        'Email Address':'EMAIL',
        'First Name':'FIRST_NAME', 
        'Last Name':'LAST_NAME',
        'Address':'ADDRESS', 
        'Phone Number':'PHONE',
        'Company':'COMPANY',
        'Full Name':'FUll_NAME',
        'Company Size':'COMPANY_SIZE',
        'Member Rating':'MEMBER_RATING'},
}  


db_cols = {
    'Unsubscribed':['EMAIL','FIRST_NAME','LAST_NAME','ADDRESS', 'PHONE','COMPANY','FUll_NAME','COMPANY_SIZE','MEMBER_RATING','REASON','DESCRIPTION'],

    'Didnt_open':['EMAIL','FIRST_NAME','LAST_NAME','ADDRESS','PHONE','COMPANY','FUll_NAME','COMPANY_SIZE','MEMBER_RATING'],

    'Bounced':['EMAIL','FIRST_NAME', 'LAST_NAME','ADDRESS','PHONE','COMPANY','FUll_NAME','COMPANY_SIZE','MEMBER_RATING','BOUNCE_TYPE'],
    
    'Clicked':['EMAIL','FIRST_NAME', 'LAST_NAME','ADDRESS', 'PHONE','COMPANY','FUll_NAME','COMPANY_SIZE','MEMBER_RATING','URL','CLICKS'],
    
    'Opened':['EMAIL','FIRST_NAME', 'LAST_NAME','ADDRESS', 'PHONE','COMPANY','FUll_NAME','COMPANY_SIZE','MEMBER_RATING','OPENS'],
    
    'Sent_to':['EMAIL','FIRST_NAME', 'LAST_NAME','ADDRESS', 'PHONE','COMPANY','FUll_NAME','COMPANY_SIZE','MEMBER_RATING'],
}  

file_table_mapping={
    'Unsubscribed':'UNSUB',

    'Didnt_open':'UNOPEN',
    
    'Bounced':'BOUNCE',
    
    'Clicked':'CLICKED',
    
    'Opened':'OPEN',
    
    'Sent_to':'SENT'
}

Download_Dir = {
    'MailChimp': '/Users/karim/Downloads/Mailchimp_downloads/'
}

def browser_init(workflow):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : Download_Dir['MailChimp']}
    chrome_options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(executable_path='/Library/Application Support/Google/chromedriver', chrome_options=chrome_options)
    return browser



def browser_init(workflow):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : Download_Dir['MailChimp']}
    chrome_options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(executable_path='/Library/Application Support/Google/chromedriver', chrome_options=chrome_options)
    return browser



def mailchimp_login(browser):
    #Go to webpage
    browser.get("https://mailchimp.com/")
    
    #Login Menu --> will ask for verification
    WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CLASS_NAME,'globalNav__actions__login'))).click() #login_button 

    #Find username/pass fields
    username = WebDriverWait(browser,4).until(EC.element_to_be_clickable((By.NAME, 'username')))
    password = WebDriverWait(browser,4).until(EC.element_to_be_clickable((By.NAME, 'password')))

    #input username and pass
    username.clear()
    username.send_keys('age_group')
    password.clear()
    password.send_keys('fourteen_gold')

    #press login button
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login-form"]/fieldset/div[4]/button'))).click() #login_button 

    #email verification workflow
    try:
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="send-email-code-step1"]/button'))).click()
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-close-btn-container"]/button'))).click()
    except TimeoutException:
        pass
    verification_code = input("Code sent! Please check your email and use the box below to submit the verification code.")
    input_verification_code = browser.find_element(By.ID, 'email_code')
    input_verification_code.send_keys(verification_code)
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login-verify-fieldset"]/div[3]/div/button'))).click() #submit_verification 


def switch_to_fallback_iframe(browser):
    campaigns = browser.find_element(By.XPATH,"//iframe[@id='fallback']")
    browser.switch_to.frame(campaigns)

def convert_str_datetime(string):
    string =string.replace(',','').split(' ')
    string[-1] = string[-1].upper()
    string = ":".join(string)
    string= datetime.strptime(string, "%a:%b:%d:%Y:%I:%M:%p")
    return string

def locate_campaign_blocks(browser):
    browser.get("https://us7.admin.mailchimp.com/campaigns/")
    switch_to_fallback_iframe(browser)
    campaignManager = browser.find_elements(By.XPATH, '//*[@id="tabList"]/div/div/div/div[2]/div[2]/div[2]')
    campaignManager = browser.find_element(By.CLASS_NAME, 'c-campaignManager_list')
    monthly_lists= campaignManager.find_elements(By.CSS_SELECTOR, ".c-campaignManager_list_group.margin--lv4.margin-bottom--lv0.margin-right--lv0.margin-left--lv0")
    blocks = {}
    for i in monthly_lists:
        date = i.find_element(By.TAG_NAME,'h6').text
        print(f'date: {date}')
        block = i
        blocks[date]=block
    return monthly_lists

def get_monthly_campaigns(monthly_lists, index=0):
    campaigns = monthly_lists[index].find_elements(By.CSS_SELECTOR, ".c-campaignManager_slat.flex.position--relative.flex-between.flex-justify--start.padding--lv3.padding-left--lv1.padding-right--lv0")
    return campaigns

def processed_campaign_filter(campaigns):
    campaigns_to_process = []
    processed = pd.read_csv('processed_campaigns.csv',header=0)["name"].tolist()
    with open('processed_campaigns.csv', 'a', newline='') as f_object:
        writer_object = csv.writer(f_object)
        for c in campaigns:
            name = c.find_element(By.TAG_NAME, 'h4').find_element(By.TAG_NAME,'a').text
            report_link = c.find_element(By.XPATH,'./div[6]/table/tbody/tr/td[1]/div/div[2]/a').get_attribute('href')
            status = c.find_element(By.CSS_SELECTOR, '.c-campaignManager_slat_status.margin-bottom--lv2').find_element(By.CLASS_NAME,'badge').text
            if status == 'Sent':
                if name not in processed:
                    print(f'adding {name}')
                    campaigns_to_process.append(c)
                    single_campaign = [name,report_link]
                    writer_object.writerow(single_campaign) 
                else:
                    pass
            else:
                pass

    f_object.close()
    return campaigns_to_process

def get_campaigns_month(c):
    summary = {}
        
    name = c.find_element(By.TAG_NAME, 'h4').find_element(By.TAG_NAME,'a').text
    status = c.find_element(By.CSS_SELECTOR, '.c-campaignManager_slat_status.margin-bottom--lv2').find_element(By.CLASS_NAME,'badge').text
    report_link = c.find_element(By.XPATH,'./div[6]/table/tbody/tr/td[1]/div/div[2]/a').get_attribute('href')
    if status == 'Sent':
        print(f'Processing {name}')
        summary[name]={}
        summary[name]['status']=status
        summary[name]['link']=report_link
        df = pd.DataFrame.from_dict(summary, orient='index')
        return df
    else:
        print(f'Not sent yet: {name}, skipping')
    
    return summary
    

def get_activity_links(browser,df):
    for x in range(len(df)):
        browser.get(df.iloc[x,1])
        switch_to_fallback_iframe(browser)
        
        activity_blocks  = browser.find_element(By.XPATH,'//*[@id="dijit__FocusMixin_1"]').find_elements(By.TAG_NAME,'li')
        date = browser.find_element(By.XPATH,'//*[@id="report-wrapper"]/div/div[1]/div[2]/div[2]/ul/li[1]/span[2]').text
        df['date'] = convert_str_datetime(date)
        activity_links = []

        print(df.index[0])
        for y in activity_blocks:
            link = y.find_element(By.TAG_NAME,'a').get_attribute('href')
            section = y.find_element(By.TAG_NAME,'a').get_attribute('text')
            #print(section, link, date)
            activity_links.append([section, link])

        activity_df = pd.DataFrame(activity_links, columns=['section', 'link'])

    return activity_df

def download_activity_report(browser,activity_df, Download_Dir=Download_Dir['MailChimp']):
    idx = activity_df.shape[0]
    for ix in range(idx):
        section = activity_df.iloc[ix,0]
        link = activity_df.iloc[ix,1]
        browser.get(link)
        switch_to_fallback_iframe(browser)
        print(f'index: {ix}, section: {section}, link {link}')
        
        if ix == 0:
            browser.find_element(By.XPATH,'//*[@id="report-wrapper"]/div/div[2]/div[1]/div[1]/div[2]/span/a').click() #This Xpath for activity_link[0]
            sleep(2)
            tiny_file_rename(f'{section}.csv',Download_Dir)
        else:
            try:
                browser.find_element(By.CSS_SELECTOR,'.button.hide-phone').click() #This Xpath for activity_link[1:], needs to be put in a try except block as some of the link won't have exports available (e.g: if no one unsubscribed)
                sleep(2)
                tiny_file_rename(f'{section}.csv',Download_Dir)
            except Exception as e:
                print(e)


def tiny_file_rename(newname, folder_of_download, time_to_wait=60):
    newname = newname.replace(' ','_').replace("'","")
    filename = max([f for f in os.listdir(folder_of_download)], key=lambda xa :   os.path.getctime(os.path.join(folder_of_download,xa)))
    os.rename(os.path.join(folder_of_download, filename), os.path.join(folder_of_download, newname))


def reports_csv_to_dfs(download_dir):
    df_dict = {}
    for i in os.listdir(download_dir):
        if i.endswith('.csv'):
            df_name = i.replace('.csv','')
            report = i.replace('.csv','')
            print(df_name)
            print(type(df_name))
            file_dir = f"{Download_Dir['MailChimp']+i}"
            print(file_dir)
            exec(f"{report} = pd.read_csv('{file_dir}', header=0, index_col=False)")
            exec(f"df_dict['{df_name}']={report}")
            os.remove(download_dir + i)
    return df_dict


def process_df_columns(df_dict,summary_df,db_cols):
    print('..1')
    for k,v  in df_dict.items(): 
        try:
            print(k)
            print(v.columns)
            v.rename(columns=col_renames[k], errors='ignore', inplace=True)
            v = v[db_cols[k]]
            print(f'v.cols: \n{v.columns}')
            # v.drop(columns = ['UID','MAILCHIMP_IMPORT','CLICKUP_IMPORT','Index'], axis=1,inplace=True)
            v['CAMPAIGN'] = summary_df.index[0]
            print('..2')
            print(summary_df.iloc[0,2])
            v['DATE'] = summary_df.iloc[0,2]
            print('..3')
            print(v.columns)

        except Exception as e:
            print('..4')
            print(e)

def send_to_database(df_dict,engine):
    for k,v  in df_dict.items(): 
        try:
            df_dict[k].to_sql(file_table_mapping[k], con=engine,index=False,  if_exists='append')
        except Exception as e:
            print(e)