import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from distutils.version import LooseVersion, StrictVersion
from pkg_resources import parse_version
import os
from nltk import pos_tag
from validatations import validate_configurations, validate_hw
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
target_release="9.3.7"
#keys=["nexus","catalyst","asr","ncs","aironet","mds","industrial ethernet","industrial wireless","flex","me","isr","cbr","network convergence system","vg300","cucm","ios xr","integrated services routers","wireless controller","series routers","multiservice platforms","cloud services router","embedded services routers","grid routers","carrier routing system","wireless lan controllers","universal gateways","sd-wan routers"]
#keys_dictionary={"nexus":["nexus","n"],"catalyst":["catalyst","cat","c"],"asr":["asr"],"ncs":["ncs"],"aironet":["aironet","air"],"mds":["mds"],"industrial ethernet":["industrial ethernet","ie"],"industrial wireless":["industrial wireless","iw"],"flex":["flex"],"me":["me"],"isr":["isr"],"cbr":["cbr"],"network convergence system":["network convergence system"],"vg300":["vg300"],"cucm":["cucm"],"ios xr":["ios xr","iosxr"],"integrated services routers":["integrated services routers"],"wireless controller":["wireless controller"],"series routers":["series routers"],"multiservice platforms":["multiservice platforms"],"cloud services router":["cloud services router","csr"],"embedded services routers":["embedded services routers","esr"],"grid routers":["grid routers","cgr"],"carrier routing system":["carrier routing system","crs"],"wireless lan controllers":["wireless lan controllers","wlc"],"universal gateways":["universal gateways","ug"],"sd-wan routers":["sd-wan routers","sd-wan","sdwan"]}

def excluded_based_on_impact(list_of_comments,excluded_bugs,bug_id):
    excluded_bugs=[]
    exclude_list_file = open('impact.txt', 'r')
    exclude_list = exclude_list_file.readlines()
    print(exclude_list)
    exclude_list = [(x.replace('\n','')).lower() for x in exclude_list]
    print(exclude_list)
    for comment in list_of_comments:
        for x in exclude_list:
            #print(comment,' ',x,'\n')
            if x in comment:
                # pass
                # add to excluded_bugs reason
                
                if bug_id not in excluded_bugs:
                    excluded_bugs[bug_id] = comment
                else:
                    excluded_bugs[bug_id] +=  ', '+comment
            
    #print(excluded_bugs)
    return excluded_bugs

def excluded_based_on_release(list_of_comments,excluded_bugs,bugId):
    comment_to_be_added=""
    phrases=["not our tr","our tr is safe","fixed in our tr","our tr should be safe","fixed in our target release", "our target release is safe","does not affect our release","our target release throttle should be safe."]
    exc_release=[]
    for each_comment in list_of_comments:
        
        each_comment=each_comment.lower()
        for phr in phrases:
            if phr in each_comment:
               
                r1 = re.findall(r'\d+\.\d+\(\w+\)', each_comment)
                r2= re.findall(r'\d+\.\d+.\d+', each_comment)
                exc_release.extend(r1)
                exc_release.extend(r2)
                r3=list(set(re.findall(r'not-required-in-\w\d+', each_comment)))
              
                print(each_comment)
                print('re = ',r3)
                exc_release.extend(r3)
        if(len(exc_release)>=1):
            comment_to_be_added=each_comment
            break

    print(exc_release)
    for each in exc_release:
        if parse_version(each) > target_release:
            if bugId not in excluded_bugs:
                excluded_bugs[bugId] = comment_to_be_added
            else:
                excluded_bugs[bugId] +=  ', '+ comment_to_be_added
    return excluded_bugs 


    

def excluded_based_on_hw(list_of_comments,excluded_bugs,bugId):
    exc_hw=[]
    comment_to_be_added=""
    for each_comment in list_of_comments:
        each_comment=each_comment.lower()
        if("not our hardware" in each_comment or "not our hw" in each_comment or "hw should be safe" in each_comment  or "hw is safe" in each_comment):
            print(each_comment)
            r1=re.findall(r'\w+-\w+-\w+', each_comment)
            print(r1)
            r2=re.findall(r'\w+-\w+', each_comment)
            print(r2)
            exc_hw.extend(r1)
            exc_hw.extend(r2)
            #validate this in inventory
    if(len(exc_hw)>=1):
        comment_to_be_added=each_comment
      
    for each_check in exc_hw:
        flag=validate_hw(each_check.strip())
        print("Flag after all checks = ",flag)
        if(flag == "not found"):
            if bugId not in excluded_bugs:
                excluded_bugs[bugId] = comment_to_be_added
            else:
                excluded_bugs[bugId] +=  ', '+ comment_to_be_added
            
    return 0


def excluded_based_on_config(list_of_comments,excluded_bugs,bugId):
    validate_configs_list=[]
    comment_to_be_added=""
    for each_comment in list_of_comments:

        each_comment=each_comment.lower()
        res1 = re.findall(r"no [\w\s\"\"*]+ configured",each_comment)
        #print(res1)
        res2 = re.findall(r"[\w\s\"\"*]+ is not configured",each_comment)
        #print(res2)
        res3 = re.findall(r"[\w\s\"\"*]+ is not present",each_comment)
        #print(res3)
        res4 = re.findall(r"[\w\s\"\"*]+ is not present as per customer config",each_comment)
        #print(res4)
       
        res6 = re.findall(r"no [\w\s\"\"*]+ as per customer config",each_comment)
        
        #print(res6)
        res7 = re.findall(r"no [\w\s\"\"*]+ in customer config",each_comment)
        #print(res7)
        res8 = re.findall(r"[\w\s\"\"*]+ not used",each_comment)
        res9 = re.findall(r"no [\w\s\"\"*]+",each_comment)
        #print(res8)
        
        validate_configs_list.extend(res1)
        validate_configs_list.extend(res2)
        validate_configs_list.extend(res3)
        validate_configs_list.extend(res4)
        validate_configs_list.extend(res6)
        validate_configs_list.extend(res7)
        validate_configs_list.extend(res8)
        validate_configs_list.extend(res9)
        if(len(validate_configs_list)>=1):
            comment_to_be_added=each_comment
            break


    print(validate_configs_list)
    stopwords1=['customer', 'config', 'configuration', 'configurations', 'configs','per','files']
    stop_words = set(stopwords.words('english'))
    for each in validate_configs_list:
        word_tokens = word_tokenize(each)
        print(word_tokens)
        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
        print("after remobing stop words = ",filtered_sentence)
        res = [ele for ele in filtered_sentence if ele.strip("``")]
        res_cleaned = [ele for ele in res if ele.strip("''")]
        joined = " ".join(res)
        print("joining filtered sentence = ",joined)
        sentence = nltk.word_tokenize(joined)
        sent = pos_tag(sentence) 
        print("Sent pos tagging = ",sent)
        sent_clean = [x for (x,y) in sent if not y.startswith('V') ]
        print("Sent after remivin verbs= ", sent_clean)
        new_words = [word for word in sent_clean if word not in stopwords1]
        print("Sent after remivin verbs= ", new_words)
        new_words_joined= " ".join(new_words)
        new_words_joined=new_words_joined.strip("``")
        print('final = ', new_words_joined)
        check=new_words_joined.split("``")
        print("check = ",check)
        #validate in configs or in featurelist
        for each_check in check:
            flag=validate_configurations(each_check.strip())
        print("Flag after all checks = ",flag)
        if(flag == "not found"):
            if bugId not in excluded_bugs:
                excluded_bugs[bugId] = comment_to_be_added
            else:
                excluded_bugs[bugId] +=  ', '+ comment_to_be_added
    return excluded_bugs 
def excluded_based_on_DE():
    return 0
# list_of_comments=[['''CSCvx63578Apr 27, 2021nipbhas updatedRelease:9.3(1)Source: SystemSelection Status:IncludeProduct Family:Cisco Nexus 9000 Series Switches10:13 PM', 'Symptoms:VSH crash observed in this issue.Conditions:This issue is seen with below conditions.1. DCNM tracker Installed2. Potential scripts collecting "show processes cpu" data3. This issue occurs when the number of processes in the switch reaches above 512.Summary:VSH (Virtual Shell) crash observed 
# in this issue. This issue is seen with below conditions.1. DCNM (Data Center Network Manager) tracker Installed2. Potential scripts collecting "show processes cpu" data3. This issue occurs when the number of processes in the switch reaches above 512.This issue is caused due to HB miss. As a workaround, stop polling show processes or show processes data using multiple VSH sessions.CLI:NATrigger:This issue is caused due to HB missRepro:NAImpactImpact Category:process crashImpact Description:In this issue DCNM tracker polling show processes CPU continuously user would have Core in VSH. VSH(Virtual Shell) gets killed by 
# SIGABRT and is not tapping HB. it looks like MTS queue issue.WorkaroundAvailable:YesAvoidance:NARecovery:As a workaround, stop polling show processes or show processes data using multiple VSH sessions.Fixed In:NAImpacted PlatformsImpact Type:OnlyPlatform List:NAFeature:StandardArchitecture:DCTechnology:StandardHardwareImpact Type:OnlyHardware List:NAFound:Customer Found', 'Exclude.As per Release-note,DCNM tracker InstalledPotential scripts collecting "show processes cpu" dataNote: Installation of a DCNM tracker leads to the installation of a small utility that runs on the guestshell of the switch and monitors changes in intent, running configuration, and so on.https://www.cisco.com/c/en/us/td/docs/switches/datacenter/sw/11_4_1/config_guide/lanfabric/b_dcnm_fabric_lan/control.html#concept_ahq_jzf_xjbNo "guestshell" or "DCNM" as per given files.', 'No DCNMExclude:As per Release-note: DCNM tracker InstalledPotential scripts collecting "show processes cpu" dataNot customer scenario.Note: Installation of a DCNM tracker leads to the installation of a small utility that runs on the 
# guestshell of the switch and monitors changes in intent, running configuration, and so on.https://www.cisco.com/c/en/us/td/docs/switches/datacenter/sw/11_4_1/config_guide/lanfabric/b_dcnm_fabric_lan/control.html#concept_ahq_jzf_xjbNo "guestshell"', 'Exclude:As per Release-note,DCNM tracker InstalledPotential scripts collecting "show processes cpu" dataNote: Installation of a DCNM tracker leads to the installation of a small utility that runs on the guestshell of the switch and monitors changes in intent, running configuration, and so on.https://www.cisco.com/c/en/us/td/docs/switches/datacenter/sw/11_4_1/config_guide/lanfabric/b_dcnm_fabric_lan/control.html#concept_ahq_jzf_xjbNo "guestshell" or "DCNM" as per config.', 'Not our case. No DCNM.', 'Exclude.DCNM related.', 'Exclude.As per no-verify Created By:rimichae Created On:04/02/2021 19:07:52Updated By:rimichaeUpdated On:04/02/2021 19:07:52CSCvx86833 - Final fix is in parser where the verification will be done. This is done to increase the PID count from 512 to 1024 and implement the design change in sysinfo part to handle more PID flags correctly.CSCvx86833 added to this project hence excluding this one', 'Exclude:As per RNE <B>Conditions:</B>DCNM tracker InstalledPotential scripts collecting "show processes cpu" dataNot our scenario. No DCNM.', 'Excl:<B>Conditions:</B>DCNM tracker InstalledPotential scripts collecting "show processes cpu" dataNo info abt DCNM', 'Exclude:As per Release-note: DCNM tracker InstalledPotential scripts collecting "show processes cpu" dataNote: Installation of a DCNM tracker leads to the installation of a small utility that runs on the guestshell of the switch and monitors changes in intent, running configuration, and so on.https://www.cisco.com/c/en/us/td/docs/switches/datacenter/sw/11_4_1/config_guide/lanfabric/b_dcnm_fabric_lan/control.html#concept_ahq_jzf_xjbNo "DCNM" in feature list.', 'ExcludeConditions:DCNM tracker InstalledPotential scripts collecting "show processes cpu" dataNot our scenario', 'Exclude:As 
# per no-verify:CSCvx86833 - Final fix is in parser where the verification will be done. This is done to increase the PID count from 512 to 1024 and implement the design change in sysinfo part to handle more PID flags correctly.CSCvx86833 added to this project hence excluding this one', 'Symptoms:VSH crash observed in this issue.Impact Description:In this issue DCNM tracker polling show processes CPU continuously user would have Core in VSH. VSH(Virtual Shell) gets 
# killed by SIGABRT and is not tapping HB. it looks like MTS queue issue.Trigger Description:This issue is caused due to HB missConditions:This issue is seen 
# with below conditions.1. DCNM tracker Installed2. Potential scripts collecting "show processes cpu" data3. This issue occurs when the number of processes in the switch reaches above 512.Workaround Available:YesWorkaround Recovery:As a workaround, stop polling show processes or show processes data using multiple VSH sessions.', '<Pmaruthi>ExcludeExclude:As per no-verifyCreated By:rimichae Created On:04/02/2021 19:07:52Updated By:rimichaeUpdated On:04/02/2021 19:07:52CSCvx86833 - Final fix is in parser where the verification will be done. This is done to increase the PID count from 512 to 1024 and implement the design 
# change in sysinfo part to handle more PID flags correctly.CSCvx86833 added to this project hence excluding this one', 'Exclude:As per RNE:<B>Conditions:</B>DCNM tracker InstalledPotential scripts collecting "show processes cpu" dataNo "guestshell"  no DCNM tracker.', 'Exclude:As per no-verify Created By:rimichae Created On:04/02/2021 19:07:52Updated By:rimichaeUpdated On:04/02/2021 19:07:52CSCvx86833 - Final fix is in parser where the verification will be done. This is done to increase the PID count from 512 to 1024 and implement the design change in sysinfo part to handle more PID flags correctly.CSCvx86833 added to this project hence excluding this oneClose''']


# list_of_comments=['''Exclude:
# As per headline: N9000 syslogs incorrect PTP messages when loss of GM is detected

# No "feature ptp" in customer config. Hence, excluding.''', """Exclude.

# As per <B>Symptom:</B>
# N9000 and N3000 do syslog incorrect PTP messages when primary GM is lost. 
# First message logged says that GM changed from original one to new one which is typically switch with best clock parameters (priority1 etc) but that's not what BMCA does as first step.

# Not using PTP as per given files.""", """Exclude:
# It is a cosmetic issue with no functional/operational   or customer impact, hence excluding this issue as per the GR.
# As per the Detection Unsuitable:
# NX-OS PTPT implementation is compliant to IEEE1588 v2 (clause 9.3.2).
# The only issue is the incorrectly printed log message regarding Grandmaster change.
# Thus considered as cosmetic issue and  will not be automated.
# As per the scrubnote:
#  {210327 vakannap S B} No issues with functionality, no operations or  customer impact.""","""Exclude:

# <B>Conditions:</B>
# VXLAN configuration on C8500-12X using replication mode Multicast.
# The range of default reserved VLANs  (3968 to 4047 and 4094) was change with the command "system vlan <vlan-id> reserve"

# Not our HW. system vlan * not used.""","""Feature ptp is not used""","""not a production scenario""","""Exclude:
# As per Not-Required-in-r71x:
# Created By:chunjwanCreated On:11/06/2020 18:36:32
# Updated By:chunjwanUpdated On:11/06/2020 18:36:32
# Not-Required-In-v1612_throttle

# Our TR should be safe. 
# ""","""Fixed in 6.3.2, hence our TR should be safe"""]

#excluded_based_on_config(list_of_comments)
#excluded_based_on_hw(list_of_comments)
# direct_exclude(list_of_comments)
# for root, dirs, files in os.walk('nbs_n7k/Config'):
#     for file in files:
#         if file.endswith('.txt'):
#             print(file)
#             filepath='nbs_n7k/Config/'+file
#             f1=open(filepath,'r')
#             configs = f1.readlines()
#             print(configs)
        
            