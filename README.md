# immerse0_checking_each_id_list


This repository is for extracting all unique participant IDs from each data source (MaganaMed, DMMH, movisensXS).

The extracted ID lists will be used 
- to check for ID inconsistencies across systems 
- and to prepare lists of IDs for pseudonymization.


**Instructions:**
Config YAML file

**Input:**
all raw data, 
located in the directory specified by the configuration file 
(\data\). 

**Output:**
extracted ID list, 
saved to the directory specified by the configuration file 
(\data_processed\idLists\)


**Status:** completed