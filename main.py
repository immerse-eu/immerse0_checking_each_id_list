import pandas as pd
# import prepare_redcap
# import prepare_allocationlist
import id_inconsistency_check
import prepare_maganamed_idlist
import prepare_dmmh_idlist
import prepare_movisens_idlist
import idlist4pseudonimization
# import integrate_all_idlists
import os
import yaml

""" 
This repository is designed to extract all unique IDs from each data source (MaganaMed, DMMH, movisensXS).
The extracted ID lists will be used 
    to check for ID inconsistencies across systems 
    and to prepare lists of IDs for pseudonymization.
"""

# Read configuration file
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Get paths from config
base_path_maganamed = config['maganamedPath']['base_path']
base_path_dmmh = config['dmmhPath']['base_path']
base_path_movisens = config['movisensxsPath']['base_path']
save_path_extractedIDs = config['extractedIDsPath']['save_path_extractedIDs']

base_path_IDpseudo = config['extractedIDsPath']['base_path_IDpseudo']
save_path_IDpseudo = config['extractedIDsPath']['save_path_IDpseudo']

output_filename_maganamed = "extracted_ids_maganamed.csv"
output_filename_dmmh = "extracted_ids_dmmh.csv"
output_filename_moviESM = "extracted_ids_movisensESM.csv"
output_filename_moviSensing = "extracted_ids_movisensSensing.csv"


# # base_path_dmmh = config['idListsPath']['dmmh']
# # base_path_movisensESM = config['idListsPath']['movisensESM']
#
# save_path = config['idListsPath']['save_path']
# save_path_redcap = os.path.join(config['idListsPath']['save_path'], "concated_redcap.csv")
# save_path_allocation = os.path.join(config['idListsPath']['save_path'], "concatenated_allocationlist.csv")


# Call the processing function
# (1) extract IDs from MaganaMed (! inclusive Clinician IDs, Admin IDs, ..., and so on.)
maganamedIDs_df = prepare_maganamed_idlist.collect_unique_id_maganamed(base_path_maganamed, save_path_extractedIDs, output_filename_maganamed)
prepare_maganamed_idlist.analyze_and_categorize_ids(save_path_extractedIDs, output_filename_maganamed, save_path_extractedIDs)

# (2) extract IDs from MaganaMed
# Please choose a proper function:
    # If we received one single JSON file per center containing data across all dates
# dmmhIDs_df = prepare_dmmh_idlist.collect_unique_id_dmmh_singleExport(base_path_dmmh, save_path_extractedIDs, output_filename_dmmh)
    # If we received multiple JSON files per center, separated by date
dmmhIDs_df = prepare_dmmh_idlist.collect_unique_id_dmmh_multipleExport(base_path_dmmh, save_path_extractedIDs, output_filename_dmmh)

prepare_dmmh_idlist.analyze_and_categorize_ids(save_path_extractedIDs, output_filename_dmmh, save_path_extractedIDs)

# (3) extract IDs from movisensESM
movisensESMIDs_df = prepare_movisens_idlist.collect_unique_id_movisensESM(base_path_movisens, save_path_extractedIDs, output_filename_moviESM)
prepare_movisens_idlist.analyze_and_categorize_ids_ESM(save_path_extractedIDs, output_filename_moviESM, save_path_extractedIDs)

# (4) extract IDs from movisensSensing
movisensSensingIDs_df = prepare_movisens_idlist.collect_unique_id_movisensSensing(base_path_movisens, save_path_extractedIDs, output_filename_moviSensing)
prepare_movisens_idlist.analyze_and_categorize_ids_Sensing(save_path_extractedIDs, output_filename_moviSensing, save_path_extractedIDs)

print("-------------------")

# (5)
idlist4pseudonimization.collect_unique_id_4_pseudonimizatoin(base_path_IDpseudo, save_path_IDpseudo)




# (1) merge redcap lists and modify (Export4Wolfgang)
# concatenated_redcap = prepare_redcap.concatenate_redcapInfos(base_path_redcap, save_path)

# (2) merge Allocation list
# concatenated_allocation = prepare_allocationlist.concatenate_allocationlists(base_path_alllocation, save_path)


input_redcap = r"C:\Users\kimgn\Documents\GitHub\IMMERSE_2025\data_processed\idLists\redcap_02_concatenated_modified.csv"
concatenated_redcap = pd.read_csv(input_redcap, sep=';', dtype=str)

save_path_missingIDs = config['extractedIDsPath']['save_path_missingIDs']

# id list 비교
id_inconsistency_check.compare_redcap_maganamed_ids(concatenated_redcap, maganamedIDs_df, save_path_missingIDs) # only PatientIDs (not ClinicianIDs, ..)
id_inconsistency_check.compare_redcap_dmmh_ids(concatenated_redcap, dmmhIDs_df, save_path_missingIDs)
id_inconsistency_check.compare_redcap_movisensESM_ids(concatenated_redcap, movisensESMIDs_df, save_path_missingIDs)
id_inconsistency_check.compare_redcap_movisensSensing_ids(concatenated_redcap, movisensSensingIDs_df, save_path_missingIDs)


# id_inconsistency_check.compare_redcap_with_multiple_sources(concatenated_redcap, maganamed_df, dmmd_df, movisens_df, save_path)


# (3) Integrate REDCap and Allocationlist
# integrate_all_idlists.integrate_redcap_and_allocation(concatenated_redcap, concatenated_allocation, save_path)

# (4) 조건필터링/ 중복치료사 제거????

