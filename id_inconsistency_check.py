import os
import pandas as pd


import os
import pandas as pd

def compare_redcap_maganamed_ids(redcap_df, maganamed_df, save_path):
    """
    Compares study_id differences between REDCap and maganamed (patients only),
    and saves missing IDs separately.

    Args:
        redcap_df (pd.DataFrame): REDCap dataframe (must contain 'record_id' column)
        maganamed_df (pd.DataFrame): maganamed dataframe (must contain 'participant_identifier' column)
        save_path (str): Folder path to save the output files
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Extract ID sets
    redcap_ids = set(redcap_df['record_id'])

    # Exclude non-patient IDs from maganamed
    all_maganamed_ids = maganamed_df['participant_identifier'].dropna().astype(str)
    is_patient = ~all_maganamed_ids.str.contains(r'[_-][ACF][_ -]', regex=True)
    maganamed_patient_ids = set(all_maganamed_ids[is_patient])

    # REDCap but not in maganamed (patient only)
    missing_in_maganamed = redcap_ids - maganamed_patient_ids
    if missing_in_maganamed:
        df_missing = pd.DataFrame({'study_id': list(missing_in_maganamed)})
        df_missing['note'] = 'Present in REDCap, missing in maganamed (patients only)'
        path = os.path.join(save_path, 'missing_in_maganamed.xlsx')
        df_missing.to_excel(path, index=False, engine='openpyxl')
        print(f"✅⚠️ Saved missing_in_maganamed.xlsx: {len(df_missing)} IDs")
    else:
        print("✅ No missing IDs from REDCap side.")

    # maganamed (patients only) but not in REDCap
    missing_in_redcap = maganamed_patient_ids - redcap_ids
    if missing_in_redcap:
        df_missing = pd.DataFrame({'study_id': list(missing_in_redcap)})
        df_missing['note'] = 'Present in maganamed (patients only), missing in REDCap'
        path = os.path.join(save_path, 'missing_in_redcap_fromMaganaMed.xlsx')
        df_missing.to_excel(path, index=False, engine='openpyxl')
        print(f"✅⚠️ Saved missing_in_redcap_fromMaganaMed.xlsx: {len(df_missing)} IDs")
    else:
        print("✅ No missing IDs from maganamed side.")


def compare_redcap_dmmh_ids(redcap_df, dmmh_df, save_path):
    """
    Compares study_id differences between REDCap and dmmh, and saves missing IDs separately.

    Args:
        redcap_df (pd.DataFrame): REDCap dataframe (must contain 'record_id' column)
        dmmh_df (pd.DataFrame): dmmh dataframe (must contain 'Participant' column)
        save_path (str): Folder path to save the output files
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        # print(f"📁 Created output directory: {os.path.abspath(save_path)}")

    # Extract ID sets
    redcap_ids = set(redcap_df['record_id'])
    dmmh_ids = set(dmmh_df['Participant'])

    # # IDs present in REDCap but missing in dmmh
    # missing_in_dmmh = redcap_ids - dmmh_ids
    # if missing_in_dmmh:
    #     df_missing_dmmh = pd.DataFrame({'study_id': list(missing_in_dmmh)})
    #     df_missing_dmmh['note'] = 'Present in REDCap, missing in dmmh'
    #     # output_path_dmmh = os.path.join(save_path, 'missing_in_dmmh.csv')
    #     # df_missing_dmmh.to_csv(output_path_dmmh, index=False, sep=';')
    #     # print(f"✅⚠️ Saved missing_in_dmmh.csv: {len(df_missing_dmmh)} IDs")
    #     output_path_dmmh = os.path.join(save_path, 'missing_in_dmmh.xlsx')
    #     df_missing_dmmh.to_excel(output_path_dmmh, index=False, engine='openpyxl')
    #     print(f"✅⚠️ Saved missing_in_dmmh.xlsx: {len(df_missing_dmmh)} IDs")
    # else:
    #     print("✅ No missing IDs from REDCap side.")

    # IDs present in dmmh but missing in REDCap
    missing_in_redcap = dmmh_ids - redcap_ids
    if missing_in_redcap:
        df_missing_redcap = pd.DataFrame({'study_id': list(missing_in_redcap)})
        df_missing_redcap['note'] = 'Present in dmmh, missing in REDCap'
        # output_path_redcap = os.path.join(save_path, 'missing_in_redcap_fromDMMH.csv')
        # df_missing_redcap.to_csv(output_path_redcap, index=False, sep=';')
        # print(f"✅⚠️ Saved missing_in_redcap_fromDMMH.csv: {len(df_missing_redcap)} IDs")
        output_path_redcap = os.path.join(save_path, 'missing_in_redcap_fromDMMH.xlsx')
        df_missing_redcap.to_excel(output_path_redcap, index=False, engine='openpyxl')
        print(f"✅⚠️ Saved missing_in_redcap_fromDMMH.xlsx: {len(df_missing_redcap)} IDs")
    else:
        print("✅ No missing IDs from dmmh side.")



def compare_redcap_movisensESM_ids(redcap_df, movisensESM_df, save_path):
    """
    Compares study_id differences between REDCap and movisensESM, and saves missing IDs separately.

    Args:
        redcap_df (pd.DataFrame): REDCap dataframe (must contain 'record_id' column)
        movisensESM_df (pd.DataFrame): movisensESM dataframe (must contain 'participant_id' column)
        save_path (str): Folder path to save the output files
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        # print(f"📁 Created output directory: {os.path.abspath(save_path)}")

    # Extract ID sets
    redcap_ids = set(redcap_df['record_id'])
    movisensESM_ids = set(movisensESM_df['participant_id'])

    # # IDs present in REDCap but missing in movisensESM
    # missing_in_movisensESM = redcap_ids - movisensESM_ids
    # if missing_in_movisensESM:
    #     df_missing_movisensESM = pd.DataFrame({'study_id': list(missing_in_movisensESM)})
    #     df_missing_movisensESM['note'] = 'Present in REDCap, missing in movisensESM'
    #     # output_pathmovisensESM = os.path.join(save_path, 'missing_in_movisensESM.csv')
    #     # df_missing_movisensESM.to_csv(output_path_movisensESM, index=False, sep=';')
    #     # print(f"✅⚠️ Saved missing_in_movisensESM.csv: {len(df_missing_movisensESM)} IDs")
    #     output_path_movisensESM = os.path.join(save_path, 'missing_in_movisensESM.xlsx')
    #     df_missing_movisensESM.to_excel(output_path_movisensESM, index=False, engine='openpyxl')
    #     print(f"✅⚠️ Saved missing_in_movisensESM.xlsx: {len(df_missing_movisensESM)} IDs")
    # else:
    #     print("✅ No missing IDs from REDCap side.")

    # IDs present in movisensESM but missing in REDCap
    missing_in_redcap = movisensESM_ids - redcap_ids
    if missing_in_redcap:
        df_missing_redcap = pd.DataFrame({'study_id': list(missing_in_redcap)})
        df_missing_redcap['note'] = 'Present in movisensESM, missing in REDCap'
        # output_path_redcap = os.path.join(save_path, 'missing_in_redcap_fromMovisensESM.csv')
        # df_missing_redcap.to_csv(output_path_redcap, index=False, sep=';')
        # print(f"✅⚠️ Saved missing_in_redcap_fromMovisensESM.csv: {len(df_missing_redcap)} IDs")
        output_path_redcap = os.path.join(save_path, 'missing_in_redcap_fromMovisensESM.xlsx')
        df_missing_redcap.to_excel(output_path_redcap, index=False, engine='openpyxl')
        print(f"✅⚠️ Saved missing_in_redcap_fromMovisensESM.xlsx: {len(df_missing_redcap)} IDs")
    else:
        print("✅ No missing IDs from movisensESM side.")


def compare_redcap_movisensSensing_ids(redcap_df, movisSensing_df, save_path):
    """
    Compares study_id differences between REDCap and movisensSensing, and saves missing IDs separately.

    Args:
        redcap_df (pd.DataFrame): REDCap dataframe (must contain 'record_id' column)
        movisensSensing_df (pd.DataFrame): movisensSensing dataframe (must contain 'study_id' column)
        save_path (str): Folder path to save the output files
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        # print(f"📁 Created output directory: {os.path.abspath(save_path)}")

    # Extract ID sets
    redcap_ids = set(redcap_df['record_id'])
    movisensSensing_ids = set(movisSensing_df['study_id'])

    # # IDs present in REDCap but missing in movisensSensing
    # missing_in_movisensSensing = redcap_ids - movisensSensing_ids
    # if missing_in_movisensSensing:
    #     df_missing_movisensSensing = pd.DataFrame({'study_id': list(missing_in_movisensSensing)})
    #     df_missing_movisensSensing['note'] = 'Present in REDCap, missing in movisensSensing'
    #     # output_pathmovisensSensing = os.path.join(save_path, 'missing_in_movisensSensing.csv')
    #     # df_missing_movisensSensing.to_csv(output_path_movisensSensing, index=False, sep=';')
    #     # print(f"✅⚠️ Saved missing_in_movisensSensing.csv: {len(df_missing_movisensSensing)} IDs")
    #     output_path_movisensSensing = os.path.join(save_path, 'missing_in_movisensSensing.xlsx')
    #     df_missing_movisensSensing.to_excel(output_path_movisensSensing, index=False, engine='openpyxl')
    #     print(f"✅⚠️ Saved missing_in_movisensSensing.xlsx: {len(df_missing_movisensSensing)} IDs")
    # else:
    #     print("✅ No missing IDs from REDCap side.")

    # IDs present in movisensSensing but missing in REDCap
    missing_in_redcap = movisensSensing_ids - redcap_ids
    if missing_in_redcap:
        df_missing_redcap = pd.DataFrame({'study_id': list(missing_in_redcap)})
        df_missing_redcap['note'] = 'Present in movisensSensing, missing in REDCap'
        # output_path_redcap = os.path.join(save_path, 'missing_in_redcap_fromMovisensSensing.csv')
        # df_missing_redcap.to_csv(output_path_redcap, index=False, sep=';')
        # print(f"✅⚠️ Saved missing_in_redcap_fromMovisensSensing.csv: {len(df_missing_redcap)} IDs")
        output_path_redcap = os.path.join(save_path, 'missing_in_redcap_fromMovisensSensing.xlsx')
        df_missing_redcap.to_excel(output_path_redcap, index=False, engine='openpyxl')
        print(f"✅⚠️ Saved missing_in_redcap_fromMovisensSensing.xlsx: {len(df_missing_redcap)} IDs")
    else:
        print("✅ No missing IDs from movisensSensing side.")


# Optional
def merge_maganamed_with_redcap(
    maganamed_csv_path,
    redcap_csv_path,
    output_csv_path,
    missing_in_redcap_log_path,
    missing_in_maganamed_log_path
):
    """
    Merges MaganaMed ID list with REDCap data by 'participant_identifier' ↔ 'record_id' matching.
    Saves both unmatched MaganaMed IDs and unmatched REDCap IDs separately.

    Args:
        maganamed_csv_path (str): Path to MaganaMed ID list CSV.
        redcap_csv_path (str): Path to REDCap data CSV.
        output_csv_path (str): Output path for merged CSV.
        missing_in_redcap_log_path (str): Path for log of IDs missing in REDCap.
        missing_in_maganamed_log_path (str): Path for log of IDs missing in MaganaMed.
    """
    df_maganamed = pd.read_csv(maganamed_csv_path, sep=';')
    df_redcap = pd.read_csv(redcap_csv_path, sep=';')

    if 'participant_identifier' not in df_maganamed.columns:
        print("❌ 'participant_identifier' column not found in MaganaMed file.")
        return

    if 'record_id' not in df_redcap.columns:
        print("❌ 'record_id' column not found in REDCap file.")
        return

    # Merge on ID
    merged_df = pd.merge(
        df_maganamed,
        df_redcap,
        left_on='participant_identifier',
        right_on='record_id',
        how='left'
    )

    # 1. Present in MaganaMed but missing in REDCap
    missing_redcap = merged_df[merged_df['record_id'].isna()][['participant_identifier']]
    if not missing_redcap.empty:
        missing_redcap.to_csv(missing_in_redcap_log_path, sep=';', index=False)
        print(f"⚠️ Missing in REDCap: saved to {missing_in_redcap_log_path}")
    else:
        print("✅ All MaganaMed IDs matched to REDCap.")

    # 2. Present in REDCap but missing in MaganaMed
    redcap_ids = set(df_redcap['record_id'].dropna().astype(str))
    maganamed_ids = set(df_maganamed['participant_identifier'].dropna().astype(str))
    missing_maganamed_ids = sorted(redcap_ids - maganamed_ids)

    if missing_maganamed_ids:
        df_missing_maganamed = pd.DataFrame(missing_maganamed_ids, columns=['record_id'])
        df_missing_maganamed.to_csv(missing_in_maganamed_log_path, sep=';', index=False)
        print(f"✅⚠️ Missing in MaganaMed: saved to {missing_in_maganamed_log_path}")
    else:
        print("✅ All REDCap IDs matched to MaganaMed.")

    # Drop unnecessary record_id column after merging
    if 'record_id' in merged_df.columns:
        merged_df.drop(columns=['record_id'], inplace=True)

    # Sort by participant_identifier alphabetically
    merged_df = merged_df.sort_values(by='participant_identifier').reset_index(drop=True)

    # Save merged result
    merged_df.to_csv(output_csv_path, sep=';', index=False)
    print(f"✅ Merged file saved to: {output_csv_path}")

