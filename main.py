import pandas as pd
import id_inconsistency_check
import prepare_maganamed_idlist
import prepare_dmmh_idlist
import prepare_movisens_idlist
import idlist4pseudonimization
import os
import yaml


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


# Extract IDs from various Data sources
# (1) extract IDs from MaganaMed (! inclusive Clinician IDs, Admin IDs, ..., and so on.)
maganamedIDs_df = prepare_maganamed_idlist.collect_unique_id_maganamed(base_path_maganamed, save_path_extractedIDs, output_filename_maganamed)
prepare_maganamed_idlist.analyze_and_categorize_ids(save_path_extractedIDs, output_filename_maganamed, save_path_extractedIDs)

# (2) extract IDs from DMMH
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

# (5) Collect unique ID from all extracted_IDs
idlist4pseudonimization.collect_unique_id_4_pseudonimizatoin(base_path_IDpseudo, save_path_IDpseudo)



# Optional: just to control id inconsistencies ----------------------------------------
# Op1. id list comparison
# id_inconsistency_check.compare_redcap_maganamed_ids(concatenated_redcap, maganamedIDs_df, save_path_missingIDs) # only PatientIDs (not ClinicianIDs, ..)
# id_inconsistency_check.compare_redcap_dmmh_ids(concatenated_redcap, dmmhIDs_df, save_path_missingIDs)
# id_inconsistency_check.compare_redcap_movisensESM_ids(concatenated_redcap, movisensESMIDs_df, save_path_missingIDs)
# id_inconsistency_check.compare_redcap_movisensSensing_ids(concatenated_redcap, movisensSensingIDs_df, save_path_missingIDs)

# Op2. id list comparison
# id_inconsistency_check.merge_maganamed_with_redcap(
#     maganamed_csv_path = os.path.join(list_base_path, "extracted_ids_maganamed.csv"),
#     redcap_csv_path = os.path.join(list_base_path, "redcap_02_concatenated_modified.csv"),
#     output_csv_path = os.path.join(list_base_path, "00_merged_magana_redcap.csv"),
#     missing_in_redcap_log_path=os.path.join(list_base_path, "missing_in_redcap.csv"),
#     missing_in_maganamed_log_path=os.path.join(list_base_path, "missing_in_maganamed.csv")
# )





