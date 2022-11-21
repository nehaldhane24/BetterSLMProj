import os
import glob
import re
def validate_configurations(config):
    os.chdir(r'C:\\Users\\ndhande\\Downloads\\PACIFIC_GAS_AND_ELECTRIC_Cat3850_and_Cat3650_PSRR_Raw_2022-10-10T13-28-31.283325\\Show Startup-Config')
    my_files = glob.glob('*.txt')
    flag="found"
    for each_file in my_files:
        with open(each_file,'r') as file_r:
            content=file_r.readlines()
            for each in content: 
                if (re.sub(r"[^a-zA-Z0-9\s]",'', config)) not in each:
                    flag="not found"
    return flag
def validate_hw(hw):
    os.chdir(r'C:\\Users\\ndhande\\Downloads\\PACIFIC_GAS_AND_ELECTRIC_Cat3850_and_Cat3650_PSRR_Raw_2022-10-10T13-28-31.283325\\Show Inventory')
    my_files = glob.glob('*.txt')
    flag="found"
    for each_file in my_files:
        with open(each_file,'r') as file_r:
            content=file_r.readlines()
            for each in content: 
                if (re.sub(r"[^a-zA-Z0-9\s]",'', hw)) not in each:
                    flag="not found"
    return flag