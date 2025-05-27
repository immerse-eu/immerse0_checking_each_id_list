import pandas as pd
import id_inconsistency_check
import prepare_maganamed_idlist
import prepare_dmmh_idlist
import prepare_movisens_idlist
import idlist4pseudonimization
import os
import yaml

# Read configuration file
with open("../assets/config.yaml", "r", encoding="utf-8") as f:
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
output_filename_moviESM = "extracted_ids_movisens_esm.csv"
output_filename_moviSensing = "extracted_ids_movisens_sensing.csv"

concatenated_redcap = config['redcap_master_path']['all_ids_redcap']
save_path_missingIDs = config['extractedIDsPath']['save_path_missingIDs']


def run_data_extraction():
    # (1) extract IDs from MaganaMed.
    raw_df_maganamed = prepare_maganamed_idlist.collect_unique_id_maganamed(
        base_path_maganamed,
        save_path_extractedIDs,
        output_filename_maganamed
    )

    # (2) extract IDs from DMMH.
    raw_df_dmmh = prepare_dmmh_idlist.collect_unique_id_dmmh_multiple_export(
        base_path_dmmh,
        save_path_extractedIDs,
        output_filename_dmmh
    )

    # (3) extract IDs from movisensESM
    raw_df_movisens_esm = prepare_movisens_idlist.collect_unique_id_movisens_esm(
        base_path_movisens,
        save_path_extractedIDs,
        output_filename_moviESM
    )

    # (4) extract IDs from movisensSensing
    raw_df_movisens_sensing = prepare_movisens_idlist.collect_unique_id_movisens_sensing(
        base_path_movisens,
        save_path_extractedIDs,
        output_filename_moviSensing
    )

    # (5) Collect unique ID from all extracted_IDs
    # idlist4pseudonimization.collect_unique_id_4_pseudonimizatoin(
    #     base_path_IDpseudo,
    #     save_path_IDpseudo
    # )
    return raw_df_maganamed, raw_df_dmmh, raw_df_movisens_esm, raw_df_movisens_sensing


def sort_extracted_data():
    # (1) Categorize IDs from Maganamed
    prepare_maganamed_idlist.analyze_and_categorize_ids(
        save_path_extractedIDs,
        output_filename_maganamed,
        save_path_extractedIDs
    )

    # (2) Categorize IDs from DMMH.
    #  Option 1. If we received one single JSON file per center containing data across all dates
    # prepare_dmmh_idlist.collect_unique_id_dmmh_singleExport(
    #     base_path_dmmh,
    #     save_path_extractedIDs,
    #     output_filename_dmmh
    # )

    #  Option 2. If we received multiple JSON files per center, separated by date
    prepare_dmmh_idlist.analyze_and_categorize_ids(
        save_path_extractedIDs,
        output_filename_dmmh,
        save_path_extractedIDs
    )

    # (3) Categorize IDs from movisensESM
    prepare_movisens_idlist.analyze_and_categorize_ids_ESM(
        save_path_extractedIDs,
        output_filename_moviESM,
        save_path_extractedIDs
    )

    # (4) Categorize IDs from movisensSensing
    prepare_movisens_idlist.analyze_and_categorize_ids_Sensing(
        save_path_extractedIDs,
        output_filename_moviSensing,
        save_path_extractedIDs
    )

    #  (5) Collect unique ID from all extracted_IDs
    # idlist4pseudonimization.collect_unique_id_4_pseudonimizatoin(base_path_IDpseudo, save_path_IDpseudo)


def compare_extracted_ids_with_redcap(raw_df_maganamed, raw_df_dmmh, raw_df_movisens_esm, raw_df_movisens_sensing):
    # Optional: just to control id inconsistencies ----------------------------------------
    # Op1. id list comparison
    id_inconsistency_check.compare_redcap_maganamed_ids(
        concatenated_redcap,
        raw_df_maganamed,
        save_path_missingIDs
    )  # only PatientIDs (not ClinicianIDs, ..)

    id_inconsistency_check.compare_redcap_dmmh_ids(
        concatenated_redcap,
        raw_df_dmmh,
        save_path_missingIDs
    )

    id_inconsistency_check.compare_redcap_movisensESM_ids(
        concatenated_redcap,
        raw_df_movisens_esm,
        save_path_missingIDs
    )

    id_inconsistency_check.compare_redcap_movisensSensing_ids(
        concatenated_redcap,
        raw_df_movisens_sensing,
        save_path_missingIDs
    )

def main():
    raw_df_maganamed, raw_df_dmmh, raw_df_movisens_esm, raw_df_movisens_sensing = run_data_extraction()
    sort_extracted_data()
    compare_extracted_ids_with_redcap(
        raw_df_maganamed,
        raw_df_dmmh,
        raw_df_movisens_esm,
        raw_df_movisens_sensing
    )

    # Op2. id list comparison
    # id_inconsistency_check.merge_maganamed_with_redcap(
    #     maganamed_csv_path = os.path.join(list_base_path, "extracted_ids_maganamed.csv"),
    #     redcap_csv_path = os.path.join(list_base_path, "redcap_02_concatenated_modified.csv"),
    #     output_csv_path = os.path.join(list_base_path, "00_merged_magana_redcap.csv"),
    #     missing_in_redcap_log_path=os.path.join(list_base_path, "missing_in_redcap.csv"),
    #     missing_in_maganamed_log_path=os.path.join(list_base_path, "missing_in_maganamed.csv")
    # )

if __name__ == "__main__":
    main()
