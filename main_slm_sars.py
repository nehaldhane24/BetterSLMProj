from index import GR_based_exclusion,cli_excludes
import requests
import json
import os
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from customerCommentsSummarizer import customerCommentSummary
from excludecomments import excluded_based_on_release, excluded_based_on_config, excluded_based_on_impact

url = "https://api-supplychain.cisco.com/pdafapp/profiles_buglist_global_users/2.0/getProfileBugsListGU"

payload = json.dumps({
  "contractId": "4140",
  "custName": "H AND M",
  "profileName": "N9K_9.3(7)",
  "deliverables": "SARS",
  "limit": 200
})
headers = {
  
  'Content-Type': 'application/json',
  # 'Authorization': 'Bearer 4Y06smMYLwPzPtoaPkM5bUkcLmhj',
   'Authorization': 'Bearer jagNYfY9ye86LwYYPkEkGNwJAU6W',
    'Cookie': '2e572c1106cef1a1a48bb7704ce98235=2e3e8b6cc4174ebba3e9e90382a4931b'
}
response = requests.request("POST", url, headers=headers, data=payload)
  #print(response)


profile_bugs=json.loads(response.text,strict=False)
exc_gr_list=(GR_based_exclusion(profile_bugs))
print("Total excludes after gr based exclusion", len(exc_gr_list))
exc_cli=(cli_excludes(exc_gr_list,profile_bugs))
print("Total excludes after cli based exclusion", len(exc_cli))
# remaining_bug_details=[]
# remaining_bugs=[]
# for profile_info in profile_bugs:
#   if profile_info['bugId'] not in exc_cli:
#     remaining_bug_details.append(profile_info)
#     remaining_bugs.append(profile_info['bugId'])
# #print(remaining_bugs)
# print("Remaining bugs = ",(remaining_bugs))
# print(os.getcwd())
os.chdir(r'C:\\Users\\ndhande\\Downloads')
# remaining_bugs= ['CSCvx63578', 'CSCuy16606', 'CSCvx56768', 'CSCvx68932', 'CSCvx66678', 'CSCvy00029', 'CSCvb66783']
remaining_bugs= ['CSCvx63578']
# bug_ids = ['CSCvx75912']
def one_time_authentication(username, password):
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    URL = "https://cloudsso.cisco.com/as/authorization.oauth2?response_type=code&client_id=wam_prod_ac&redirect_uri=https%3A%2F%2Fdirectory.cisco.com%2Fpa%2Foidc%2Fcb&state=eyJ6aXAiOiJERUYiLCJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2Iiwia2lkIjoiNnMiLCJzdWZmaXgiOiI5Zjk3YlUuMTU4MjUyNDcxMyJ9..mfYP_XXMWUkSk26xqwT4Cg.H3YYZYb10RoVOzfRObRRhotiyXWWxfzQExE_eMk3n87LGYjnEhsWtZjMLoHmX0dMSUTFGagZmY77g7FqwUBOE5BEDEGagvPIARTNJSbKyQg.t7HQ-00koYGp2TtDRkdvCA&nonce=XXgjysS5vZrT_1xXGi5RAau2x0WiTHD3fhz7ajAJTOM&acr_values=stdnomfa&scope=openid%20profile%20address%20email%20phone&vnd_pi_requested_resource=https%3A%2F%2Fdirectory.cisco.com%2Fdir%2Fdetail.cgi%3Fname%3D&vnd_pi_application_name=CAEAIprod-directory"
    driver.maximize_window()
    driver.get(URL)
    driver.implicitly_wait(10)
    username1 = driver.find_element_by_id("userInput")
    username1.send_keys(username)

    submit_button = driver.find_element_by_name("login-button")
    ActionChains(driver).move_to_element(submit_button).click(submit_button).perform()
    driver.implicitly_wait(10)
    
    password1 = driver.find_element_by_name("pf.pass")
    password1.send_keys(password)
    
    submit_button2 = driver.find_element_by_name("login-button")
    ActionChains(driver).move_to_element(submit_button2).click(submit_button2).perform()
    time.sleep(40)
    driver.implicitly_wait(20)
    

    return driver

link = "https://slm.cloudapps.cisco.com/slm/#/asComments?bugId={}&viewType=Internal&isInternalNCE=true&adjacentHlt=false&adjacentIntHlt=true&profileId=29046&adjacentBugId={}&source=Master%20Project&selectedTab=Impacted"
def fetch_data(driver,contract,profile,link,bug_id):
    
    #load slm page
    link = link.format(bug_id, bug_id)
    driver.get(link)
    time.sleep(10)
    driver.implicitly_wait(40) 
    
    return driver
    

with open('config.json','r') as fp:
        conf = json.load(fp)
        username = conf['username']
        password = conf['password']
        profile = conf['profile']
        contract = conf['contract']
driver = one_time_authentication(username, password)

for bug_id in remaining_bugs:
    listOfComments=[]
    driver=fetch_data(driver,contract,profile,link,bug_id)
    time.sleep(10)
    driver.implicitly_wait(10)

#Load more/all comments button
#load_all_cmts=driver.find_element_by_xpath('//*[@id="topcomments"]/div/div/div[3]/button[2]')
    wait = WebDriverWait(driver, 10)
    # load_all_cmts = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="topcomments"]/div/div/div[3]/button[2]')))
    load_all_cmts = driver.find_element(By.XPATH, '//*[@id="topcomments"]/div/div/div[3]/button[2]')
    ActionChains(driver).move_to_element(load_all_cmts).click(load_all_cmts).perform()
    time.sleep(10)
    driver.implicitly_wait(10) 

#Read all data
#pop_up=driver.find_element_by_xpath("//*[@id='topcomments']")
    pop_up =wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='topcomments']")))
    summary=""
    summary=pop_up.text+'\n\n\n\n'
    time.sleep(10)
    driver.implicitly_wait(10) 
    #print(summary)
    # listOfComments.append(summary)
    # print(listOfComments)
    # print(count)
    
    listC=summary.split('Comments:')
    print("after split = ", listC)
    listOfComments = ([x.replace('\n', '') for x in listC if x != '\n'])
    print("List of Comments = ",listOfComments)
    print("List of Comments = ",len(listOfComments))
    print("Details for ", bug_id)
    # with open('output.txt','w') as file_open:
    clean_list_comments=[]
    for each in listOfComments:
        
        each=re.sub(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d+, \d+Customer:.+", "", each)
        clean_list_comments.append(each)
        #print("each = ", each)
    #print("after cleaning = ",clean_list_comments)
    reduced_comments,count=customerCommentSummary(clean_list_comments)
    #print("All comments = ", reduced_comments)
    # excluded_based_on_release(reduced_comments,exc_cli,bug_id)
    exc_impacts=excluded_based_on_impact(reduced_comments,exc_cli,bug_id)
    print("Total excludes after excluding based on impact from comments = ", len(exc_impacts))
    print("Excluded based on impact = ",exc_impacts)
    exc_configs=excluded_based_on_config(reduced_comments,exc_cli,bug_id)
    print("Total excludes after excluding based on configs from comments = ", len(exc_configs))
    print("Excluded based on config from the comment",exc_configs)
    exc_release=excluded_based_on_release(reduced_comments,exc_configs,bug_id)
    print("Excluded based on config from the comment",exc_release)
    os.chdir(r'C:\\Users\\ndhande\\Downloads')
    exc_hw=excluded_based_on_hw(reduced_comments,exc_hw,bug_id)
    print("Excluded based on config from the comment",exc_hw)

    


    # time.sleep(10)
    file = open("scraped_potential_bugs.txt", "a", encoding='utf-8')
    file.write(summary)
    file.close()

    # print("End of program")

driver.quit()



